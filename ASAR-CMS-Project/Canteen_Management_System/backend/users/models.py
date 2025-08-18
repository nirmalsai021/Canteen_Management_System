# models.py
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomerProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    roll_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/customers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Customer"

    class Meta:
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"

class AdminProfile(models.Model):
    DEPARTMENT_CHOICES = [
        ('KITCHEN', 'Kitchen'),
        ('MANAGEMENT', 'Management'),
        ('ACCOUNTS', 'Accounts'),
        ('SUPERVISOR', 'Supervisor'),
        ('OTHER', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    employee_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='OTHER')
    position = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/admins/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Admin ({self.department})"

    class Meta:
        verbose_name = "Admin Profile"
        verbose_name_plural = "Admin Profiles"

# Optional: Auto-create profiles when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create profile based on user type"""
    if created:
        if instance.is_staff:
            AdminProfile.objects.get_or_create(user=instance)
        else:
            CustomerProfile.objects.get_or_create(user=instance)