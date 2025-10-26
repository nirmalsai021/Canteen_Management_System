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
    """Send email using Django backend with console fallback"""
    
    subject = "Password Reset Code - MITS Canteen"
    message = f"""Hello {user_name},

Your password reset verification code is: {code}

This code will expire in 10 minutes.

If you didn't request this password reset, please ignore this email.

Best regards,
MITS Canteen Team"""

    # Try Django's email backend with detailed debugging
    try:
        print(f"\n=== EMAIL DEBUG INFO ===")
        print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        print(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Not set')}")
        print(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Not set')}")
        print(f"EMAIL_HOST_PASSWORD: {'Set' if getattr(settings, 'EMAIL_HOST_PASSWORD', '') else 'Not set'}")
        print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        print(f"To: {email}")
        print(f"Reset Code: {code}")
        print(f"========================\n")
        
        logger.info(f"Attempting to send email to {email} using Django backend")
        result = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )
        
        print(f"\n=== EMAIL SEND RESULT ===")
        print(f"send_mail() returned: {result}")
        print(f"========================\n")
        
        if result:
            logger.info(f"Email sent successfully to {email} via Django backend")
            return True
        else:
            print(f"\n❌ send_mail() returned 0 - email not sent")
            return False
            
    except Exception as e:
        logger.error(f"Django email backend failed for {email}: {str(e)}")
        print(f"\n=== EMAIL DELIVERY FAILED ===")
        print(f"Email: {email}")
        print(f"Reset Code: {code}")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        print(f"================================\n")
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
        
        logger.info(f"Generated reset code {code} for {email}")
        
        # Try to send email
        email_sent = send_email_with_fallback(email, code, user.first_name or user.username)
        
        # Always return success but include debug info if email failed
        response_data = {
            "message": "Verification code sent to your email",
            "email": email
        }
        
        # If email failed or in debug mode, include the code
        if not email_sent or settings.DEBUG:
            response_data["debug_code"] = code
            response_data["debug_note"] = "Email delivery may have failed - code provided for testing"
        
        return JsonResponse(response_data)
        
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