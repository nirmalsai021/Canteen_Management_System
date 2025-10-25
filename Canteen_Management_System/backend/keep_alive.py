#!/usr/bin/env python
"""
Keep-alive script for Render deployment
Add this to your build command: python keep_alive.py &
"""
import requests
import time
import threading
import os

def ping_server():
    """Ping the server every 5 minutes to keep it alive"""
    base_url = os.environ.get('RENDER_EXTERNAL_URL', 'https://canteen-backend-bbqk.onrender.com')
    
    while True:
        try:
            response = requests.get(f"{base_url}/api/menu/customer/", timeout=30)
            print(f"Keep-alive ping: {response.status_code}")
        except Exception as e:
            print(f"Keep-alive failed: {e}")
        
        time.sleep(300)  # 5 minutes

if __name__ == "__main__":
    # Start keep-alive in background
    thread = threading.Thread(target=ping_server, daemon=True)
    thread.start()
    
    # Keep the main process alive
    while True:
        time.sleep(60)