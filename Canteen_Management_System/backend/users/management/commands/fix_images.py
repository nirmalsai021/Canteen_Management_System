from django.core.management.base import BaseCommand
from menu.models import MenuItem

class Command(BaseCommand):
    help = 'Fix menu item images with working URLs'

    def handle(self, *args, **options):
        # Sample food images from a reliable CDN
        image_mapping = {
            'burger': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=200&fit=crop',
            'pizza': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop',
            'coffee': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=300&h=200&fit=crop',
            'sandwich': 'https://images.unsplash.com/photo-1553909489-cd47e0ef937f?w=300&h=200&fit=crop',
        }

        # Update menu items with working image URLs
        for item in MenuItem.objects.all():
            item_name_lower = item.name.lower()
            
            # Find matching image
            for key, url in image_mapping.items():
                if key in item_name_lower:
                    item.image = url
                    item.save()
                    self.stdout.write(f"Updated {item.name}: {url}")
                    break
            else:
                # Default food image
                item.image = 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=300&h=200&fit=crop'
                item.save()
                self.stdout.write(f"Updated {item.name}: default food image")

        self.stdout.write(self.style.SUCCESS('All menu items updated with working image URLs!'))