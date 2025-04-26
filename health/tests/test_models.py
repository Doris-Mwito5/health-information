from datetime import date
from django.test import TestCase
from health.models import HealthProgram, Client, ClientEnrollment
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='doctor', password='testpass123')
        self.program = HealthProgram.objects.create(
            name="Malaria Prevention",
            created_by=self.user
        )
        self.client = Client.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            gender='M',
            contact_number='1234567890',
            address="123 Health Street",
            created_by=self.user
        )

    def test_program_creation(self):
        self.assertEqual(self.program.name, "Malaria Prevention")
        self.assertEqual(str(self.program), "Malaria Prevention")

    def test_client_enrollment(self):
        enrollment = ClientEnrollment.objects.create(
            client=self.client,
            program=self.program
        )
        self.assertEqual(enrollment.client, self.client)
        self.assertEqual(enrollment.program, self.program)