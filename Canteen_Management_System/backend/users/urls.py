# users/urls.py
from django.urls import path
from .views import (
    # Authentication
    UserRegisterView, AdminRegisterView,
    CustomTokenObtainPairView, AdminTokenObtainPairView,
    LogoutView, simple_admin_login,
    
    # Profiles
    CustomerProfileView, AdminProfileView,
    
    # User Management (Admin only)
    UserListView, UserDetailView,
    
    # Utility
    user_profile_info, check_username_availability,
    
    # Legacy (if needed)
    CustomAuthToken
)

urlpatterns = [
    # =============================================================================
    # AUTHENTICATION ENDPOINTS
    # =============================================================================
    
    # Registration
    path('register/', UserRegisterView.as_view(), name='user_register'),
    # path('admin/register/', AdminRegisterView.as_view(), name='admin_register'),  # Disabled - using predefined admin
    
    # Login
    path('login/', CustomTokenObtainPairView.as_view(), name='user_login'),
    path('admin/login/', simple_admin_login, name='admin_login'),  # Simple JSON-only login
    
    # Logout
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # =============================================================================
    # PROFILE MANAGEMENT
    # =============================================================================
    
    path('profile/', CustomerProfileView.as_view(), name='customer_profile'),
    path('admin/profile/', AdminProfileView.as_view(), name='admin_profile'),
    path('profile/info/', user_profile_info, name='user_profile_info'),
    
    # =============================================================================
    # USER MANAGEMENT (Admin Only)
    # =============================================================================
    
    path('admin/users/', UserListView.as_view(), name='user_list'),
    path('admin/users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    
    # =============================================================================
    # UTILITY ENDPOINTS
    # =============================================================================
    
    path('check-username/', check_username_availability, name='check_username'),
    
    # =============================================================================
    # LEGACY ENDPOINTS (Optional - for backwards compatibility)
    # =============================================================================
    
    path('auth/token/', CustomAuthToken.as_view(), name='api_token_auth'),
]