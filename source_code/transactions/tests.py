from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from accounts.models import BankAccount
from transactions.models import Transaction

class TransferTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user1@example.com', password='testpass')
        self.user2 = User.objects.create_user(email='user2@example.com', password='testpass')
        self.account1 = BankAccount.objects.create(user=self.user, iban='IT0000000000000000000001', name='Conto 1', balance=1000)
        self.account2 = BankAccount.objects.create(user=self.user, iban='IT0000000000000000000002', name='Conto 2', balance=500)
        self.account3 = BankAccount.objects.create(user=self.user2, iban='IT0000000000000000000003', name='Conto 3', balance=300)
        self.client = APIClient()
        self.url = reverse('transfer')

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def test_transfer_success(self):
        self.authenticate()
        data = {
            'from_account': str(self.account1.id),
            'to_account': str(self.account2.id),
            'amount': 200,
            'description': 'Test bonifico'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.account1.refresh_from_db()
        self.account2.refresh_from_db()
        self.assertEqual(float(self.account1.balance), 800)
        self.assertEqual(float(self.account2.balance), 700)
        self.assertEqual(Transaction.objects.filter(account=self.account1).count(), 1)
        self.assertEqual(Transaction.objects.filter(account=self.account2).count(), 1)

    def test_transfer_insufficient_funds(self):
        self.authenticate()
        data = {
            'from_account': str(self.account2.id),
            'to_account': str(self.account1.id),
            'amount': 1000,
            'description': 'Saldo insufficiente'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Saldo insufficiente', str(response.data))

    def test_transfer_from_other_user_account(self):
        self.authenticate()
        data = {
            'from_account': str(self.account3.id),
            'to_account': str(self.account1.id),
            'amount': 50,
            'description': 'Non autorizzato'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('Non puoi disporre bonifici', str(response.data)) 