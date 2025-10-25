import random
import string
import threading
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.core.cache import cache

logger = logging.getLogger(__name__)

def send_email_with_fallback(email, code, user_name):
    """Send email using Django backend first, then fallback to direct API"""
    
    subject = "Password Reset Code - MITS Canteen"
    message = f"""Hello {user_name},

Your password reset verification code is: {code}

This code will expire in 10 minutes.

If you didn't request this password reset, please ignore this email.

Best regards,
MITS Canteen Team"""

    # Method 1: Try Django's email backend first
    try:
        logger.info(f"Attempting to send email to {email} using Django backend")
        result = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )
        if result:
            logger.info(f"Email sent successfully to {email} via Django backend")
            return True
    except Exception as e:
        logger.error(f"Django email backend failed for {email}: {str(e)}")

    # Method 2: Fallback to direct SendGrid API
    try:
        import requests
        logger.info(f"Attempting to send email to {email} using SendGrid API")
        
        url = "https://api.sendgrid.com/v3/mail/send"
        
        data = {
            "personalizations": [{
                "to": [{"email": email}],
                "subject": subject
            }],
            "from": {"email": settings.DEFAULT_FROM_EMAIL},
            "content": [{
                "type": "text/plain",
                "value": message
            }]
        }
        
        headers = {
            "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 202:
            logger.info(f"Email sent successfully to {email} via SendGrid API")
            return True
        else:
            logger.error(f"SendGrid API error: {response.status_code} - {response.text}")
            return False
        
    except Exception as e:
        logger.error(f"SendGrid API failed for {email}: {str(e)}")
        return False

@csrf_exempt
@require_http_methods(["POST"])
def secure_send_code(request):
    """Send password reset code"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        
        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)
        
        if '@' not in email or '.' not in email:
            return JsonResponse({"error": "Invalid email format"}, status=400)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"error": "No account found with this email address"}, status=404)
        
        code = ''.join(random.choices(string.digits, k=6))
        cache_key = f"reset_code_{email}"
        cache.set(cache_key, code, 600)
        
        logger.info(f"Generated reset code for {email}")
        
        email_thread = threading.Thread(
            target=send_email_with_fallback, 
            args=(email, code, user.first_name or user.username)
        )
        email_thread.daemon = True
        email_thread.start()
        
        return JsonResponse({
            "message": "Verification code sent to your email",
            "email": email
        })
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        return JsonResponse({"error": "Failed to send reset code"}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def secure_verify_code(request):
    """Verify code and reset password"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        code = data.get('code')
        new_password = data.get('new_password')
        
        if not all([email, code, new_password]):
            return JsonResponse({"error": "Email, code, and password are required"}, status=400)
        
        if len(new_password) < 6:
            return JsonResponse({"error": "Password must be at least 6 characters long"}, status=400)
        
        cache_key = f"reset_code_{email}"
        stored_code = cache.get(cache_key)
        
        if not stored_code:
            return JsonResponse({"error": "Verification code expired or invalid"}, status=400)
        
        if stored_code != code:
            return JsonResponse({"error": "Invalid verification code"}, status=400)
        
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            cache.delete(cache_key)
            
            logger.info(f"Password reset successful for user: {user.username}")
            
            return JsonResponse({
                "message": "Password reset successfully",
                "username": user.username
            })
            
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        logger.error(f"Password verification error: {str(e)}")
        return JsonResponse({"error": "Failed to reset password"}, status=500)