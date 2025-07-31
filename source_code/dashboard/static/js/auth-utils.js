/**
 * Utility per la gestione dell'autenticazione e scadenza token
 */

// --- GESTIONE SCADENZA TOKEN ---
function handleTokenExpiration() {
  // Rimuovi i token dal localStorage
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  
  // Mostra un messaggio all'utente
  alert('La tua sessione è scaduta. Verrai reindirizzato al login.');
  
  // Reindirizza al login
  window.location.href = '/';
}

function isTokenExpired(response) {
  // Controlla se la risposta indica un token scaduto o non autorizzato
  return response.status === 401;
}

function getAccessToken() {
  return localStorage.getItem('accessToken');
}

function getRefreshToken() {
  return localStorage.getItem('refreshToken');
}

// Funzione fetch con gestione automatica della scadenza token
async function authFetch(url, options = {}) {
  const accessToken = getAccessToken();
  
  if (!accessToken) {
    handleTokenExpiration();
    return { response: { ok: false, status: 401 }, data: { detail: 'Token mancante' } };
  }

  const headers = {
    ...(options.headers || {}),
    'Authorization': 'Bearer ' + accessToken,
    'Content-Type': 'application/json'
  };
  
  const response = await fetch(url, {
    ...options,
    credentials: 'include',
    headers
  });

  // Controlla se il token è scaduto
  if (isTokenExpired(response)) {
    handleTokenExpiration();
    return { response, data: { detail: 'Token scaduto' } };
  }

  // Gestione del parsing della risposta
  let data = null;
  if (response.status !== 204) {
    try {
      const text = await response.text();
      data = text ? JSON.parse(text) : null;
    } catch {
      data = null;
    }
  }

  return { response, data };
}

// Verifica se l'utente è autenticato
function isAuthenticated() {
  return !!getAccessToken();
}

// Controllo iniziale dell'autenticazione per le pagine protette
function requireAuth() {
  if (!isAuthenticated()) {
    handleTokenExpiration();
    return false;
  }
  return true;
}

// Esporta le funzioni per l'uso globale
window.authUtils = {
  handleTokenExpiration,
  isTokenExpired,
  getAccessToken,
  getRefreshToken,
  authFetch,
  isAuthenticated,
  requireAuth
};