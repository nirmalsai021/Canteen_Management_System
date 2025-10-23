#!/usr/bin/env python3
"""
Deployment update script for Render
Run this after pushing to update the backend with admin functionality
"""

import os
import django
from django.core.management import execute_from_command_line

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

def update_deployment():
    """Update deployment with new admin functionality"""
    print("🚀 Updating deployment with admin functionality...")
    
    # Run migrations
    print("📦 Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Collect static files
    print("📁 Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    print("✅ Deployment update complete!")
    print("🔧 Admin endpoints now available:")
    print("   - POST /api/admin/login/ (canteen/canteen@321)")
    print("   - GET /api/menu/admin-list/ (list items)")
    print("   - PUT /api/menu/<id>/update/ (edit items)")
    print("   - DELETE /api/menu/<id>/delete/ (delete items)")
    print("   - GET /api/menu/admin-orders/ (list orders)")

if __name__ == '__main__':
    update_deployment()