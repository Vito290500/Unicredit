/**
 * Esempio di utilizzo delle utility di autenticazione in altre pagine
 * Includi questo script dopo auth-utils.js
 */

document.addEventListener('DOMContentLoaded', function() {
  // Controlla se l'utente è autenticato all'inizio della pagina
  if (!window.authUtils.requireAuth()) {
    return; // L'utente verrà reindirizzato al login
  }

  // Esempio di chiamata API con gestione automatica della scadenza token
  async function fetchUserData() {
    try {
      const { response, data } = await window.authUtils.authFetch('/api/user/profile/');
      
      if (response.ok) {
        console.log('Dati utente:', data);
        // Utilizza i dati...
      } else {
        console.error('Errore nel caricamento dati utente:', data);
      }
    } catch (error) {
      console.error('Errore di rete:', error);
    }
  }

  // Esempio di controllo periodico del token (opzionale)
  function startTokenCheck() {
    // Controlla il token ogni 5 minuti
    setInterval(async () => {
      try {
        const { response } = await window.authUtils.authFetch('/api/auth/verify/');
        if (!response.ok) {
          console.log('Token non più valido, reindirizzamento al login...');
        }
      } catch (error) {
        console.log('Errore nella verifica periodica del token:', error);
      }
    }, 5 * 60 * 1000); // 5 minuti
  }

  // Avvia il controllo periodico (opzionale)
  // startTokenCheck();
});