#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.conf import settings
from menu.models import MenuItem

print("Media Root:", settings.MEDIA_ROOT)
print("Media URL:", settings.MEDIA_URL)

# Check if media directory exists
if os.path.exists(settings.MEDIA_ROOT):
    print("Media directory exists")
    
    # List all files in media directory
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
            print(f"File: {rel_path}")
else:
    print("Media directory does not exist")

# Check menu items with images
print("\nMenu items with images:")
items = MenuItem.objects.exclude(image='')
for item in items:
    print(f"{item.name}: {item.image}")
    if item.image:
        full_path = os.path.join(settings.MEDIA_ROOT, str(item.image))
        exists = os.path.exists(full_path)
        print(f"  File exists: {exists}")
        if not exists:
            print(f"  Expected path: {full_path}")