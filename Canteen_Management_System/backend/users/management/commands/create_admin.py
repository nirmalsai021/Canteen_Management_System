from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Create admin user and token'

    def handle(self, *args, **options):
        # Create or get admin user
        user, created = User.objects.get_or_create(
            username='canteen',
            defaults={
                'email': 'admin@canteen.com',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        
        if created:
            user.set_password('canteen@321')
            user.save()
            self.stdout.write('✅ Admin user created')
        else:
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.set_password('canteen@321')
            user.save()
            self.stdout.write('✅ Admin user updated')
        
        # Delete existing token and create new one
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user, key='admin-token-12345')
        
        self.stdout.write(f'✅ Token created: {token.key}')
        self.stdout.write('✅ Admin setup complete!')