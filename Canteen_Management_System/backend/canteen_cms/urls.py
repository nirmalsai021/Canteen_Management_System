# main urls.py (project level)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from admin_login import bulletproof_admin_login
from simple_admin_auth import simple_admin_login
from serve_media import serve_media
from password_reset import send_reset_code, verify_reset_code
from simple_password_reset import simple_send_code, simple_verify_code
from password_reset_secure import secure_send_code, secure_verify_code

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Direct admin login (bypass middleware issues)
    path('api/users/admin/login/', bulletproof_admin_login, name='bulletproof_admin_login'),
    path('api/admin/login/', simple_admin_login, name='simple_admin_login'),
    
    # API endpoints
    path('api/users/', include('users.urls')),
    path('api/menu/', include('menu.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/timings/', include('core.urls')),
    
    # JWT Token endpoints
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Media files serving
    path('media/<path:path>', serve_media, name='serve_media'),
    
    # Password reset endpoints
    path('api/password-reset/send-code/', secure_send_code, name='send_reset_code'),
    path('api/password-reset/verify/', secure_verify_code, name='verify_reset_code'),
]

# ✅ Serve media files in both development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
