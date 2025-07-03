/* FUNCTION FOR PROFILE DATA FETCH AND REDIRECT */

document.addEventListener('DOMContentLoaded', async () => {
    const cont  = document.getElementById('profile-container');
    cont.innerHTML = '<p>Caricamento dati profilo…</p>';
    try {
        const resp = await fetch('/api/accounts/me/', {
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('accessToken'),
                'Accept': 'application/json',
            }
        });
        if (!resp.ok) {
            throw new Error(`Errore ${resp.status}`);
        }
        const data = await resp.json();
        cont.innerHTML = `
            <h3>Il tuo profilo</h3>
            <p><strong>Nome:</strong> ${data.profile ? data.profile.full_name : ''}</p>
            <p><strong>Telefono:</strong> ${data.profile ? data.profile.phone_number : ''}</p>
            <p><strong>Data di nascita:</strong> ${data.profile ? data.profile.birth_date : ''}</p>
            <p><strong>Codice fiscale:</strong> ${data.profile ? data.profile.fiscal_code : ''}</p>
            <p><strong>Città:</strong> ${data.profile ? data.profile.city : ''}</p>
            <p><strong>CAP:</strong> ${data.profile ? data.profile.postal_code : ''}</p>
            <hr>
            <h4>Il tuo conto</h4>
            <p><strong>IBAN:</strong> ${data.iban}</p>
            <p><strong>Saldo:</strong> ${data.balance} ${data.currency}</p>
        `;
        cont.style.display = 'block';
    } catch (err) {
        cont.innerHTML = '<p style="color:red;">Impossibile caricare il profilo: ' + err.message + '</p>';
    }
});


