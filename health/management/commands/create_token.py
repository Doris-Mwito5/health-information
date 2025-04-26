from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Create or update auth token for a user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to create token for')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        try:
            user = User.objects.get(username=username)
            token, created = Token.objects.get_or_create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Token for {username}: {token.key}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} not found'))