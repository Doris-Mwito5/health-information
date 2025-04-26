from datetime import date
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from health.views import ClientViewSet
from health.models import Client

class ViewTests(TestCase):
    def setUp(self):
        User = get_user_model() 
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='doctor', password='testpass123')
        self.client = Client.objects.create(
            first_name="Jane",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            gender='M',
            contact_number='1234567890',
            address="123 Health Street",
            created_by=self.user
        )

    def test_client_list_view(self):
        request = self.factory.get('/clients/')
        request.user = self.user
        view = ClientViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)