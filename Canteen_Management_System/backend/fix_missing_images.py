#!/usr/bin/env python
import os
import django
from PIL import Image, ImageDraw, ImageFont

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.conf import settings
from menu.models import MenuItem

def create_missing_images():
    """Create missing images for menu items"""
    
    media_root = settings.MEDIA_ROOT
    menu_images_dir = os.path.join(media_root, 'menu_images')
    os.makedirs(menu_images_dir, exist_ok=True)
    
    # Get all menu items with images
    items = MenuItem.objects.exclude(image='').exclude(image__isnull=True)
    
    for item in items:
        if item.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(item.image))
            
            if not os.path.exists(image_path):
                print(f"Creating missing image for: {item.name}")
                
                # Create a simple colored image
                colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3']
                color = colors[item.id % len(colors)]
                
                img = Image.new('RGB', (400, 300), color=color)
                draw = ImageDraw.Draw(img)
                
                # Add item name
                try:
                    font = ImageFont.truetype("arial.ttf", 24)
                except:
                    font = ImageFont.load_default()
                
                # Calculate text position
                bbox = draw.textbbox((0, 0), item.name, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                x = (400 - text_width) // 2
                y = (300 - text_height) // 2
                
                draw.text((x, y), item.name, fill='white', font=font)
                
                # Save image
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                img.save(image_path, 'JPEG')
                print(f"Created: {image_path}")

if __name__ == "__main__":
    create_missing_images()
    print("Missing images created!")