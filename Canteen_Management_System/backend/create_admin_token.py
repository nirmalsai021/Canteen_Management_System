#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from users.models import AdminProfile

# Create or get admin user
username = 'canteen'
email = 'canteen@example.com'
password = 'canteen@321'

# Create or get the admin user
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
    print(f"✅ Admin user created!")
else:
    # Ensure existing user has admin privileges
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    print(f"✅ Admin user updated!")

# Create admin profile
AdminProfile.objects.get_or_create(user=user)

# Create or get token
token, token_created = Token.objects.get_or_create(user=user)

print(f"Username: {username}")
print(f"Password: {password}")
print(f"Token: {token.key}")

# For the hardcoded admin system, let's also create a specific token
# Delete any existing token with the hardcoded key and create a new one
try:
    # Try to find if there's already a token with our hardcoded key
    existing_token = Token.objects.filter(key='admin-token-12345').first()
    if existing_token and existing_token.user != user:
        existing_token.delete()
    
    # Create the hardcoded token for our admin user
    hardcoded_token, _ = Token.objects.get_or_create(
        user=user,
        defaults={'key': 'admin-token-12345'}
    )
    
    if hardcoded_token.key != 'admin-token-12345':
        # If token exists but with different key, update it
        hardcoded_token.key = 'admin-token-12345'
        hardcoded_token.save()
    
    print(f"✅ Hardcoded admin token created: admin-token-12345")
    
except Exception as e:
    print(f"⚠️ Could not create hardcoded token: {e}")
    print(f"Using regular token: {token.key}")