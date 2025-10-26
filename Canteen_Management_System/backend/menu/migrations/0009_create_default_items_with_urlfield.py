# Create default menu items after URLField is ready

from django.db import migrations

def create_default_items_safe(apps, schema_editor):
    MenuItem = apps.get_model('menu', 'MenuItem')
    
    # Clear any existing items first
    MenuItem.objects.all().delete()
    
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

    for item_data in default_items:
        MenuItem.objects.create(
            name=item_data['name'],
            description='',
            price=item_data['price'],
            available=True,
            category=item_data['category'],
            image=item_data['image']
        )

def reverse_create_items(apps, schema_editor):
    MenuItem = apps.get_model('menu', 'MenuItem')
    MenuItem.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0008_safe_image_urlfield'),
    ]

    operations = [
        migrations.RunPython(create_default_items_safe, reverse_create_items),
    ]