document.addEventListener('DOMContentLoaded', function() {
    // Popola le card
    fetch('/api/dashboard-stats/', {
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('accessToken'),
            'Accept': 'application/json'
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('bonifici-inviati').textContent = data.bonifici_inviati;
        document.getElementById('bonifici-ricevuti').textContent = data.bonifici_ricevuti;
        document.getElementById('transazioni').textContent = data.transazioni;
        document.getElementById('categorie').textContent = data.categorie;
    })
    .catch(err => {
        console.error('Errore nel fetch dati dashboard:', err);
    });

    // Popola il grafico Entrate/Uscite - FETCH COMBINATO
    Promise.all([
        fetch('/api/transactions/', { 
            headers: { 'Authorization': 'Bearer ' + localStorage.getItem('accessToken') } 
        }).then(res => res.json()),
        fetch('/api/accrediti/', { 
            headers: { 'Authorization': 'Bearer ' + localStorage.getItem('accessToken') } 
        }).then(res => res.json())
    ]).then(([transazioni, accrediti]) => {
        // Processa transazioni (uscite)
        const txs = (transazioni.results || []).map(tx => ({
            date: tx.date,
            amount: Math.abs(tx.amount), // uscite sempre positive per il grafico
            type: 'uscita'
        }));
        
        // Processa accrediti (entrate)
        const accs = (accrediti.results || []).map(acc => ({
            date: acc.date,
            amount: Math.abs(acc.amount), // entrate sempre positive
            type: 'entrata'
        }));

        // Combina e raggruppa per giorno/mese
        const allMovimenti = txs.concat(accs);
        const chartData = processDataForChart(allMovimenti);
        
        if (!chartData || !chartData.current_month) return;
        
        const labels = chartData.current_month.map(d => d.day);
        const entrateMese = chartData.current_month.map(d => d.entrate);
        const usciteMese = chartData.current_month.map(d => d.uscite);
        const entratePrecedente = chartData.previous_month.map(d => d.entrate);
        const uscitePrecedente = chartData.previous_month.map(d => d.uscite);

        const ctxLine = document.getElementById('lineChart').getContext('2d');
        new Chart(ctxLine, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Entrate (mese attuale)',
                        data: entrateMese,
                        borderColor: '#2ecc71',
                        backgroundColor: 'rgba(46,204,113,0.1)',
                        tension: 0.4,
                        borderWidth: 2,
                    },
                    {
                        label: 'Uscite (mese attuale)',
                        data: usciteMese,
                        borderColor: '#e74c3c',
                        backgroundColor: 'rgba(231,76,60,0.1)',
                        tension: 0.4,
                        borderWidth: 2,
                    },
                    {
                        label: 'Entrate (mese precedente)',
                        data: entratePrecedente,
                        borderColor: '#2ecc71',
                        borderDash: [5,5],
                        backgroundColor: 'rgba(46,204,113,0.05)',
                        tension: 0.4,
                        borderWidth: 1,
                        pointRadius: 0,
                        fill: false,
                        hidden: false,
                    },
                    {
                        label: 'Uscite (mese precedente)',
                        data: uscitePrecedente,
                        borderColor: '#e74c3c',
                        borderDash: [5,5],
                        backgroundColor: 'rgba(231,76,60,0.05)',
                        tension: 0.4,
                        borderWidth: 1,
                        pointRadius: 0,
                        fill: false,
                        hidden: false,
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'top' },
                    title: { display: true, text: 'Entrate e Uscite - Ultimi 2 mesi' }
                }
            }
        });
    })
    .catch(err => {
        console.error('Errore nel fetch grafico entrate/uscite:', err);
    });

    // Popola il grafico per categoria - FETCH COMBINATO
    Promise.all([
        fetch('/api/transactions/', { 
            headers: { 'Authorization': 'Bearer ' + localStorage.getItem('accessToken') } 
        }).then(res => res.json()),
        fetch('/api/accrediti/', { 
            headers: { 'Authorization': 'Bearer ' + localStorage.getItem('accessToken') } 
        }).then(res => res.json())
    ]).then(([transazioni, accrediti]) => {
        // Raggruppa per categoria
        const categorieData = {};
        
        // Processa transazioni
        (transazioni.results || []).forEach(tx => {
            const cat = tx.category_name || 'Altro';
            if (!categorieData[cat]) categorieData[cat] = 0;
            categorieData[cat] += Math.abs(tx.amount);
        });
        
        // Processa accrediti
        (accrediti.results || []).forEach(acc => {
            const cat = acc.description || 'Entrate';
            if (!categorieData[cat]) categorieData[cat] = 0;
            categorieData[cat] += Math.abs(acc.amount);
        });

        const categorie = Object.keys(categorieData);
        const valori = Object.values(categorieData);
        
        if (categorie.length === 0) return;

        const ctxPie = document.getElementById('pieChart').getContext('2d');
        new Chart(ctxPie, {
            type: 'doughnut',
            data: {
                labels: categorie,
                datasets: [{
                    data: valori,
                    backgroundColor: [
                        '#2d8cf0',
                        '#2ecc71',
                        '#f1c40f',
                        '#e67e22',
                        '#9b59b6',
                        '#34495e',
                        '#e84393'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'right' },
                    title: { display: true, text: 'Transazioni per Categoria' }
                }
            }
        });
    })
    .catch(err => {
        console.error('Errore nel fetch grafico categorie:', err);
    });
});

// Funzione per processare i dati per il grafico temporale
function processDataForChart(movimenti) {
    const now = new Date();
    const currentMonth = now.getMonth();
    const currentYear = now.getFullYear();
    const previousMonth = currentMonth === 0 ? 11 : currentMonth - 1;
    const previousYear = currentMonth === 0 ? currentYear - 1 : currentYear;

    // Raggruppa per giorno
    const currentMonthData = {};
    const previousMonthData = {};

    movimenti.forEach(mov => {
        const date = new Date(mov.date);
        const month = date.getMonth();
        const year = date.getFullYear();
        const day = date.getDate();

        if (year === currentYear && month === currentMonth) {
            if (!currentMonthData[day]) {
                currentMonthData[day] = { entrate: 0, uscite: 0 };
            }
            if (mov.type === 'entrata') {
                currentMonthData[day].entrate += mov.amount;
            } else {
                currentMonthData[day].uscite += mov.amount;
            }
        } else if (year === previousYear && month === previousMonth) {
            if (!previousMonthData[day]) {
                previousMonthData[day] = { entrate: 0, uscite: 0 };
            }
            if (mov.type === 'entrata') {
                previousMonthData[day].entrate += mov.amount;
            } else {
                previousMonthData[day].uscite += mov.amount;
            }
        }
    });

    // Converti in array ordinato
    const daysInCurrentMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    const daysInPreviousMonth = new Date(previousYear, previousMonth + 1, 0).getDate();

    const current_month = [];
    const previous_month = [];

    for (let day = 1; day <= daysInCurrentMonth; day++) {
        current_month.push({
            day: day,
            entrate: currentMonthData[day]?.entrate || 0,
            uscite: currentMonthData[day]?.uscite || 0
        });
    }

    for (let day = 1; day <= daysInPreviousMonth; day++) {
        previous_month.push({
            day: day,
            entrate: previousMonthData[day]?.entrate || 0,
            uscite: previousMonthData[day]?.uscite || 0
        });
    }

    return { current_month, previous_month };
}