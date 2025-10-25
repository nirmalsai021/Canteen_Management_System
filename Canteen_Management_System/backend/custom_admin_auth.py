from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

class AdminTokenAuthentication(BaseAuthentication):
    """
    Custom authentication for admin panel using hardcoded token
    """
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header:
            return None
            
        try:
            # Check for Token admin-token-12345
            if auth_header == 'Token admin-token-12345':
                # Create or get admin user
                admin_user, created = User.objects.get_or_create(
                    username='canteen',
                    defaults={
                        'email': 'canteen@example.com',
                        'first_name': 'Admin',
                        'last_name': 'User',
                        'is_staff': True,
                        'is_superuser': True,
                        'is_active': True
                    }
                )
                
                # Ensure user has admin privileges
                if not admin_user.is_staff:
                    admin_user.is_staff = True
                    admin_user.is_superuser = True
                    admin_user.save()
                
                return (admin_user, 'admin-token-12345')
                
        except Exception:
            pass
            
        return None

    def authenticate_header(self, request):
        return 'Token'