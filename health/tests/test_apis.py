from datetime import date
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from health.models import HealthProgram, Client
from django.contrib.auth import get_user_model


class ClientAPITests(APITestCase):
    def setUp(self):
        User = get_user_model()  
        self.user = User.objects.create_user(username='doctor', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.program = HealthProgram.objects.create(
            name="HIV Program",
            created_by=self.user
        )
        
        self.sample_client = Client.objects.create(
            first_name="Test",
            last_name="Client",
            date_of_birth=date(1990, 1, 1),
            gender='M',
            contact_number='1234567890',
            address="123 Health Street",
            created_by=self.user,
        )

    def test_create_program(self):
        url = reverse('healthprogram-list')
        data = {
            'name': 'TB Program', 
            'description': 'TB treatment program',
            'created_by': self.user.id  
    }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HealthProgram.objects.count(), 2)

    def test_client_search(self):
        url = reverse('client-list') + '?search=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)