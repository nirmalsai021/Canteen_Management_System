#!/usr/bin/env python
import requests

def verify_menu_images():
    try:
        response = requests.get("https://canteen-backend-bbqk.onrender.com/api/menu/")
        if response.status_code == 200:
            items = response.json()
            images = [item.get('image', '') for item in items]
            unique_images = set(images)
            
            print(f"Total items: {len(items)}")
            print(f"Unique images: {len(unique_images)}")
            
            if len(images) == len(unique_images):
                print("SUCCESS: All items have unique images!")
            else:
                print("WARNING: Some items share images")
                
            return len(images) == len(unique_images)
        else:
            print(f"Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    verify_menu_images()
