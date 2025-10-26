#!/usr/bin/env python
"""
Simple script to create admin token via HTTP request
This can be run from anywhere to set up the admin token
"""

import requests
import json

def setup_admin_token():
    """Create admin token by calling the admin login endpoint"""
    
    # First, let's try to login with admin credentials
    login_url = "https://canteen-backend-bbqk.onrender.com/api/users/admin/login/"
    
    login_data = {
        "username": "canteen",
        "password": "canteen@321"
    }
    
    try:
        print("🔧 Attempting admin login to create token...")
        response = requests.post(login_url, json=login_data, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access', 'No token found')
            print(f"✅ Admin login successful!")
            print(f"✅ Token: {token}")
            
            # Test the token
            test_url = "https://canteen-backend-bbqk.onrender.com/api/menu/"
            headers = {"Authorization": f"Token {token}"}
            
            test_response = requests.get(test_url, headers=headers, timeout=30)
            if test_response.status_code == 200:
                print("✅ Token works! Admin authentication is now set up.")
            else:
                print(f"⚠️ Token created but test failed: {test_response.status_code}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_admin_token()