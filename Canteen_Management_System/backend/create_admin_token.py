#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def create_admin_token():
    try:
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
            print(f"✅ Admin user '{user.username}' created!")
        else:
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            print(f"✅ Admin user '{user.username}' updated!")
        
        # Delete any existing tokens and create new one
        Token.objects.filter(user=user).delete()
        
        # Create token with exact key
        token = Token(user=user, key='admin-token-12345')
        token.save()
        
        print(f"✅ Admin token created: {token.key}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    create_admin_token()