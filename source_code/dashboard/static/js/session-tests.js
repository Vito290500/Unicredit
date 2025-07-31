/**
 * Test Suite per la Gestione della Sessione
 * Questo file contiene test per verificare il comportamento della gestione del token
 */

// Simulazione di un token scaduto per test
function simulateExpiredToken() {
  // Salva il token originale
  const originalToken = localStorage.getItem('accessToken');
  
  // Imposta un token fittizio scaduto
  localStorage.setItem('accessToken', 'expired_token_for_testing');
  
  console.log('🧪 TEST: Token scaduto simulato');
  
  // Ripristina il token originale dopo 10 secondi
  setTimeout(() => {
    if (originalToken) {
      localStorage.setItem('accessToken', originalToken);
    } else {
      localStorage.removeItem('accessToken');
    }
    console.log('🔄 Token originale ripristinato');
  }, 10000);
}

// Test della gestione token scaduto
async function testTokenExpiration() {
  console.log('🧪 INIZIO TEST: Gestione Token Scaduto');
  
  try {
    // Simula una chiamata API con token scaduto
    const response = await fetch('/api/goals-saving/', {
      headers: {
        'Authorization': 'Bearer invalid_token_test',
        'Content-Type': 'application/json'
      }
    });
    
    console.log('📊 Risposta del server:', {
      status: response.status,
      statusText: response.statusText,
      ok: response.ok
    });
    
    if (response.status === 401) {
      console.log('✅ TEST PASSATO: Il server restituisce 401 per token non valido');
      return true;
    } else {
      console.log('❌ TEST FALLITO: Il server non restituisce 401 per token non valido');
      return false;
    }
    
  } catch (error) {
    console.error('❌ ERRORE NEL TEST:', error);
    return false;
  }
}

// Test della funzione authFetch
async function testAuthFetch() {
  console.log('🧪 INIZIO TEST: Funzione authFetch');
  
  if (!window.authUtils) {
    console.error('❌ authUtils non disponibile');
    return false;
  }
  
  try {
    // Test con token valido (se presente)
    const { response, data } = await window.authUtils.authFetch('/api/goals-saving/');
    
    console.log('📊 Risultato authFetch:', {
      status: response.status,
      ok: response.ok,
      hasData: !!data
    });
    
    if (response.status === 401) {
      console.log('⚠️  Token scaduto rilevato da authFetch');
      return true; // È normale se il token è scaduto
    } else if (response.ok) {
      console.log('✅ TEST PASSATO: authFetch funziona correttamente');
      return true;
    } else {
      console.log('❌ TEST FALLITO: authFetch ha restituito errore inaspettato');
      return false;
    }
    
  } catch (error) {
    console.error('❌ ERRORE NEL TEST authFetch:', error);
    return false;
  }
}

// Test del controllo di autenticazione
function testAuthCheck() {
  console.log('🧪 INIZIO TEST: Controllo Autenticazione');
  
  if (!window.authUtils) {
    console.error('❌ authUtils non disponibile');
    return false;
  }
  
  const hasToken = !!window.authUtils.getAccessToken();
  const isAuth = window.authUtils.isAuthenticated();
  
  console.log('📊 Stato autenticazione:', {
    hasToken,
    isAuthenticated: isAuth,
    tokenLength: hasToken ? window.authUtils.getAccessToken().length : 0
  });
  
  if (hasToken === isAuth) {
    console.log('✅ TEST PASSATO: Controllo autenticazione coerente');
    return true;
  } else {
    console.log('❌ TEST FALLITO: Controllo autenticazione incoerente');
    return false;
  }
}

// Esegui tutti i test
async function runAllTests() {
  console.log('🚀 INIZIO SUITE DI TEST PER GESTIONE SESSIONE');
  console.log('================================================');
  
  const results = {
    authCheck: testAuthCheck(),
    tokenExpiration: await testTokenExpiration(),
    authFetch: await testAuthFetch()
  };
  
  console.log('================================================');
  console.log('📋 RISULTATI DEI TEST:');
  console.log('- Controllo Autenticazione:', results.authCheck ? '✅ PASSATO' : '❌ FALLITO');
  console.log('- Gestione Token Scaduto:', results.tokenExpiration ? '✅ PASSATO' : '❌ FALLITO');
  console.log('- Funzione authFetch:', results.authFetch ? '✅ PASSATO' : '❌ FALLITO');
  
  const allPassed = Object.values(results).every(result => result);
  console.log('================================================');
  console.log('🎯 RISULTATO FINALE:', allPassed ? '✅ TUTTI I TEST PASSATI' : '❌ ALCUNI TEST FALLITI');
  
  return results;
}

// Test manuale per simulare scadenza token
function manualTokenExpirationTest() {
  console.log('🧪 TEST MANUALE: Simulazione Scadenza Token');
  console.log('Questo test simula un token scaduto per 10 secondi');
  console.log('Durante questo periodo, tutte le chiamate API dovrebbero reindirizzare al login');
  
  simulateExpiredToken();
  
  // Prova a fare una chiamata API dopo 2 secondi
  setTimeout(async () => {
    console.log('🔄 Tentativo di chiamata API con token scaduto...');
    try {
      const { response } = await window.authUtils.authFetch('/api/goals-saving/');
      console.log('📊 Risposta:', response.status);
    } catch (error) {
      console.log('❌ Errore:', error.message);
    }
  }, 2000);
}

// Esporta le funzioni di test
window.sessionTests = {
  runAllTests,
  testTokenExpiration,
  testAuthFetch,
  testAuthCheck,
  simulateExpiredToken,
  manualTokenExpirationTest
};

// Messaggio di istruzioni
console.log('🧪 TEST SESSIONE CARICATI');
console.log('Usa i seguenti comandi nella console:');
console.log('- sessionTests.runAllTests() - Esegue tutti i test');
console.log('- sessionTests.manualTokenExpirationTest() - Test manuale scadenza token');
console.log('- sessionTests.simulateExpiredToken() - Simula token scaduto per 10 secondi');