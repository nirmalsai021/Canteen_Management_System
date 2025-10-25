#!/usr/bin/env python
import os
import django
from PIL import Image
import io

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.conf import settings
from menu.models import MenuItem
from django.core.files.base import ContentFile

def create_and_upload_images():
    """Create images and upload them properly"""
    
    # Get all menu items
    items = MenuItem.objects.all()
    
    for item in items:
        if item.image and not item.image.name.startswith('http'):
            # Create a simple image
            colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57']
            color = colors[item.id % len(colors)]
            
            # Create image
            img = Image.new('RGB', (400, 300), color=color)
            
            # Save to BytesIO
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG', quality=85)
            img_io.seek(0)
            
            # Create filename
            filename = f"{item.name.lower().replace(' ', '_')}.jpg"
            
            # Save to model
            item.image.save(
                filename,
                ContentFile(img_io.getvalue()),
                save=True
            )
            
            print(f"Created and saved image for: {item.name}")

if __name__ == "__main__":
    create_and_upload_images()
    print("All images created and uploaded!")