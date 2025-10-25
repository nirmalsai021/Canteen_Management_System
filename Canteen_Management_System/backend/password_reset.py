import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.core.cache import cache

@csrf_exempt
@require_http_methods(["POST"])
def send_reset_code(request):
    """Send password reset verification code to email"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        
        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)
        
        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"error": "No user found with this email"}, status=404)
        
        # Generate 6-digit verification code
        code = ''.join(random.choices(string.digits, k=6))
        
        # Store code in cache for 10 minutes
        cache_key = f"reset_code_{email}"
        cache.set(cache_key, code, 600)  # 10 minutes
        
        # Send email
        subject = "Password Reset Code - MITS Canteen"
        message = f"""
Hello {user.first_name or user.username},

Your password reset verification code is: {code}

This code will expire in 10 minutes.

If you didn't request this, please ignore this email.

Best regards,
MITS Canteen Team
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )
        
        return JsonResponse({
            "message": "Verification code sent to your email",
            "email": email
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def verify_reset_code(request):
    """Verify the reset code and allow password reset"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        code = data.get('code')
        new_password = data.get('new_password')
        
        if not all([email, code, new_password]):
            return JsonResponse({"error": "Email, code, and new password are required"}, status=400)
        
        # Check cached code
        cache_key = f"reset_code_{email}"
        stored_code = cache.get(cache_key)
        
        if not stored_code:
            return JsonResponse({"error": "Verification code expired or invalid"}, status=400)
        
        if stored_code != code:
            return JsonResponse({"error": "Invalid verification code"}, status=400)
        
        # Get user and update password
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            # Clear the code from cache
            cache.delete(cache_key)
            
            return JsonResponse({
                "message": "Password reset successfully",
                "username": user.username
            })
            
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)