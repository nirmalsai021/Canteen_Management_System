#!/usr/bin/env python
"""
Deployment fix script for admin authentication
This script should be run after deployment to fix admin auth
"""
import os
import sys
import django

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def main():
    print("Starting admin authentication fix...")
    
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
        
        if created:
            user.set_password('canteen@321')
            user.save()
            print("✓ Admin user created")
        else:
            # Ensure admin privileges
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            print("✓ Admin user updated")
        
        # Create admin profile
        try:
            from users.models import AdminProfile
            AdminProfile.objects.get_or_create(user=user)
            print("✓ Admin profile created")
        except:
            print("! Admin profile creation skipped (model not available)")
        
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
        
        print(f"✓ Admin token ready: {token.key}")
        print("✓ Admin authentication fixed successfully!")
        
        return True
        
    except Exception as e:
        print(f"✗ Error fixing admin auth: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)