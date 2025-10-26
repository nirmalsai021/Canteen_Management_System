from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
@require_http_methods(["POST"])
def simple_admin_login(request):
    """Simple admin login for canteen management"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        
        print(f"Admin login attempt: {username}")
        
        if username == 'canteen' and password == 'canteen@321':
            # Return a static admin token that works
            return JsonResponse({
                "access": "admin-token-12345",
                "user": {
                    "id": 1,
                    "username": "canteen",
                    "is_staff": True,
                    "is_superuser": True
                },
                "message": "Admin login successful"
            })
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        print(f"Admin login error: {str(e)}")
        return JsonResponse({"error": "Login failed"}, status=500)