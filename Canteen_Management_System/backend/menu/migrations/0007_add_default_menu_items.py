# Generated manually to add default menu items

from django.db import migrations

def create_default_menu_items(apps, schema_editor):
    MenuItem = apps.get_model('menu', 'MenuItem')
    
    # Clear existing items
    MenuItem.objects.all().delete()
    
    # Create default menu items with images
    default_items = [
        {
            'name': 'Masala Puri',
            'description': '',
            'price': '30.00',
            'available': True,
            'category': 'snacks',
            'image': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=300&h=200&fit=crop'
        },
        {
            'name': 'Pani Puri',
            'description': '',
            'price': '25.00',
            'available': True,
            'category': 'snacks',
            'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300&h=200&fit=crop'
        },
        {
            'name': 'Badam Milk',
            'description': '',
            'price': '40.00',
            'available': True,
            'category': 'drinks',
            'image': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=300&h=200&fit=crop'
        },
        {
            'name': 'Gobi Rice',
            'description': '',
            'price': '50.00',
            'available': True,
            'category': 'lunch',
            'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=300&h=200&fit=crop'
        },
        {
            'name': 'Egg Rice',
            'description': '',
            'price': '45.00',
            'available': True,
            'category': 'lunch',
            'image': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=300&h=200&fit=crop'
        },
        {
            'name': 'Poori',
            'description': '',
            'price': '20.00',
            'available': True,
            'category': 'breakfast',
            'image': 'https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=300&h=200&fit=crop'
        },
        {
            'name': 'Egg Puff',
            'description': '',
            'price': '20.00',
            'available': True,
            'category': 'snacks',
            'image': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=300&h=200&fit=crop'
        },
        {
            'name': 'Samosa',
            'description': '',
            'price': '10.00',
            'available': True,
            'category': 'snacks',
            'image': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=300&h=200&fit=crop'
        },
        {
            'name': 'Curd Rice',
            'description': '',
            'price': '35.00',
            'available': True,
            'category': 'lunch',
            'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=300&h=200&fit=crop'
        },
        {
            'name': 'Parotha',
            'description': '',
            'price': '30.00',
            'available': True,
            'category': 'breakfast',
            'image': 'https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=300&h=200&fit=crop'
        },
        {
            'name': 'Biryani',
            'description': '',
            'price': '100.00',
            'available': True,
            'category': 'lunch',
            'image': 'https://images.unsplash.com/photo-1563379091339-03246963d51a?w=300&h=200&fit=crop'
        },
        {
            'name': 'Tea',
            'description': '',
            'price': '10.00',
            'available': True,
            'category': 'drinks',
            'image': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=300&h=200&fit=crop'
        },
        {
            'name': 'Green Tea',
            'description': '',
            'price': '15.00',
            'available': True,
            'category': 'drinks',
            'image': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=300&h=200&fit=crop'
        },
        {
            'name': 'Coffee',
            'description': '',
            'price': '10.00',
            'available': True,
            'category': 'drinks',
            'image': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=300&h=200&fit=crop'
        },
        {
            'name': 'Dosa',
            'description': '',
            'price': '25.00',
            'available': True,
            'category': 'breakfast',
            'image': 'https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=300&h=200&fit=crop'
        },
        {
            'name': 'Idli',
            'description': '',
            'price': '20.00',
            'available': True,
            'category': 'breakfast',
            'image': 'https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=300&h=200&fit=crop'
        }
    ]
    
    for item_data in default_items:
        MenuItem.objects.create(**item_data)

def reverse_default_menu_items(apps, schema_editor):
    MenuItem = apps.get_model('menu', 'MenuItem')
    MenuItem.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_alter_menuitem_category'),
    ]

    operations = [
        migrations.RunPython(create_default_menu_items, reverse_default_menu_items),
    ]