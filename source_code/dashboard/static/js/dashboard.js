/* FUNCTION FOR HANDLING DROPDOWN MENU */
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('profileToggle');
  const menu   = document.getElementById('profileMenu');

  toggle.addEventListener('click', e => {
    e.stopPropagation();
    const isOpen = !menu.classList.contains('hidden');
    menu.classList.toggle('hidden', isOpen);
    toggle.setAttribute('aria-expanded', String(!isOpen));
  });

  document.addEventListener('click', () => {
    if (!menu.classList.contains('hidden')) {
      menu.classList.add('hidden');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
});



/* FUNCTION FOR CREDIT CARD */
document.addEventListener('DOMContentLoaded', () => {

  const front = document.querySelector('.finhub-card:not(.back)');
  const back  = document.querySelector('.finhub-card.back');

  if (front){
    const num = front.dataset.number;
    const bal = Number(front.dataset.balance).toLocaleString('it-IT',{minimumFractionDigits:2});

    front.querySelector('.card-number').textContent = num.replace(/(\d{4})(?=\d)/g,'$1 ');
    front.querySelector('.card-name').textContent   = front.dataset.name;
    front.querySelector('.card-expiry').textContent = front.dataset.expiry;
    front.querySelector('.card-balance').textContent = `€ ${bal}`;


    front.querySelector('.card-balance').classList.add('masked');
  }
  if (back){
    back.querySelector('.cvv-box').textContent = back.dataset.cvv;
    back.querySelector('.cvv-box').classList.add('masked');
  }

  const eyeBtn = document.getElementById('toggle-eye');
  eyeBtn.addEventListener('click', () => {
    eyeBtn.classList.toggle('open');          
    document.querySelectorAll('.masked, .unmasked')
            .forEach(el => el.classList.toggle('unmasked'));
  });
});

document.addEventListener('DOMContentLoaded', function() {
    const scrollContent = document.querySelector('.scroll-content');
    const leftButton = document.querySelector('.left-button');
    const rightButton = document.querySelector('.right-button');
    if (scrollContent && leftButton && rightButton) {
        const scrollAmount = 200; 
        // Impedisci scroll verticale via JS
        scrollContent.addEventListener('wheel', function(e) {
            if (e.deltaY !== 0) {
                e.preventDefault();
                scrollContent.scrollBy({ left: e.deltaY, behavior: 'smooth' });
            }
        }, { passive: false });
        // Scroll con i bottoni solo se serve
        function updateButtons() {
            const maxScroll = scrollContent.scrollWidth - scrollContent.clientWidth;
            leftButton.disabled = scrollContent.scrollLeft <= 0;
            rightButton.disabled = scrollContent.scrollLeft >= maxScroll - 1;
        }
        leftButton.addEventListener('click', function() {
            scrollContent.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
            setTimeout(updateButtons, 300);
        });
        rightButton.addEventListener('click', function() {
            scrollContent.scrollBy({ left: scrollAmount, behavior: 'smooth' });
            setTimeout(updateButtons, 300);
        });
        scrollContent.addEventListener('scroll', updateButtons);
        window.addEventListener('resize', updateButtons);
        updateButtons();
    }
});

// FETCH DATI DASHBOARD E POPOLAMENTO DINAMICO

document.addEventListener('DOMContentLoaded', () => {
  fetch('/api/dashboard-data/', {
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem('accessToken'),
      'Accept': 'application/json'
    },
    credentials: 'same-origin'
  })
    .then(response => response.json())
    .then(data => {
      // Popola nome utente e ultimo accesso
      if (data.user_full_name) {
        const userNameElem = document.querySelector('.banner-container h3');
        if (userNameElem) userNameElem.textContent = data.user_full_name;
      }
      if (data.last_login) {
        const lastLoginElem = document.querySelector('.banner-container p');
        if (lastLoginElem) {
          const date = new Date(data.last_login);
          lastLoginElem.textContent = 'Ultimo accesso: ' + date.toLocaleString('it-IT');
        }
      }
      // Popola dati carta e saldo
      if (data.card && data.account) {
        const front = document.querySelector('.finhub-card:not(.back)');
        const back  = document.querySelector('.finhub-card.back');
        if (front) {
          // Format card number with space every 4 digits
          let cardNumber = data.card.card_number || '0000';
          cardNumber = cardNumber.replace(/(\d{4})(?=\d)/g, '$1 ');
          front.dataset.number = cardNumber;
          front.dataset.name = data.card.holder_name || '---';
          front.dataset.expiry = (data.card.expiry_month ? String(data.card.expiry_month).padStart(2, '0') : '--') + '/' + (data.card.expiry_year || '--');
          front.dataset.balance = data.account.balance || '0.00';
          // Aggiorna i campi visivi
          front.querySelector('.card-number').textContent = front.dataset.number;
          front.querySelector('.card-name').textContent = front.dataset.name;
          front.querySelector('.card-expiry').textContent = front.dataset.expiry;
          front.querySelector('.card-balance').textContent = `€ ${Number(front.dataset.balance).toLocaleString('it-IT',{minimumFractionDigits:2})}`;
        }
        if (back) {
          back.dataset.cvv = data.card.cvv_hash ;
          back.querySelector('.cvv-box').textContent = back.dataset.cvv;
        }
      }
    })
    .catch(err => {
      console.error('Errore nel fetch dati dashboard:', err);
    });
});

