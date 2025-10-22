from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
@require_http_methods(["POST"])
def bulletproof_admin_login(request):
    """Bulletproof admin login that always returns JSON"""
    try:
        # Parse request body
        body = request.body.decode('utf-8')
        if not body:
            return JsonResponse({"error": "Empty request body"}, status=400)
        
        data = json.loads(body)
        username = data.get('username')
        password = data.get('password')
        
        # Check credentials
        if username == 'canteen' and password == 'canteen@321':
            return JsonResponse({
                "access": "admin-token-12345",
                "refresh": "admin-refresh-12345", 
                "user": {
                    "id": 1,
                    "username": "canteen",
                    "email": "canteen@example.com",
                    "first_name": "Admin",
                    "last_name": "User"
                },
                "user_type": "admin",
                "message": "Login successful"
            })
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)