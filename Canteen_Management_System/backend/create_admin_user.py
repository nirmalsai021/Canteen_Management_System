#!/usr/bin/env python
import os
import django
import sys

# Add the project directory to Python path
sys.path.append('/opt/render/project/src/Canteen_Management_System/backend')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    username = 'canteen'
    password = 'canteen@321'
    email = 'admin@canteen.com'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"✅ Admin user '{username}' created successfully!")
    else:
        print(f"ℹ️ Admin user '{username}' already exists")

if __name__ == '__main__':
    create_admin_user()