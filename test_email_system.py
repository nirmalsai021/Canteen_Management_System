import requests
import time

def test_email_system():
    """Test the email reset system"""
    
    # Test with a valid email (you need to have a user with this email)
    test_email = "test@example.com"  # Replace with actual user email
    
    print("Testing email reset system...")
    print(f"Testing with email: {test_email}")
    
    # Test 1: Send reset code
    print("\n1. Testing send reset code...")
    start_time = time.time()
    
    try:
        response = requests.post(
            'https://canteen-backend-bbqk.onrender.com/api/password-reset/send-code/',
            json={'email': test_email},
            timeout=30
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"Response time: {response_time:.2f} seconds")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Email sending works!")
        elif response.status_code == 404:
            print("❌ User not found - need to create user with this email first")
        else:
            print("❌ Email sending failed")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - email system is too slow")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_email_system()