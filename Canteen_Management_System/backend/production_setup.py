#!/usr/bin/env python
import os
import django
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.conf import settings
from menu.models import MenuItem

def setup_production_media():
    """Setup media files for production"""
    
    print("Setting up production media files...")
    
    # Create media directories
    media_root = settings.MEDIA_ROOT
    menu_images_dir = os.path.join(media_root, 'menu_images')
    
    os.makedirs(media_root, exist_ok=True)
    os.makedirs(menu_images_dir, exist_ok=True)
    
    print(f"Media directories created: {media_root}")
    
    # Create placeholder if it doesn't exist
    placeholder_path = os.path.join(menu_images_dir, 'placeholder.jpg')
    if not os.path.exists(placeholder_path):
        from PIL import Image, ImageDraw
        
        img = Image.new('RGB', (400, 300), color='#f0f0f0')
        draw = ImageDraw.Draw(img)
        
        # Simple text
        draw.text((150, 140), "No Image", fill='#666666')
        img.save(placeholder_path, 'JPEG')
        print("Placeholder image created")
    
    # Check existing menu items
    items = MenuItem.objects.all()
    print(f"Found {items.count()} menu items")
    
    for item in items:
        if item.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(item.image))
            if not os.path.exists(image_path):
                print(f"Missing image for {item.name}: {item.image}")
                # Set to placeholder or remove image reference
                item.image = 'menu_images/placeholder.jpg'
                item.save()
                print(f"Updated {item.name} to use placeholder")
    
    print("Production media setup complete!")

if __name__ == "__main__":
    setup_production_media()