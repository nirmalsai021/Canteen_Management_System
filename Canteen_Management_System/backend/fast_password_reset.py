import random
import string
import threading
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.core.cache import cache

def send_email_async(email, code, user_name):
    """Send email using SendGrid HTTPS API"""
    try:
        import requests
        
        # SendGrid API endpoint
        url = "https://api.sendgrid.com/v3/mail/send"
        
        # Email data
        data = {
            "personalizations": [{
                "to": [{"email": email}],
                "subject": "Password Reset Code - MITS Canteen"
            }],
            "from": {"email": settings.DEFAULT_FROM_EMAIL},
            "content": [{
                "type": "text/plain",
                "value": f"Hello,\n\nYour password reset verification code is: {code}\n\nThis code will expire in 10 minutes.\n\nIf you didn't request this password reset, please ignore this email.\n\nBest regards,\nMITS Canteen Team"
            }]
        }
        
        # Headers with API key
        headers = {
            "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Send via HTTPS API
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 202:
            print(f"Email sent successfully to {email} via SendGrid API")
            return True
        else:
            print(f"SendGrid API error: {response.status_code} - {response.text}")
            return False
        
    except Exception as e:
        print(f"Email sending failed to {email}: {str(e)}")
        return False

@csrf_exempt
@require_http_methods(["POST"])
def fast_send_code(request):
    """Fast password reset - immediate response"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        
        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)
        
        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"error": "No account found with this email address"}, status=404)
        
        # Generate code
        code = ''.join(random.choices(string.digits, k=6))
        
        # Store code immediately
        cache_key = f"reset_code_{email}"
        cache.set(cache_key, code, 600)  # 10 minutes
        
        # Send email in background thread (non-blocking)
        email_thread = threading.Thread(
            target=send_email_async, 
            args=(email, code, user.first_name or user.username)
        )
        email_thread.daemon = True
        email_thread.start()
        
        # Return immediately
        return JsonResponse({
            "message": "Verification code sent to your email",
            "email": email
        })
        
    except Exception as e:
        return JsonResponse({"error": "Failed to send reset code"}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def fast_verify_code(request):
    """Verify code and reset password"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        code = data.get('code')
        new_password = data.get('new_password')
        
        if not all([email, code, new_password]):
            return JsonResponse({"error": "Email, code, and password required"}, status=400)
        
        # Check cached code
        cache_key = f"reset_code_{email}"
        stored_code = cache.get(cache_key)
        
        if not stored_code:
            return JsonResponse({"error": "Verification code expired or invalid"}, status=400)
        
        if stored_code != code:
            return JsonResponse({"error": "Invalid verification code"}, status=400)
        
        # Reset password
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            # Clear code
            cache.delete(cache_key)
            
            return JsonResponse({
                "message": "Password reset successfully",
                "username": user.username
            })
            
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        
    except Exception as e:
        return JsonResponse({"error": "Failed to reset password"}, status=500)