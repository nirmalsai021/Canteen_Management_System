# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomerProfile, AdminProfile
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for customer registration"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class AdminRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for admin registration"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_staff=True,  # Admin users are staff
            is_superuser=True  # Give admin privileges
        )
        return user

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CustomerProfile
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate_roll_number(self, value):
        if value and CustomerProfile.objects.filter(roll_number=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("This roll number is already taken.")
        return value

class AdminProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = AdminProfile
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate_employee_id(self, value):
        if value and AdminProfile.objects.filter(employee_id=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("This employee ID is already taken.")
        return value

# Detailed serializers for profile updates
class CustomerProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating customer profile with user info"""
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    
    class Meta:
        model = CustomerProfile
        fields = [
            'phone', 'roll_number', 'address', 'gender', 
            'date_of_birth', 'profile_image', 'first_name', 
            'last_name', 'email'
        ]

    def update(self, instance, validated_data):
        # Update user fields
        user_data = validated_data.pop('user', {})
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        
        # Update profile fields
        return super().update(instance, validated_data)

class AdminProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating admin profile with user info"""
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    
    class Meta:
        model = AdminProfile
        fields = [
            'phone', 'employee_id', 'department', 'position',
            'profile_image', 'is_active', 'first_name', 
            'last_name', 'email'
        ]

    def update(self, instance, validated_data):
        # Update user fields
        user_data = validated_data.pop('user', {})
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        
        # Update profile fields
        return super().update(instance, validated_data)