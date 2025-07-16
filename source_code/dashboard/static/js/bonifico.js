// Funzione per recuperare e popolare i dati del mittente
function fetchAndPopulateMittente(accessToken) {
  const mittenteNome = document.querySelector('input[name="mittente-nome"]');
  const mittenteEmail = document.querySelector('input[name="mittente-email"]');
  const mittenteIban = document.querySelector('input[name="mittente-iban"]');
  const mittenteCitta = document.querySelector('input[name="mittente-citta"]');

  fetch('/api/accounts/me/', {
    credentials: 'include',
    headers: {
      'Authorization': 'Bearer ' + accessToken,
      'Content-Type': 'application/json'
    }
  })
    .then(res => res.json())
    .then(data => {
      if (data) {
        if (mittenteNome) mittenteNome.value = data.profile?.full_name || '';
        if (mittenteEmail) mittenteEmail.value = data.email || '';
        if (mittenteIban) mittenteIban.value = data.iban || '';
        if (mittenteCitta) mittenteCitta.value = data.profile?.city || '';
      }
    });
}

// Gestione modale PIN e invio bonifico
function setupBonificoFlow(accessToken) {
  const form = document.querySelector('form');
  const pinModal = document.getElementById('pin-modal');
  const pinInput = document.getElementById('pin-input');
  const pinConfirmBtn = document.getElementById('pin-confirm-btn');
  const pinCancelBtn = document.getElementById('pin-cancel-btn');
  const pinLoader = document.getElementById('pin-loader');
  const pinError = document.getElementById('pin-error');
  const pinModalTitle = document.getElementById('pin-modal-title');
  const pinModalMessage = document.getElementById('pin-modal-message');
  const successModal = document.getElementById('success-modal');
  const viewReceiptBtn = document.getElementById('view-receipt-btn');
  const saveContactBtn = document.getElementById('save-contact-btn');
  const rubricaBtn = document.getElementById('rubrica-btn');
  const rubricaModal = document.getElementById('rubrica-modal');
  const rubricaList = document.getElementById('rubrica-list');
  const rubricaCloseBtn = document.getElementById('rubrica-close-btn');

  if (!form) return;

  // Mostra la modale PIN
  function showPinModal() {
    pinInput.value = '';
    pinError.textContent = '';
    pinLoader.style.display = 'none';
    pinInput.style.display = '';
    pinConfirmBtn.style.display = '';
    pinCancelBtn.style.display = '';
    pinModalTitle.textContent = 'Transizione iniziata';
    pinModalMessage.textContent = 'Inserisci il PIN per autorizzare il bonifico';
    pinModal.style.display = 'flex';
    pinInput.focus();
  }

  // Nascondi la modale PIN
  function hidePinModal() {
    pinModal.style.display = 'none';
  }

  // Mostra la modale di successo
  function showSuccessModal() {
    successModal.style.display = 'flex';
  }
  function hideSuccessModal() {
    successModal.style.display = 'none';
  }

  // Gestione submit form bonifico
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    showPinModal();
  });

  // Gestione click su "Autorizza" nella modale PIN
  pinConfirmBtn.addEventListener('click', function() {
    const pin = pinInput.value.trim();
    if (!pin) {
      pinError.textContent = 'Inserisci il PIN';
      return;
    }
    // Mostra loader
    pinLoader.style.display = 'block';
    pinInput.style.display = 'none';
    pinConfirmBtn.style.display = 'none';
    pinCancelBtn.style.display = 'none';
    pinError.textContent = '';
    pinModalTitle.textContent = 'Autorizzazione in corso...';
    pinModalMessage.textContent = '';

    // Recupera dati dai campi del form
    const importo = document.querySelector('.other-spec input[placeholder="Inserisci l\'importo"]')?.value || '';
    const nota = document.querySelector('.other-spec input[placeholder="Scrivi qui una nota testuale"]')?.value || '';
    const categoria = document.querySelector('.other-spec input[placeholder="Scrivi qui la categoria"]')?.value || '';
    const clausola = document.querySelector('.other-spec input[placeholder="Inserisci qui una motivazione"]')?.value || '';
    // Dati destinatario (puoi aggiungere altri campi se vuoi)
    const destNome = document.querySelector('.container-dati-destinatario input[placeholder="Inserisci il nome o entità"]')?.value || '';
    const destEmail = document.querySelector('.container-dati-destinatario input[placeholder="Inserisci l\'email"]')?.value || '';
    const destIban = document.querySelector('.container-dati-destinatario input[placeholder="Inserisci l\'IBAN"]')?.value || '';
    const destCitta = document.querySelector('.container-dati-destinatario input[placeholder="Inserisci la città di residenza"]')?.value || '';

    // Invia il bonifico con il PIN
    fetch('/api/transfer/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + accessToken
      },
      credentials: 'include',
      body: JSON.stringify({
        amount: importo,
        description: nota,
        category: categoria,
        clause: clausola,
        pin: pin,
        to_name: destNome,
        to_email: destEmail,
        to_iban: destIban,
        to_city: destCitta
      })
    })
    .then(res => res.json().then(data => ({ status: res.status, data })))
    .then(({ status, data }) => {
      pinLoader.style.display = 'none';
      if (status === 201) {
        hidePinModal();
        showSuccessModal();
      } else {
        pinInput.style.display = '';
        pinConfirmBtn.style.display = '';
        pinCancelBtn.style.display = '';
        pinModalTitle.textContent = 'Transizione iniziata';
        pinModalMessage.textContent = 'Inserisci il PIN per autorizzare il bonifico';
        pinError.textContent = data.detail || Object.values(data).join(' ');
      }
    })
    .catch(() => {
      pinLoader.style.display = 'none';
      pinInput.style.display = '';
      pinConfirmBtn.style.display = '';
      pinCancelBtn.style.display = '';
      pinModalTitle.textContent = 'Transizione iniziata';
      pinModalMessage.textContent = 'Inserisci il PIN per autorizzare il bonifico';
      pinError.textContent = 'Errore di rete.';
    });
  });

  // Gestione click su "Annulla"
  pinCancelBtn.addEventListener('click', function() {
    hidePinModal();
  });

  // Gestione chiusura modale successo
  viewReceiptBtn.addEventListener('click', function() {
    // TODO: implementa visualizzazione ricevuta (redirect o modale)
    hideSuccessModal();
    alert('TODO: Visualizzazione ricevuta transazione!');
  });

  // --- RUBRICA: Mostra modale e carica contatti ---
  if (rubricaBtn) {
    rubricaBtn.addEventListener('click', function() {
      rubricaList.innerHTML = '<div style="padding:1rem;">Caricamento...</div>';
      rubricaModal.style.display = 'flex';
      fetch('/api/accounts/contacts/', {
        headers: { 'Authorization': 'Bearer ' + accessToken },
        credentials: 'include',
      })
        .then(res => res.json())
        .then(data => {
          if (Array.isArray(data) && data.length > 0) {
            rubricaList.innerHTML = '';
            data.forEach(contact => {
              const div = document.createElement('div');
              div.className = 'rubrica-contact-item';
              div.innerHTML = `
                <div class="rubrica-contact-name">${contact.name}</div>
                <div class="rubrica-contact-iban">${contact.iban}</div>
                <div style="font-size:0.95em;color:#666;">${contact.email || ''} ${contact.city ? '• ' + contact.city : ''}</div>
              `;
              div.addEventListener('click', function() {
                // Compila i campi destinatario
                document.querySelector('.container-dati-destinatario input[placeholder="Inserisci il nome o entità"]').value = contact.name || '';
                document.querySelector('.container-dati-destinatario input[placeholder="Inserisci l\'email"]').value = contact.email || '';
                document.querySelector('.container-dati-destinatario input[placeholder="Inserisci l\'IBAN"]').value = contact.iban || '';
                document.querySelector('.container-dati-destinatario input[placeholder="Inserisci la città di residenza"]').value = contact.city || '';
                rubricaModal.style.display = 'none';
              });
              rubricaList.appendChild(div);
            });
          } else {
            rubricaList.innerHTML = '<div style="padding:1rem;">Nessun contatto in rubrica.</div>';
          }
        })
        .catch(() => {
          rubricaList.innerHTML = '<div style="padding:1rem;color:red;">Errore nel caricamento della rubrica.</div>';
        });
    });
  }
  if (rubricaCloseBtn) {
    rubricaCloseBtn.addEventListener('click', function() {
      rubricaModal.style.display = 'none';
    });
  }

  // --- Salva destinatario in rubrica dopo bonifico ---
  if (saveContactBtn) {
    saveContactBtn.addEventListener('click', function() {
      // Prendi dati destinatario dal form
      const destNome = document.querySelector('.container-dati-destinatario input[placeholder="Inserisci il nome o entità"]')?.value || '';
      const destEmail = document.querySelector('.container-dati-destinatario input[placeholder="Inserisci l\'email"]')?.value || '';
      const destIban = document.querySelector('.container-dati-destinatario input[placeholder="Inserisci l\'IBAN"]')?.value || '';
      const destCitta = document.querySelector('.container-dati-destinatario input[placeholder="Inserisci la città di residenza"]')?.value || '';
      if (!destNome || !destIban) {
        alert('Nome e IBAN sono obbligatori per salvare il contatto.');
        return;
      }
      saveContactBtn.disabled = true;
      saveContactBtn.textContent = 'Salvataggio...';
      fetch('/api/accounts/contacts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + accessToken
        },
        credentials: 'include',
        body: JSON.stringify({
          name: destNome,
          email: destEmail,
          iban: destIban,
          city: destCitta
        })
      })
        .then(res => res.json().then(data => ({ status: res.status, data })))
        .then(({ status, data }) => {
          saveContactBtn.disabled = false;
          saveContactBtn.textContent = 'Salva l\'utente in rubrica';
          if (status === 201) {
            alert('Contatto salvato in rubrica!');
            hideSuccessModal();
          } else {
            alert(data.detail || Object.values(data).join(' '));
          }
        })
        .catch(() => {
          saveContactBtn.disabled = false;
          saveContactBtn.textContent = 'Salva l\'utente in rubrica';
          alert('Errore di rete nel salvataggio contatto.');
        });
    });
  }
}

// Al caricamento della pagina, recupera il token e popola i dati mittente e setup modale
document.addEventListener('DOMContentLoaded', function() {
  const accessToken = localStorage.getItem('accessToken');
  if (accessToken) {
    fetchAndPopulateMittente(accessToken);
    setupBonificoFlow(accessToken);
  }
});


