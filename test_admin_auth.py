#!/usr/bin/env python
"""
Test script to verify admin authentication works
"""
import requests
import json

# Configuration
BACKEND_URL = "https://canteen-backend-bbqk.onrender.com"
ADMIN_TOKEN = "admin-token-12345"

def test_admin_login():
    """Test admin login endpoint"""
    print("Testing admin login...")
    
    url = f"{BACKEND_URL}/api/admin/login/"
    data = {
        "username": "canteen",
        "password": "canteen@321"
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("Admin login works!")
            return True
        else:
            print("Admin login failed!")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_admin_endpoints():
    """Test admin endpoints with token"""
    print("\nTesting admin endpoints...")
    
    headers = {
        "Authorization": f"Token {ADMIN_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Test menu endpoint
    print("Testing menu endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/menu/", headers=headers, timeout=30)
        print(f"Menu API Status: {response.status_code}")
        if response.status_code == 200:
            print("Menu API works!")
        else:
            print(f"Menu API failed: {response.text}")
    except Exception as e:
        print(f"Menu API error: {e}")
    
    # Test orders endpoint
    print("Testing orders endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/orders/admin/", headers=headers, timeout=30)
        print(f"Orders API Status: {response.status_code}")
        if response.status_code == 200:
            print("Orders API works!")
        else:
            print(f"Orders API failed: {response.text}")
    except Exception as e:
        print(f"Orders API error: {e}")

if __name__ == "__main__":
    print("Testing Admin Authentication System")
    print("=" * 50)
    
    # Test login
    login_works = test_admin_login()
    
    # Test endpoints
    test_admin_endpoints()
    
    print("\n" + "=" * 50)
    if login_works:
        print("Admin system is working!")
    else:
        print("Admin system needs fixing!")