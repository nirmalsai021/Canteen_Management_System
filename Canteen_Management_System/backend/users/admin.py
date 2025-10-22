# admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomerProfile, AdminProfile

# Inline admin for profiles
class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = 'Customer Profile'
    fields = ('phone', 'roll_number', 'address', 'gender', 'date_of_birth', 'profile_image')

class AdminProfileInline(admin.StackedInline):
    model = AdminProfile
    can_delete = False
    verbose_name_plural = 'Admin Profile'
    fields = ('phone', 'employee_id', 'department', 'position', 'profile_image', 'is_active')

# Extended User Admin
class UserAdmin(BaseUserAdmin):
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        
        inlines = []
        if obj.is_staff:
            inlines.append(AdminProfileInline(self.model, admin.site))
        else:
            inlines.append(CustomerProfileInline(self.model, admin.site))
        
        return inlines

# Register models
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'phone', 'gender', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('user__username', 'user__email', 'roll_number', 'phone')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'position', 'is_active', 'created_at')
    list_filter = ('department', 'is_active', 'created_at')
    search_fields = ('user__username', 'user__email', 'employee_id', 'position')
    readonly_fields = ('created_at', 'updated_at')