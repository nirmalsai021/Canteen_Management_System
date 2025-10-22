# token_serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer, CustomerProfileSerializer, AdminProfileSerializer
from .models import CustomerProfile, AdminProfile
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Token serializer for customer login"""
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Check if user is not admin (customers only)
        if self.user.is_staff:
            raise serializers.ValidationError("Admin users should use admin login endpoint")
        
        # Add user data
        data['user'] = UserSerializer(self.user).data
        data['user_type'] = 'customer'
        
        # Add profile data if exists
        try:
            profile = CustomerProfile.objects.get(user=self.user)
            data['profile'] = CustomerProfileSerializer(profile).data
        except CustomerProfile.DoesNotExist:
            data['profile'] = None
            
        return data

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Token serializer for admin login"""
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Check if user is admin
        if not self.user.is_staff:
            raise serializers.ValidationError("Only admin users can use this login endpoint")
        
        # Add user data
        data['user'] = UserSerializer(self.user).data
        data['user_type'] = 'admin'
        
        # Add admin profile data if exists
        try:
            profile = AdminProfile.objects.get(user=self.user)
            data['profile'] = AdminProfileSerializer(profile).data
        except AdminProfile.DoesNotExist:
            data['profile'] = None
            
        return data