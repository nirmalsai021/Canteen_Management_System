#!/usr/bin/env python3
"""
Test the login endpoint directly
"""
import os
import django
import sys

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from users.views import simple_admin_login
from django.http import HttpRequest
import json

def test_login_direct():
    print("Testing login endpoint directly...")
    
    # Create a mock request
    request = HttpRequest()
    request.method = 'POST'
    request.META['CONTENT_TYPE'] = 'application/json'
    
    # Set the request body
    body_data = {
        'username': 'canteen',
        'password': 'canteen@321'
    }
    request._body = json.dumps(body_data).encode('utf-8')
    
    try:
        response = simple_admin_login(request)
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        
        if response.status_code == 200:
            data = json.loads(response.content.decode())
            print(f"Token returned: {data.get('token', 'NO TOKEN')}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_login_direct()
    if success:
        print("\nLogin endpoint test PASSED!")
    else:
        print("\nLogin endpoint test FAILED!")