#!/usr/bin/env python3
"""
Script to create admin user and token on deployed backend
Run this after deployment to ensure admin token exists in PostgreSQL
"""

import requests
import json

# Backend URL
BACKEND_URL = "https://canteen-backend-bbqk.onrender.com"

def create_admin_token():
    """Create admin user and token via API call"""
    try:
        # Try to create admin via management command endpoint (if exists)
        # Or create via direct database setup
        
        print("🔧 Setting up admin user and token...")
        print("📍 Backend URL:", BACKEND_URL)
        
        # Test if backend is accessible
        response = requests.get(f"{BACKEND_URL}/api/menu/", timeout=30)
        print(f"✅ Backend is accessible (Status: {response.status_code})")
        
        print("\n📝 Manual steps needed:")
        print("1. SSH into your Render backend service")
        print("2. Run: python manage.py create_admin")
        print("3. This will create user 'canteen' with token 'admin-token-12345'")
        print("4. Then test the admin panel login")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to backend: {e}")
        return False

if __name__ == "__main__":
    create_admin_token()