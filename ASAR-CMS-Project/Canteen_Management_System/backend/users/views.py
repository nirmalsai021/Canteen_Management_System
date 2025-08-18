# views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from .models import CustomerProfile, AdminProfile
from .serializers import (
    RegisterSerializer, 
    CustomerProfileSerializer, 
    UserSerializer,
    AdminRegistrationSerializer,
    AdminProfileSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from .token_serializers import CustomTokenObtainPairSerializer, AdminTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes

# =============================================================================
# AUTHENTICATION VIEWS (Both Admin & User)
# =============================================================================

class CustomTokenObtainPairView(TokenObtainPairView):
    """Login view for regular users"""
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

class AdminTokenObtainPairView(TokenObtainPairView):
    """Login view for admin users"""
    serializer_class = AdminTokenObtainPairSerializer
    permission_classes = [AllowAny]

# =============================================================================
# REGISTRATION VIEWS
# =============================================================================

class UserRegisterView(generics.CreateAPIView):
    """Registration for regular users (customers)"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        
        # Create customer profile
        CustomerProfile.objects.get_or_create(user=user)
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            "message": "User registered successfully",
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(access),
            "user_type": "customer"
        }, status=status.HTTP_201_CREATED)

class AdminRegisterView(generics.CreateAPIView):
    """Registration for admin users - only accessible by superuser"""
    queryset = User.objects.all()
    serializer_class = AdminRegistrationSerializer
    permission_classes = [IsAdminUser]  # Only admin can create admin users

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        
        # Make user staff and superuser
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        # Create admin profile
        AdminProfile.objects.get_or_create(user=user)
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            "message": "Admin registered successfully",
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(access),
            "user_type": "admin"
        }, status=status.HTTP_201_CREATED)

# =============================================================================
# LOGOUT VIEW
# =============================================================================

class LogoutView(APIView):
    """Logout view for both admin and users"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token is None:
                raise ValidationError("Refresh token is required")

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "message": "Logout successful"
            }, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

# =============================================================================
# PROFILE VIEWS
# =============================================================================

class CustomerProfileView(generics.RetrieveUpdateAPIView):
    """Customer profile management"""
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Ensure user is not admin
        if self.request.user.is_staff:
            raise ValidationError("Admin users cannot access customer profiles")
        
        profile, created = CustomerProfile.objects.get_or_create(user=self.request.user)
        return profile

class AdminProfileView(generics.RetrieveUpdateAPIView):
    """Admin profile management"""
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        profile, created = AdminProfile.objects.get_or_create(user=self.request.user)
        return profile

# =============================================================================
# USER MANAGEMENT VIEWS (Admin Only)
# =============================================================================

class UserListView(generics.ListAPIView):
    """List all users - Admin only"""
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """User detail management - Admin only"""
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

# =============================================================================
# UTILITY VIEWS
# =============================================================================

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile_info(request):
    """Get current user profile information"""
    user = request.user
    
    if user.is_staff:
        try:
            admin_profile = AdminProfile.objects.get(user=user)
            profile_data = AdminProfileSerializer(admin_profile).data
        except AdminProfile.DoesNotExist:
            profile_data = None
        
        return Response({
            "user": UserSerializer(user).data,
            "user_type": "admin",
            "profile": profile_data
        })
    else:
        try:
            customer_profile = CustomerProfile.objects.get(user=user)
            profile_data = CustomerProfileSerializer(customer_profile).data
        except CustomerProfile.DoesNotExist:
            profile_data = None
        
        return Response({
            "user": UserSerializer(user).data,
            "user_type": "customer",
            "profile": profile_data
        })

@api_view(['POST'])
@permission_classes([AllowAny])
def check_username_availability(request):
    """Check if username is available"""
    username = request.data.get('username')
    if not username:
        return Response({
            "error": "Username is required"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    is_available = not User.objects.filter(username=username).exists()
    return Response({
        "username": username,
        "is_available": is_available
    })

# =============================================================================
# LEGACY TOKEN AUTH (if needed for backwards compatibility)
# =============================================================================

class CustomAuthToken(ObtainAuthToken):
    """Legacy token authentication"""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': user.username,
            'user_type': 'admin' if user.is_staff else 'customer'
        })