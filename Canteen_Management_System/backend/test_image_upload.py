#!/usr/bin/env python
import os
import django
from PIL import Image

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.conf import settings
from menu.models import MenuItem
from django.core.files.uploadedfile import SimpleUploadedFile

def create_test_images():
    """Create test images and menu items"""
    
    print("Creating test images and menu items...")
    
    # Create test images
    menu_images_dir = os.path.join(settings.MEDIA_ROOT, 'menu_images')
    os.makedirs(menu_images_dir, exist_ok=True)
    
    test_items = [
        {'name': 'Burger', 'price': 150, 'category': 'lunch', 'color': '#ff6b6b'},
        {'name': 'Pizza', 'price': 200, 'category': 'lunch', 'color': '#4ecdc4'},
        {'name': 'Coffee', 'price': 50, 'category': 'drinks', 'color': '#45b7d1'},
        {'name': 'Sandwich', 'price': 80, 'category': 'snacks', 'color': '#96ceb4'},
    ]
    
    for item_data in test_items:
        # Create test image
        img = Image.new('RGB', (300, 200), color=item_data['color'])
        image_path = os.path.join(menu_images_dir, f"{item_data['name'].lower()}.jpg")
        img.save(image_path, 'JPEG')
        
        # Create menu item
        menu_item, created = MenuItem.objects.get_or_create(
            name=item_data['name'],
            defaults={
                'price': item_data['price'],
                'category': item_data['category'],
                'description': f"Delicious {item_data['name']}",
                'available': True,
                'image': f"menu_images/{item_data['name'].lower()}.jpg"
            }
        )
        
        if created:
            print(f"Created: {menu_item.name} with image {menu_item.image}")
        else:
            print(f"Already exists: {menu_item.name}")
    
    print(f"Total menu items: {MenuItem.objects.count()}")

if __name__ == "__main__":
    create_test_images()