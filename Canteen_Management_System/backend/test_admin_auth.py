#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def test_admin_auth():
    try:
        # Check if admin user exists
        user = User.objects.get(username='canteen')
        print(f"✅ Admin user found: {user.username}")
        print(f"   - is_staff: {user.is_staff}")
        print(f"   - is_superuser: {user.is_superuser}")
        print(f"   - is_active: {user.is_active}")
        
        # Check if token exists
        try:
            token = Token.objects.get(user=user)
            print(f"✅ Token found: {token.key}")
        except Token.DoesNotExist:
            print("❌ No token found for admin user")
            
    except User.DoesNotExist:
        print("❌ Admin user not found")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    test_admin_auth()