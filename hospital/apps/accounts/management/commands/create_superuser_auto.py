import os
from django.core.management.base import BaseCommand
from hospital.apps.accounts.models import User

class Command(BaseCommand):
    help = 'Create superuser automatically from environment variables'

    def handle(self, *args, **kwargs):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@hospital.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')

        if not password:
            self.stdout.write('DJANGO_SUPERUSER_PASSWORD not set, skipping.')
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'Superuser {username} already exists, skipping.')
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role='admin'
        )
        self.stdout.write(f'Superuser {username} created successfully.')