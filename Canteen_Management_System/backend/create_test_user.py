#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.contrib.auth.models import User

# Create a test user for password reset testing
email = "test@example.com"
username = "testuser"
password = "testpass123"

try:
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': username,
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        user.set_password(password)
        user.save()
        print(f"✅ Test user created: {email}")
    else:
        print(f"✅ Test user already exists: {email}")
        
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    
except Exception as e:
    print(f"❌ Error: {e}")