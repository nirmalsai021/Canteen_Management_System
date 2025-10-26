#!/usr/bin/env python
"""
Script to trigger menu update on next deployment
"""
import os
import datetime

def create_deployment_trigger():
    """Create files to trigger menu update on deployment"""
    
    # Create a startup script that will run the management command
    startup_script = """#!/usr/bin/env python
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.core.management import call_command

# Run the menu update command
try:
    call_command('create_default_items')
    print("Menu items updated successfully with unique images")
except Exception as e:
    print(f"Error updating menu items: {e}")
"""
    
    with open('startup_menu_update.py', 'w') as f:
        f.write(startup_script)
    
    print("Created startup_menu_update.py")
    
    # Update the force redeploy trigger
    redeploy_file = os.path.join('..', '..', 'force_redeploy.txt')
    
    with open(redeploy_file, 'w') as f:
        f.write(f"Force redeploy triggered at {datetime.datetime.now()}\n")
        f.write("Reason: Updated menu items with unique images\n")
        f.write("Changes: Fixed create_default_items.py with 16 unique images\n")
    
    print("Updated force_redeploy.txt")
    
    # Create a simple verification script
    verify_script = """#!/usr/bin/env python
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
"""
    
    with open('verify_menu_images.py', 'w') as f:
        f.write(verify_script)
    
    print("Created verify_menu_images.py")

def show_deployment_instructions():
    """Show instructions for deployment"""
    
    print("\n" + "="*60)
    print("DEPLOYMENT INSTRUCTIONS")
    print("="*60)
    print()
    print("1. CHANGES MADE:")
    print("   - Updated create_default_items.py with 16 unique images")
    print("   - Fixed Unicode encoding issues")
    print("   - Fixed signal handlers for URLField")
    print()
    print("2. VERIFICATION (Local):")
    print("   - Run: python manage.py create_default_items")
    print("   - Confirmed: 16 items with 16 unique images")
    print()
    print("3. PRODUCTION DEPLOYMENT:")
    print("   - Commit all changes to GitHub")
    print("   - Push to main branch")
    print("   - Render will auto-deploy")
    print("   - Run management command on production")
    print()
    print("4. VERIFICATION (Production):")
    print("   - Run: python verify_menu_images.py")
    print("   - Check frontend apps for unique images")
    print()
    print("5. MENU ITEMS WITH UNIQUE IMAGES:")
    
    items = [
        "Masala Puri", "Pani Puri", "Badam Milk", "Gobi Rice",
        "Egg Rice", "Poori", "Egg Puff", "Samosa",
        "Curd Rice", "Parotha", "Biryani", "Tea",
        "Green Tea", "Coffee", "Dosa", "Idli"
    ]
    
    for i, item in enumerate(items, 1):
        print(f"   {i:2d}. {item}")
    
    print()
    print("="*60)
    print("READY FOR DEPLOYMENT!")
    print("="*60)

if __name__ == '__main__':
    create_deployment_trigger()
    show_deployment_instructions()