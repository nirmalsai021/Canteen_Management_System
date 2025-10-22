# permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user

class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission that allows access to admin users or the owner of the object.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user.is_staff:
            return True
        
        # Owner has access to their own objects
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False

class IsCustomerUser(permissions.BasePermission):
    """
    Custom permission to only allow customer users (non-staff).
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            not request.user.is_staff
        )

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users (staff).
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_staff
        )