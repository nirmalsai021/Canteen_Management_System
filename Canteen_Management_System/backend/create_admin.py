#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import AdminProfile

# Create superuser
username = 'canteen'
email = 'canteen@example.com'
password = 'canteen@321'

if not User.objects.filter(username=username).exists():
    user = User.objects.create_superuser(username=username, email=email, password=password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    
    # Create admin profile
    AdminProfile.objects.get_or_create(user=user)
    
    print(f"✅ Admin user created successfully!")
    print(f"Username: {username}")
    print(f"Password: {password}")
else:
    print("❌ Admin user already exists!")