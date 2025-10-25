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
        
        if username == 'canteen' and password == 'canteen@321':
            # Get the real Django token for the admin user
            from django.contrib.auth.models import User
            from rest_framework.authtoken.models import Token
            try:
                user = User.objects.get(username='canteen')
                token, created = Token.objects.get_or_create(user=user)
                return JsonResponse({
                    "access": token.key,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "is_staff": user.is_staff,
                        "is_superuser": user.is_superuser
                    },
                    "message": "Admin login successful"
                })
            except User.DoesNotExist:
                return JsonResponse({"error": "Admin user not found"}, status=500)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
            
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)