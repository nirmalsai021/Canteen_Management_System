#!/usr/bin/env python
import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.conf import settings
from menu.models import MenuItem

# Create static images directory
static_images_dir = os.path.join(settings.STATIC_ROOT or 'staticfiles', 'images')
os.makedirs(static_images_dir, exist_ok=True)

print(f"Copying images to: {static_images_dir}")

# Copy all media images to static folder
media_images_dir = os.path.join(settings.MEDIA_ROOT, 'menu_images')
if os.path.exists(media_images_dir):
    for filename in os.listdir(media_images_dir):
        src = os.path.join(media_images_dir, filename)
        dst = os.path.join(static_images_dir, filename)
        
        if os.path.isfile(src):
            shutil.copy2(src, dst)
            print(f"Copied: {filename}")

# Update menu items to use static URLs
for item in MenuItem.objects.exclude(image=''):
    if item.image and 'menu_images/' in str(item.image):
        filename = os.path.basename(str(item.image))
        new_path = f'images/{filename}'
        
        # Update the database record
        item.image = new_path
        item.save()
        print(f"Updated {item.name}: {new_path}")

print("Done! Images copied to static folder and database updated.")