#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

def fix_media_paths():
    """Fix media file paths in database"""
    from menu.models import MenuItem
    
    print("Fixing media file paths...")
    
    items = MenuItem.objects.all()
    for item in items:
        if item.image:
            # Ensure the image path is correct
            image_path = str(item.image)
            if not image_path.startswith('menu_images/'):
                # Fix the path if needed
                filename = os.path.basename(image_path)
                item.image = f'menu_images/{filename}'
                item.save()
                print(f"Fixed path for {item.name}: {item.image}")
    
    print("Media paths fixed!")

def create_media_dirs():
    """Create media directories if they don't exist"""
    media_root = settings.MEDIA_ROOT
    menu_images_dir = os.path.join(media_root, 'menu_images')
    
    os.makedirs(menu_images_dir, exist_ok=True)
    print(f"Media directories created: {menu_images_dir}")

if __name__ == "__main__":
    create_media_dirs()
    fix_media_paths()
    print("Deployment media fix complete!")