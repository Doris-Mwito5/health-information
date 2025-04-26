from django.test import TestCase
from health.serializers import ClientSerializer
from health.models import Client
from django.contrib.auth import get_user_model
from datetime import date

class SerializerTests(TestCase):
    def setUp(self):
        User = get_user_model() 
        self.user = User.objects.create_user(username='doctor', password='testpass123')
        self.client_data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'date_of_birth': date(1990, 1, 1),
            'gender': 'M',
            'contact_number': '1234567890',
            'address': '123 Main St',
            'created_by': self.user.id
        }

    def test_client_serializer(self):
        serializer = ClientSerializer(data=self.client_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)  
        client = serializer.save()
        self.assertEqual(client.first_name, 'John')