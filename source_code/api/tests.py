from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()
from accounts.models import BankAccount, Accredito
from transactions.models import Transaction
from datetime import date
import uuid

class APITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create BankAccount with initial balance
        self.bank_account = BankAccount.objects.create(
            user=self.user,
            iban=str(uuid.uuid4()),
            name='Test Account',
            balance=1000.00,
            currency='EUR'
        )

        # Create some transactions and accreditamenti
        Transaction.objects.create(
            account=self.bank_account,
            date=date(2023, 6, 15),
            amount=-200.00,
            description='Test transaction June'
        )
        Transaction.objects.create(
            account=self.bank_account,
            date=date(2023, 7, 10),
            amount=-100.00,
            description='Test transaction July'
        )
        Accredito.objects.create(
            account=self.bank_account,
            date=date(2023, 7, 20),
            amount=300.00,
            description='Test accredito July',
            source='Employer'
        )

    def test_estratto_conto_list(self):
        url = reverse('estratti-conto-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        mesi = [e['mese'] for e in response.data]
        self.assertIn(6, mesi)
        self.assertIn(7, mesi)

    def test_movimenti_mensili(self):
        url_list = reverse('estratti-conto-list')
        response_list = self.client.get(url_list)
        estratti = response_list.data
        estratto_luglio = next((e for e in estratti if e['mese'] == 7), None)
        self.assertIsNotNone(estratto_luglio)

        url_mov = reverse('movimenti-mensili', kwargs={'estratto_id': '00000000-0000-0000-0000-000000000000'})
        response_mov = self.client.get(url_mov)
        self.assertEqual(response_mov.status_code, status.HTTP_404_NOT_FOUND)

    def test_my_account_view(self):
        url = reverse('my-account')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('profile', response.data)

    def test_dashboard_data(self):
        url = reverse('dashboard-data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_bank_account_list(self):
        url = reverse('user-bank-account-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_list(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dashboard_stats(self):
        url = reverse('dashboard-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_entrate_uscite_chart(self):
        url = reverse('entrate-uscite-chart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_categoria_chart(self):
        url = reverse('categoria-chart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_goals_saving_list_create(self):
        url = reverse('goals-saving-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_goals_saving_detail(self):
        # Test detail view with non-existent id
        url = reverse('goals-saving-detail', kwargs={'pk': '00000000-0000-0000-0000-000000000000'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_goals_saving_add_money(self):
        url = reverse('goals-saving-add-money')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


