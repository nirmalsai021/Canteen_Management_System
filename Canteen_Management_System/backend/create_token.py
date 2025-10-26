#!/usr/bin/env python
import os
import django
import sys

# Add the project directory to Python path
sys.path.append('/opt/render/project/src/Canteen_Management_System/backend')

# Set Django settings
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
        
        # Set password
        user.set_password('canteen@321')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        # Delete existing token and create specific one
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user, key='admin-token-12345')
        
        print(f"✅ Admin user created: {user.username}")
        print(f"✅ Token created: {token.key}")
        print("✅ Admin setup complete!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    create_admin_token()