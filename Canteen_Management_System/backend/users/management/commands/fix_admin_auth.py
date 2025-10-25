from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from users.models import AdminProfile

class Command(BaseCommand):
    help = 'Fix admin authentication by creating proper admin user and token'

    def handle(self, *args, **options):
        self.stdout.write('Fixing admin authentication...')
        
        # Create or get admin user
        user, created = User.objects.get_or_create(
            username='canteen',
            defaults={
                'email': 'canteen@example.com',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        
        if created:
            user.set_password('canteen@321')
            user.save()
            self.stdout.write(self.style.SUCCESS('Admin user created'))
        else:
            # Ensure admin privileges
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            self.stdout.write(self.style.SUCCESS('Admin user updated'))
        
        # Create admin profile
        AdminProfile.objects.get_or_create(user=user)
        
        # Delete existing hardcoded token if it exists for different user
        Token.objects.filter(key='admin-token-12345').exclude(user=user).delete()
        
        # Create the hardcoded token for admin user
        token, token_created = Token.objects.get_or_create(
            user=user,
            defaults={'key': 'admin-token-12345'}
        )
        
        # Ensure the token has the correct key
        if token.key != 'admin-token-12345':
            token.delete()
            token = Token.objects.create(user=user, key='admin-token-12345')
        
        self.stdout.write(self.style.SUCCESS(f'Admin token ready: {token.key}'))
        self.stdout.write(self.style.SUCCESS('Admin authentication fixed!'))