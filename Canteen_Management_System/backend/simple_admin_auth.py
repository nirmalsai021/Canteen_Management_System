from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import json

@csrf_exempt
@require_http_methods(["POST"])
def simple_admin_login(request):
    """Real Django token authentication for admin"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        # Check hardcoded admin credentials
        if username == 'canteen' and password == 'canteen@321':
            # Get or create admin user
            user, created = User.objects.get_or_create(
                username='canteen',
                defaults={
                    'email': 'canteen@example.com',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            if created:
                user.set_password('canteen@321')
                user.save()

            # Generate real Django token
            token, _ = Token.objects.get_or_create(user=user)

            return JsonResponse({
                "access": token.key,
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_staff": user.is_staff
                },
                "message": "Login successful"
            })
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
