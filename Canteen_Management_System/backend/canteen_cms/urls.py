# main urls.py (project level)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from admin_login import bulletproof_admin_login

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Direct admin login (bypass middleware issues)
    path('api/users/admin/login/', bulletproof_admin_login, name='bulletproof_admin_login'),
    
    # API endpoints
    path('api/users/', include('users.urls')),
    path('api/menu/', include('menu.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/timings/', include('core.urls')),
    
    # JWT Token endpoints
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# ✅ Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
