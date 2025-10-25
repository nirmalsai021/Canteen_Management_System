#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create admin user and token
user, _ = User.objects.get_or_create(
    username='canteen',
    defaults={'email': 'canteen@example.com', 'is_staff': True, 'is_superuser': True}
)
user.is_staff = True
user.is_superuser = True
user.save()

# Create the exact token the frontend expects
Token.objects.filter(key='admin-token-12345').delete()
Token.objects.create(user=user, key='admin-token-12345')
print("✅ Fixed! Admin token created: admin-token-12345")