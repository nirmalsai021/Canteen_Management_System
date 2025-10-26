#!/usr/bin/env python
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def create_admin_user():
    username = 'canteen'
    password = 'canteen@321'
    email = 'admin@canteen.com'
    
    try:
        # Create or get admin user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        
        if created:
            user.set_password(password)
            user.save()
            print(f"✅ Admin user '{username}' created successfully!")
        else:
            # Update existing user to ensure it's admin
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.set_password(password)
            user.save()
            print(f"✅ Admin user '{username}' updated successfully!")
        
        # Create or get token for admin user
        token, token_created = Token.objects.get_or_create(user=user)
        print(f"✅ Admin token: {token.key}")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")

if __name__ == '__main__':
    create_admin_user()