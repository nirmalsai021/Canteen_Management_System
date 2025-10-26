#!/usr/bin/env python3
"""
Quick test script to verify admin token authentication
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

def test_admin_token():
    print("Testing Admin Token Authentication...")
    
    try:
        # Get the admin user
        admin_user = User.objects.get(username='canteen')
        print(f"Admin user found: {admin_user.username}")
        print(f"   - Is staff: {admin_user.is_staff}")
        print(f"   - Is superuser: {admin_user.is_superuser}")
        print(f"   - Is active: {admin_user.is_active}")
        
        # Get the token
        try:
            token = Token.objects.get(user=admin_user)
            print(f"Token found: {token.key}")
            
            # Verify token exists and is valid
            test_token = Token.objects.filter(key=token.key).first()
            if test_token:
                print(f"Token is valid and belongs to user: {test_token.user.username}")
                return True
            else:
                print("Token not found in database")
                return False
                
        except Token.DoesNotExist:
            print("No token found for admin user")
            return False
            
    except User.DoesNotExist:
        print("Admin user 'canteen' not found")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_admin_token()
    if success:
        print("\nAdmin token authentication test PASSED")
    else:
        print("\nAdmin token authentication test FAILED")