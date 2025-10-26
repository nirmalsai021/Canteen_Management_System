import requests

# Direct API calls to update each menu item with unique image
items = [
    {'id': 1, 'name': 'Masala Puri', 'image': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400&h=300&fit=crop&auto=format'},
    {'id': 2, 'name': 'Pani Puri', 'image': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400&h=300&fit=crop&auto=format'},
    {'id': 3, 'name': 'Badam Milk', 'image': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=400&h=300&fit=crop&auto=format'},
    {'id': 4, 'name': 'Gobi Rice', 'image': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop&auto=format'},
    {'id': 5, 'name': 'Egg Rice', 'image': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400&h=300&fit=crop&auto=format'},
    {'id': 6, 'name': 'Poori', 'image': 'https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=400&h=300&fit=crop&auto=format'},
    {'id': 7, 'name': 'Egg Puff', 'image': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=300&fit=crop&auto=format'},
    {'id': 8, 'name': 'Samosa', 'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=300&fit=crop&auto=format'},
    {'id': 9, 'name': 'Curd Rice', 'image': 'https://images.unsplash.com/photo-1512058564366-18510be2db19?w=400&h=300&fit=crop&auto=format'},
    {'id': 10, 'name': 'Parotha', 'image': 'https://images.unsplash.com/photo-1574653853027-5d5c7b9c6d0f?w=400&h=300&fit=crop&auto=format'},
    {'id': 11, 'name': 'Biryani', 'image': 'https://images.unsplash.com/photo-1563379091339-03246963d51a?w=400&h=300&fit=crop&auto=format'},
    {'id': 12, 'name': 'Tea', 'image': 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=300&fit=crop&auto=format'},
    {'id': 13, 'name': 'Green Tea', 'image': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&h=300&fit=crop&auto=format'},
    {'id': 14, 'name': 'Coffee', 'image': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop&auto=format'},
    {'id': 15, 'name': 'Dosa', 'image': 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400&h=300&fit=crop&auto=format'},
    {'id': 16, 'name': 'Idli', 'image': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400&h=300&fit=crop&auto=format'}
]

url = "https://canteen-backend-bbqk.onrender.com/api/menu/"

# Get current items to match IDs
response = requests.get(url)
current_items = response.json()

for i, item in enumerate(current_items[:16]):
    if i < len(items):
        patch_data = {"image": items[i]["image"]}
        patch_url = f"{url}{item['id']}/"
        
        try:
            patch_response = requests.patch(patch_url, json=patch_data)
            print(f"Updated {item['name']}: {patch_response.status_code}")
        except:
            print(f"Failed to update {item['name']}")

# Verify
response = requests.get(url)
items = response.json()
images = [item.get('image', '') for item in items]
unique_images = set(images)
print(f"Final: {len(items)} items, {len(unique_images)} unique images")