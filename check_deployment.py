import requests
import time

def check_deployment():
    try:
        r = requests.post('https://canteen-backend-bbqk.onrender.com/api/admin/login/', 
                         json={'username': 'canteen', 'password': 'canteen@321'}, 
                         timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            token = data.get('access', '')
            
            if len(token) > 20:  # Real Django token
                print("✅ Deployment successful! Testing API...")
                
                # Test API endpoints
                headers = {'Authorization': f'Token {token}'}
                
                menu_r = requests.get('https://canteen-backend-bbqk.onrender.com/api/menu/', 
                                    headers=headers, timeout=10)
                orders_r = requests.get('https://canteen-backend-bbqk.onrender.com/api/orders/admin/', 
                                      headers=headers, timeout=10)
                
                print(f"Menu API: {'✅ Working' if menu_r.status_code == 200 else '❌ Failed'}")
                print(f"Orders API: {'✅ Working' if orders_r.status_code == 200 else '❌ Failed'}")
                
                if menu_r.status_code == 200 and orders_r.status_code == 200:
                    print("🎉 Admin authentication is fully fixed!")
                    return True
                else:
                    print("⚠️ Some APIs still failing")
                    return False
            else:
                print("⏳ Still deploying... (old token)")
                return False
        else:
            print(f"❌ Login failed: {r.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Checking deployment status...")
    success = check_deployment()
    
    if not success:
        print("\n⏳ Waiting for deployment to complete...")
        print("This may take 2-5 minutes on Render...")
        
    exit(0 if success else 1)