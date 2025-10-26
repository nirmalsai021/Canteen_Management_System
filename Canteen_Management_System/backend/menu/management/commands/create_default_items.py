from django.core.management.base import BaseCommand
from menu.models import MenuItem

class Command(BaseCommand):
    help = 'Create default menu items with images'

    def handle(self, *args, **options):
        # Clear existing items first (including corrupted ones)
        MenuItem.objects.all().delete()
        self.stdout.write('🗑️ Cleared existing menu items')
        
        default_items = [
            {'name': 'Masala Puri', 'price': '30.00', 'category': 'snacks', 'image': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=300&h=200&fit=crop'},
            {'name': 'Pani Puri', 'price': '25.00', 'category': 'snacks', 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300&h=200&fit=crop'},
            {'name': 'Badam Milk', 'price': '40.00', 'category': 'drinks', 'image': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=300&h=200&fit=crop'},
            {'name': 'Gobi Rice', 'price': '50.00', 'category': 'lunch', 'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=300&h=200&fit=crop'},
            {'name': 'Egg Rice', 'price': '45.00', 'category': 'lunch', 'image': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=300&h=200&fit=crop'},
            {'name': 'Poori', 'price': '20.00', 'category': 'breakfast', 'image': 'https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=300&h=200&fit=crop'},
            {'name': 'Egg Puff', 'price': '20.00', 'category': 'snacks', 'image': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=300&h=200&fit=crop'},
            {'name': 'Samosa', 'price': '10.00', 'category': 'snacks', 'image': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=300&h=200&fit=crop'},
            {'name': 'Curd Rice', 'price': '35.00', 'category': 'lunch', 'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=300&h=200&fit=crop'},
            {'name': 'Parotha', 'price': '30.00', 'category': 'breakfast', 'image': 'https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=300&h=200&fit=crop'},
            {'name': 'Biryani', 'price': '100.00', 'category': 'lunch', 'image': 'https://images.unsplash.com/photo-1563379091339-03246963d51a?w=300&h=200&fit=crop'},
            {'name': 'Tea', 'price': '10.00', 'category': 'drinks', 'image': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=300&h=200&fit=crop'},
            {'name': 'Green Tea', 'price': '15.00', 'category': 'drinks', 'image': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=300&h=200&fit=crop'},
            {'name': 'Coffee', 'price': '10.00', 'category': 'drinks', 'image': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=300&h=200&fit=crop'},
            {'name': 'Dosa', 'price': '25.00', 'category': 'breakfast', 'image': 'https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=300&h=200&fit=crop'},
            {'name': 'Idli', 'price': '20.00', 'category': 'breakfast', 'image': 'https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=300&h=200&fit=crop'},
        ]

        created_count = 0
        for item_data in default_items:
            MenuItem.objects.create(
                name=item_data['name'],
                description='',
                price=item_data['price'],
                available=True,
                category=item_data['category'],
                image=item_data['image']
            )
            created_count += 1
            self.stdout.write(f'✅ Created: {item_data["name"]}')

        self.stdout.write(self.style.SUCCESS(f'✅ Created all {created_count} default menu items with images'))