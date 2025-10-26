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
            'image': 'menu_images/Masala_Puri.jpg'
        },
        {
            'name': 'Pani Puri',
            'description': '',
            'price': '25.00',
            'available': True,
            'category': 'snacks',
            'image': 'menu_images/Pani_Puri.jpg'
        },
        {
            'name': 'Badam Milk',
            'description': '',
            'price': '40.00',
            'available': True,
            'category': 'drinks',
            'image': 'menu_images/Badam_Milk.jpg'
        },
        {
            'name': 'Gobi Rice',
            'description': '',
            'price': '50.00',
            'available': True,
            'category': 'lunch',
            'image': 'menu_images/Gobi_Rice.jpg'
        },
        {
            'name': 'Egg Rice',
            'description': '',
            'price': '45.00',
            'available': True,
            'category': 'lunch',
            'image': 'menu_images/Egg_Rice.jpg'
        },
        {
            'name': 'Poori',
            'description': '',
            'price': '20.00',
            'available': True,
            'category': 'breakfast',
            'image': 'menu_images/Poori.jpg'
        },
        {
            'name': 'Egg Puff',
            'description': '',
            'price': '20.00',
            'available': True,
            'category': 'snacks',
            'image': 'menu_images/Egg_Puff.jpg'
        },
        {
            'name': 'Samosa',
            'description': '',
            'price': '10.00',
            'available': True,
            'category': 'snacks',
            'image': 'menu_images/Samosa.jpg'
        },
        {
            'name': 'Curd Rice',
            'description': '',
            'price': '35.00',
            'available': True,
            'category': 'lunch',
            'image': 'menu_images/Curd_Rice.jpg'
        },
        {
            'name': 'Parotha',
            'description': '',
            'price': '30.00',
            'available': True,
            'category': 'breakfast',
            'image': 'menu_images/Parotha.jpg'
        },
        {
            'name': 'Biryani',
            'description': '',
            'price': '100.00',
            'available': True,
            'category': 'lunch',
            'image': 'menu_images/Biryani.jpg'
        },
        {
            'name': 'Tea',
            'description': '',
            'price': '10.00',
            'available': True,
            'category': 'drinks',
            'image': 'menu_images/Tea.jpg'
        },
        {
            'name': 'Green Tea',
            'description': '',
            'price': '15.00',
            'available': True,
            'category': 'drinks',
            'image': 'menu_images/Green_Tea.jpg'
        },
        {
            'name': 'Coffee',
            'description': '',
            'price': '10.00',
            'available': True,
            'category': 'drinks',
            'image': 'menu_images/Coffee.jpg'
        },
        {
            'name': 'Dosa',
            'description': '',
            'price': '25.00',
            'available': True,
            'category': 'breakfast',
            'image': 'menu_images/Dosa.jpg'
        },
        {
            'name': 'Idli',
            'description': '',
            'price': '20.00',
            'available': True,
            'category': 'breakfast',
            'image': 'menu_images/Idli.jpg'
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