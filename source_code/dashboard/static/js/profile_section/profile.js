/* FUNCTION FOR PROFILE DATA FETCH AND REDIRECT */

document.addEventListener('DOMContentLoaded', async () => {
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

        const Name = document.getElementById('full_name');
        const PlaceDateBirth = document.getElementById('place_date_birth');

        Name.textContent = data.profile.full_name;
        PlaceDateBirth.textContent = 'Nato a ' + data.profile.city + ' il ' + data.profile.birth_date ;


        const iso = data.created_at;               
        const dateOnly = iso.split('T')[0];        
        const Status = document.getElementById('status_account')

        Status.textContent = 'Verificato - attivo dal ' + dateOnly;

        
    } catch (err) {
        console.log(err);
    }
});


