# Generated manually to fix corrupted image URLs

from django.db import migrations
import urllib.parse

def fix_image_urls(apps, schema_editor):
    MenuItem = apps.get_model('menu', 'MenuItem')
    
    for item in MenuItem.objects.all():
        if item.image and item.image.startswith('/media/https%3A'):
            # Extract the URL-encoded part and decode it
            encoded_url = item.image.replace('/media/', '')
            decoded_url = urllib.parse.unquote(encoded_url)
            item.image = decoded_url
            item.save()

def reverse_fix_image_urls(apps, schema_editor):
    pass  # No reverse needed

class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0008_change_image_to_urlfield'),
    ]

    operations = [
        migrations.RunPython(fix_image_urls, reverse_fix_image_urls),
    ]