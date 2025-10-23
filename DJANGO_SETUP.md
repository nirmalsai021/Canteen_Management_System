# 🔧 Django Backend Setup for Full Functionality

## 🚀 **Quick Setup Steps:**

### **1. Create Django Superuser**
On your Render backend, run:
```bash
python manage.py createsuperuser
```
- Username: `admin` (or any name)
- Password: `admin123` (or secure password)
- Email: your email

### **2. Update Django Settings**
Make sure your `settings.py` has:

```python
# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "https://canteen-management-system-coral.vercel.app",
    "https://canteen-management-system-lo73.vercel.app",
]

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

# JWT Settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

### **3. Update URLs**
In your main `urls.py`:
```python
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/menu/', include('menu.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/cart/', include('cart.urls')),
]
```

### **4. Menu ViewSet (menu/views.py)**
```python
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import MenuItem
from .serializers import MenuItemSerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
```

### **5. Orders ViewSet (orders/views.py)**
```python
from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
```

## 🎯 **After Setup:**

### **✅ Full Functionality:**
1. **Login:** Use your Django superuser credentials
2. **View Items:** ✅ Works
3. **Add Items:** ✅ Works  
4. **Edit Items:** ✅ Works with real auth
5. **Delete Items:** ✅ Works with real auth
6. **View Orders:** ✅ Works with real auth

### **🔄 Demo Fallback:**
- If Django auth fails, demo login still works
- Limited to view/add operations only

## 🚀 **Deploy & Test:**

1. **Update Django backend** with above settings
2. **Create superuser** on Render
3. **Test admin login** with real credentials
4. **Full CRUD operations** should work!

**Your admin panel will have complete functionality! 🎉**