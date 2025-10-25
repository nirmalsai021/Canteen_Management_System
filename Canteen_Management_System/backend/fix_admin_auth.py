#!/usr/bin/env python
"""
Quick fix for admin authentication in production
Run this script on the production server to create proper admin token
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def fix_admin_auth():
    print("🔧 Fixing admin authentication...")
    
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
        print("✅ Admin user created")
    else:
        # Ensure admin privileges
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        print("✅ Admin user updated")
    
    # Delete existing hardcoded token if it exists for different user
    Token.objects.filter(key='admin-token-12345').exclude(user=user).delete()
    
    # Create the hardcoded token for admin user
    token, token_created = Token.objects.get_or_create(
        user=user,
        defaults={'key': 'admin-token-12345'}
    )
    
    # Ensure the token has the correct key
    if token.key != 'admin-token-12345':
        token.key = 'admin-token-12345'
        token.save()
    
    print(f"✅ Admin token ready: {token.key}")
    print("✅ Admin authentication fixed!")
    
    return True

if __name__ == "__main__":
    try:
        fix_admin_auth()
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)