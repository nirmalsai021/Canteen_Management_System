#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

def create_base64_placeholder():
    """Create a simple base64 placeholder image"""
    
    # Simple 1x1 transparent PNG in base64
    placeholder_b64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    
    # Create a simple HTML response for missing images
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head><title>Image Not Found</title></head>
    <body style="margin:0;padding:20px;text-align:center;background:#f0f0f0;color:#666;">
        <div style="width:300px;height:200px;display:flex;align-items:center;justify-content:center;border:1px solid #ddd;">
            No Image Available
        </div>
    </body>
    </html>
    '''
    
    # Create media directory
    media_root = settings.MEDIA_ROOT
    menu_images_dir = os.path.join(media_root, 'menu_images')
    os.makedirs(menu_images_dir, exist_ok=True)
    
    # Create a simple text file as placeholder
    placeholder_path = os.path.join(menu_images_dir, 'placeholder.html')
    with open(placeholder_path, 'w') as f:
        f.write(html_content)
    
    print(f"Placeholder created: {placeholder_path}")

if __name__ == "__main__":
    create_base64_placeholder()