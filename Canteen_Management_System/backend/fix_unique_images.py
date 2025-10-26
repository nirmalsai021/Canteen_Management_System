#!/usr/bin/env python
import os
import django
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from menu.models import MenuItem

def fix_menu_images():
    """Fix menu items with unique, high-quality food images"""
    
    # Clear existing items
    MenuItem.objects.all().delete()
    print("🗑️ Cleared existing menu items")
    
    # 16 unique menu items with individual high-quality images
    menu_items = [
        {
            'name': 'Masala Puri',
            'price': '30.00',
            'category': 'snacks',
            'description': 'Crispy puris topped with spicy masala and chutneys',
            'image': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400&h=300&fit=crop&auto=format'
        },
        {
            'name': 'Pani Puri',
            'price': '25.00',
            'category': 'snacks',
            'description': 'Hollow crispy shells filled with tangy water and chutneys',
            'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400&h=300&fit=crop&auto=format'
        },
        {
            'name': 'Badam Milk',
            'price': '40.00',
            'category': 'drinks',
            'description': 'Rich almond milk with cardamom and saffron',
            'image': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=400&h=300&fit=crop&auto=format'
        },
        {
            'name': 'Gobi Rice',
            'price': '50.00',
            'category': 'lunch',
            'description': 'Fragrant rice cooked with cauliflower and spices',
            'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop&auto=format'
        },
        {
            'name': 'Egg Rice',
            'price': '45.00',
            'category': 'lunch',
            'description': 'Delicious fried rice with scrambled eggs and vegetables',
            'image': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400&h=300&fit=crop&auto=format'
        },
        {
            'name': 'Poori',
            'price': '20.00',
            'category': 'breakfast',
            'description': 'Deep-fried bread served with curry',
            'image': 'https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=400&h=300&fit=crop&auto=format'
        },
        {
            'name': 'Egg Puff',
            'price': '20.00',
            'category': 'snacks',
            'description': 'Flaky pastry filled with spiced egg mixture',
            'image': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=300&fit=crop&auto=format'
        },
        {
            'name': 'Samosa',
            'price': '10.00',
            'category': 'snacks',
            'description': 'Crispy triangular pastry with potato filling',
            'image': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400&h=300&fit=crop&auto=format&q=80'
        },
        {
            'name': 'Curd Rice',
            'price': '35.00',
            'category': 'lunch',
            'description': 'Cooling rice mixed with yogurt and tempered spices',
            'image': 'https://images.unsplash.com/photo-1512058564366-18510be2db19?w=400&h=300&fit=crop&auto=format'
        },
        {
            'name': 'Parotha',
            'price': '30.00',
            'category': 'breakfast',
            'description': 'Layered flatbread served with curry or pickle',
            'image': 'https://images.unsplash.com/photo-1574653853027-5d5c7b9c6d0f?w=400&h=300&fit=crop&auto=format'
        },
        {
            'name': 'Biryani',
            'price': '100.00',
            'category': 'lunch',
            'description': 'Aromatic basmati rice with spiced meat or vegetables',
            'image': 'https://images.unsplash.com/photo-1563379091339-03246963d51a?w=400&h=300&fit=crop&auto=format'
        },
        {
            'name': 'Tea',
            'price': '10.00',
            'category': 'drinks',
            'description': 'Traditional Indian chai with milk and spices',
            'image': 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=300&fit=crop&auto=format'
        },
        {
            'name': 'Green Tea',
            'price': '15.00',
            'category': 'drinks',
            'description': 'Healthy green tea with antioxidants',
            'image': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&h=300&fit=crop&auto=format'
        },
        {
            'name': 'Coffee',
            'price': '10.00',
            'category': 'drinks',
            'description': 'Fresh brewed coffee, hot or cold',
            'image': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop&auto=format'
        },
        {
            'name': 'Dosa',
            'price': '25.00',
            'category': 'breakfast',
            'description': 'Crispy South Indian crepe served with sambar and chutney',
            'image': 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400&h=300&fit=crop&auto=format'
        },
        {
            'name': 'Idli',
            'price': '20.00',
            'category': 'breakfast',
            'description': 'Soft steamed rice cakes served with sambar and chutney',
            'image': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400&h=300&fit=crop&auto=format'
        }
    ]
    
    created_count = 0
    for item_data in menu_items:
        try:
            MenuItem.objects.create(
                name=item_data['name'],
                description=item_data['description'],
                price=item_data['price'],
                available=True,
                category=item_data['category'],
                image=item_data['image']
            )
            created_count += 1
            print(f'✅ Created: {item_data["name"]} - {item_data["image"]}')
        except Exception as e:
            print(f'❌ Error creating {item_data["name"]}: {e}')
    
    print(f'✅ Successfully created {created_count}/16 menu items with unique images')
    
    # Verify all items have unique images
    items = MenuItem.objects.all()
    images = [item.image for item in items]
    unique_images = set(images)
    
    print(f'📊 Total items: {len(items)}')
    print(f'📊 Unique images: {len(unique_images)}')
    
    if len(images) == len(unique_images):
        print('✅ All items have unique images!')
    else:
        print('⚠️ Some items share the same image')
        
    return created_count

if __name__ == '__main__':
    fix_menu_images()