#!/usr/bin/env python
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.core.management import call_command

# Run the menu update command
try:
    call_command('create_default_items')
    print("Menu items updated successfully with unique images")
except Exception as e:
    print(f"Error updating menu items: {e}")
