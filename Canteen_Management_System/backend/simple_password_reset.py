from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.core.cache import cache
import json
import random
import string

@csrf_exempt
@require_http_methods(["POST"])
def simple_send_code(request):
    """Simple password reset without email - just generate and store code"""
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
        
        # Generate 6-digit code
        code = ''.join(random.choices(string.digits, k=6))
        
        # Store code in cache for 10 minutes
        cache_key = f"reset_code_{email}"
        cache.set(cache_key, code, 600)
        
        # For testing - return the code in response (remove in production)
        return JsonResponse({
            "message": "Verification code generated",
            "email": email,
            "code": code  # Remove this in production
        })
        
    except Exception as e:
        return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def simple_verify_code(request):
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
            return JsonResponse({"error": "Code expired or invalid"}, status=400)
        
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
                "message": "Password reset successfully"
            })
            
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        
    except Exception as e:
        return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)