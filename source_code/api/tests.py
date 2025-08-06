from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from accounts.models import BankAccount, Card, GoalsSaving
from transactions.models import Category, Transaction
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date

User = get_user_model()

class BaseAPITestCase(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Create a bank account for the user
        self.bank_account = BankAccount.objects.create(user=self.user, iban='IT60X0542811101000000123456', balance=1000)

        # Create a card linked to the bank account
        self.card = Card.objects.create(
            account=self.bank_account,
            circuit=Card.Circuit.VISA,
            pan_last4='3456',
            pan_hash='dummyhash',
            pan_real='1234567890123456',
            expiry_month=12,
            expiry_year=2030,
            cvv_hash='dummycvvhash',
            cvv_real='123',
            holder_name='Test User',
            active=True
        )

        # Create a category
        self.category = Category.objects.create(name='Test Category')

        # Create a transaction
        self.transaction = Transaction.objects.create(
            account=self.bank_account,
            amount=100,
            category=self.category,
            date=date.today()
        )

        # Create a saving goal
        self.goal = GoalsSaving.objects.create(
            bank_account=self.bank_account,
            nome='Test Goal',
            importo_target=500,
            importo_attuale=100
        )

class DashboardDataAPIViewTest(BaseAPITestCase):
    def test_get_dashboard_data(self):
        url = reverse('dashboard-data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_full_name', response.data)
        self.assertIn('last_login', response.data)
        self.assertIn('account', response.data)
        self.assertIn('card', response.data)

class UserBankAccountListViewTest(BaseAPITestCase):
    def test_get_user_bank_accounts(self):
        url = reverse('user-accounts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

class CategoryListViewTest(BaseAPITestCase):
    def test_get_categories(self):
        url = reverse('categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

class DashboardStatsViewTest(BaseAPITestCase):
    def test_get_dashboard_stats(self):
        url = reverse('dashboard-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('bonifici_inviati', response.data)
        self.assertIn('bonifici_ricevuti', response.data)
        self.assertIn('transazioni', response.data)
        self.assertIn('categorie', response.data)

class EntrateUsciteChartViewTest(BaseAPITestCase):
    def test_get_entrate_uscite_chart(self):
        url = reverse('entrate-uscite-chart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('current_month', response.data)
        self.assertIn('previous_month', response.data)

class CategoriaChartViewTest(BaseAPITestCase):
    def test_get_categoria_chart(self):
        url = reverse('categoria-chart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

class GoalsSavingListCreateViewTest(BaseAPITestCase):
    def test_get_goals_saving(self):
        url = reverse('goals-saving-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check 'results' key for paginated response
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)

    def test_create_goal_saving(self):
        url = reverse('goals-saving-list-create')
        data = {
            'nome': 'New Goal',
            'importo_target': 1000,
            'colore': '#3498db',
            'attivo': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nome'], 'New Goal')

class GoalsSavingDetailViewTest(BaseAPITestCase):
    def test_get_goal_detail(self):
        url = reverse('goals-saving-detail', kwargs={'pk': self.goal.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], self.goal.nome)

    def test_update_goal(self):
        url = reverse('goals-saving-detail', kwargs={'pk': self.goal.id})
        data = {'nome': 'Updated Goal'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Updated Goal')

    def test_delete_goal(self):
        url = reverse('goals-saving-detail', kwargs={'pk': self.goal.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class GoalsSavingAddMoneyViewTest(BaseAPITestCase):
    def test_add_money_to_goal(self):
        url = reverse('goals-saving-add-money', kwargs={'pk': self.goal.id})
        data = {'importo': 50, 'descrizione': 'Test deposit'}
        response = self.client.post(url, data, format='json')
        # The view returns 201 Created, update test to expect 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.importo_attuale, 150)

