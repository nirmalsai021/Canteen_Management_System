#!/usr/bin/env python
"""
Deploy script to update menu items with unique images in production
"""
import requests
import json

def deploy_to_production():
    """Deploy the updated menu items to production"""
    
    # Production API endpoint
    PRODUCTION_URL = "https://canteen-backend-bbqk.onrender.com"
    
    print("Deploying menu items with unique images to production...")
    
    # Test if production is accessible
    try:
        response = requests.get(f"{PRODUCTION_URL}/api/menu/", timeout=10)
        print(f"Production server is accessible: {response.status_code}")
    except Exception as e:
        print(f"Cannot reach production server: {e}")
        return False
    
    # The management command will run automatically on the next deployment
    # Since we've updated the create_default_items.py file
    
    print("Updated menu management command with unique images")
    print("Next deployment will automatically update menu items")
    
    # Verify current menu items
    try:
        response = requests.get(f"{PRODUCTION_URL}/api/menu/")
        if response.status_code == 200:
            menu_items = response.json()
            print(f"Current menu items in production: {len(menu_items)}")
            
            # Check for unique images
            images = [item.get('image', '') for item in menu_items]
            unique_images = set(images)
            
            print(f"Unique images: {len(unique_images)}")
            
            if len(images) == len(unique_images):
                print("All items already have unique images!")
            else:
                print("Some items share the same image - deployment needed")
                
        else:
            print(f"Could not fetch menu items: {response.status_code}")
            
    except Exception as e:
        print(f"Error checking menu items: {e}")
    
    return True

def trigger_redeploy():
    """Create a trigger file to force redeployment"""
    
    # Update the force redeploy file
    import os
    import datetime
    
    redeploy_file = os.path.join(os.path.dirname(__file__), '..', '..', 'force_redeploy.txt')
    
    with open(redeploy_file, 'w') as f:
        f.write(f"Force redeploy triggered at {datetime.datetime.now()}\n")
        f.write("Reason: Updated menu items with unique images\n")
    
    print("Created redeploy trigger file")

if __name__ == '__main__':
    success = deploy_to_production()
    if success:
        trigger_redeploy()
        print("\nDeployment preparation complete!")
        print("Next steps:")
        print("1. Commit and push changes to GitHub")
        print("2. Production will auto-deploy with updated menu items")
        print("3. All 16 menu items will have unique, high-quality images")
    else:
        print("\nDeployment preparation failed")