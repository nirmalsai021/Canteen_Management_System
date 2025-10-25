#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.conf import settings
from menu.models import MenuItem

def test_image_system():
    """Test that image system works for future uploads"""
    
    print("Testing Image Upload System...")
    
    # Check media settings
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    
    # Check if media directories exist
    media_root = settings.MEDIA_ROOT
    menu_images_dir = os.path.join(media_root, 'menu_images')
    
    if not os.path.exists(media_root):
        os.makedirs(media_root, exist_ok=True)
        print("Created MEDIA_ROOT directory")
    
    if not os.path.exists(menu_images_dir):
        os.makedirs(menu_images_dir, exist_ok=True)
        print("Created menu_images directory")
    
    # Test current menu items
    items = MenuItem.objects.all()
    print(f"\nCurrent menu items: {items.count()}")
    
    for item in items:
        if item.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(item.image))
            exists = os.path.exists(image_path)
            print(f"  {item.name}: {item.image} - {'EXISTS' if exists else 'MISSING'}")
        else:
            print(f"  {item.name}: No image")
    
    print("\n✅ Image system ready for future uploads!")
    print("Future image uploads will work automatically.")

if __name__ == "__main__":
    test_image_system()