#!/usr/bin/env python3
"""
Final fix for admin authentication issues
"""
import os
import django
import sys

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def fix_admin_auth():
    print("Fixing admin authentication...")
    
    try:
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
        
        # Set password
        user.set_password('canteen@321')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        
        # Get or create token
        token, token_created = Token.objects.get_or_create(user=user)
        
        print(f"Admin user: {user.username}")
        print(f"User created: {created}")
        print(f"Token: {token.key}")
        print(f"Token created: {token_created}")
        
        # Test the login endpoint
        import json
        from django.test import Client
        
        client = Client()
        response = client.post(
            '/api/users/simple-admin-login/',
            data=json.dumps({
                'username': 'canteen',
                'password': 'canteen@321'
            }),
            content_type='application/json'
        )
        
        print(f"Login test status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Login response token: {data.get('token', 'NO TOKEN')}")
            print("Login endpoint working correctly!")
        else:
            print(f"Login test failed: {response.content}")
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = fix_admin_auth()
    if success:
        print("\nAdmin authentication fix completed successfully!")
    else:
        print("\nAdmin authentication fix failed!")