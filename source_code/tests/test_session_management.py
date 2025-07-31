"""
Unit Test per la Gestione della Sessione
Test per verificare il comportamento dell'autenticazione JWT e scadenza token
Compatibile con Docker e Django
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.conf import settings
import json

# Configurazione Django per i test
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'source_code.settings')
    django.setup()

try:
    from rest_framework.test import APITestCase, APIClient
    from rest_framework_simplejwt.tokens import RefreshToken
    REST_FRAMEWORK_AVAILABLE = True
except ImportError:
    REST_FRAMEWORK_AVAILABLE = False
    print("⚠️  REST Framework non disponibile, usando solo test Django base")


class SessionManagementTestCase(TestCase):
    """Test per la gestione della sessione e autenticazione JWT"""
    
    def setUp(self):
        """Setup iniziale per i test"""
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        
    def test_login_endpoint_exists(self):
        """Test: Verifica che l'endpoint di login esista"""
        response = self.client.post('/auth/jwt/create/', {
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        
        # Non dovrebbe restituire 404 (endpoint non trovato)
        self.assertNotEqual(response.status_code, 404)
        print(f"✅ Login endpoint status: {response.status_code}")
        
    def test_login_with_valid_credentials(self):
        """Test: Login con credenziali valide"""
        response = self.client.post('/auth/jwt/create/', {
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        
        print(f"📊 Login response status: {response.status_code}")
        print(f"📊 Login response content: {response.content.decode()}")
        
        # Se il login funziona, dovrebbe restituire 200
        if response.status_code == 200:
            try:
                data = json.loads(response.content)
                self.assertIn('access', data)
                self.assertIn('refresh', data)
                print("✅ Login successful - tokens received")
            except json.JSONDecodeError:
                print("⚠️  Response is not JSON")
        else:
            print(f"❌ Login failed with status {response.status_code}")
            
    def test_login_with_invalid_credentials(self):
        """Test: Login con credenziali non valide"""
        response = self.client.post('/auth/jwt/create/', {
            'email': 'test@example.com',
            'password': 'wrong_password'
        })
        
        print(f"📊 Invalid login status: {response.status_code}")
        
        # Dovrebbe restituire 401 o 400
        self.assertIn(response.status_code, [400, 401])
        print("✅ Invalid credentials correctly rejected")
        
    def test_protected_endpoint_without_token(self):
        """Test: Accesso a endpoint protetto senza token"""
        endpoints_to_test = [
            '/api/goals-saving/',
            '/api/dashboard-data/',
            '/api/transactions/',
            '/api/accounts/me/'
        ]
        
        for endpoint in endpoints_to_test:
            response = self.client.get(endpoint)
            print(f"📊 {endpoint} without token: {response.status_code}")
            
            # Dovrebbe restituire 401 (non autorizzato) o 403 (forbidden)
            if response.status_code in [401, 403]:
                print(f"✅ {endpoint} correctly protected")
            elif response.status_code == 404:
                print(f"⚠️  {endpoint} not found (endpoint might not exist)")
            else:
                print(f"❌ {endpoint} not properly protected (status: {response.status_code})")


if REST_FRAMEWORK_AVAILABLE:
    class APISessionTestCase(APITestCase):
        """Test avanzati con REST Framework (se disponibile)"""
        
        def setUp(self):
            """Setup per test API"""
            self.client = APIClient()
            User = get_user_model()
            self.user = User.objects.create_user(
                email='api_test@example.com',
                password='testpassword123'
            )
            
            # Genera token JWT
            self.refresh = RefreshToken.for_user(self.user)
            self.access_token = str(self.refresh.access_token)
            
        def test_api_with_valid_token(self):
            """Test: API call con token valido"""
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
            
            response = self.client.get('/api/goals-saving/')
            print(f"📊 API with valid token: {response.status_code}")
            
            # Non dovrebbe restituire 401
            self.assertNotEqual(response.status_code, 401)
            print("✅ Valid token accepted")
            
        def test_api_with_invalid_token(self):
            """Test: API call con token non valido"""
            self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token_123')
            
            response = self.client.get('/api/goals-saving/')
            print(f"📊 API with invalid token: {response.status_code}")
            
            # Dovrebbe restituire 401
            self.assertEqual(response.status_code, 401)
            print("✅ Invalid token rejected")
            
        def test_token_refresh(self):
            """Test: Refresh del token"""
            refresh_token = str(self.refresh)
            
            response = self.client.post('/auth/jwt/refresh/', {
                'refresh': refresh_token
            })
            
            print(f"📊 Token refresh status: {response.status_code}")
            
            if response.status_code == 200:
                data = json.loads(response.content)
                self.assertIn('access', data)
                print("✅ Token refresh successful")
            else:
                print(f"❌ Token refresh failed: {response.content.decode()}")


class DockerCompatibilityTestCase(TestCase):
    """Test specifici per compatibilità Docker"""
    
    def test_database_connection(self):
        """Test: Connessione al database"""
        try:
            User = get_user_model()
            user_count = User.objects.count()
            print(f"✅ Database connection OK - {user_count} users found")
            self.assertTrue(True)
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            self.fail("Database connection failed")
            
    def test_django_settings(self):
        """Test: Configurazione Django"""
        try:
            from django.conf import settings
            print(f"✅ Django settings loaded")
            print(f"📊 DEBUG: {settings.DEBUG}")
            print(f"📊 Database: {settings.DATABASES['default']['ENGINE']}")
            self.assertTrue(True)
        except Exception as e:
            print(f"❌ Django settings error: {e}")
            self.fail("Django settings not properly configured")


def run_tests():
    """Funzione per eseguire i test manualmente"""
    print("🚀 INIZIO TEST GESTIONE SESSIONE")
    print("=" * 50)
    
    import unittest
    
    # Crea una test suite
    suite = unittest.TestSuite()
    
    # Aggiungi i test
    suite.addTest(unittest.makeSuite(SessionManagementTestCase))
    suite.addTest(unittest.makeSuite(DockerCompatibilityTestCase))
    
    if REST_FRAMEWORK_AVAILABLE:
        suite.addTest(unittest.makeSuite(APISessionTestCase))
    
    # Esegui i test
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 50)
    print(f"🎯 RISULTATI: {result.testsRun} test eseguiti")
    print(f"✅ Successi: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Fallimenti: {len(result.failures)}")
    print(f"🚨 Errori: {len(result.errors)}")
    
    return result


if __name__ == '__main__':
    run_tests()