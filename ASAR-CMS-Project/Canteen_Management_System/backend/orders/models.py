# orders/models.py - Temporary modification for migration
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from menu.models import MenuItem

class Order(models.Model):
    STATUS_CHOICES = [
        ('PLACED', 'Placed'),
        ('CONFIRMED', 'Confirmed'),
        ('PREPARING', 'Preparing'),
        ('READY', 'Ready'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLACED')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.status}"

    def calculate_total(self):
        """Calculate total amount from order items"""
        total = sum(item.total_price for item in self.items.all())
        self.total_amount = total
        self.save()
        return total

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # Add default value temporarily for migration
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    # Add default value temporarily for migration  
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.menu_item.name} (x{self.quantity}) for Order #{self.order.id}"

    @property
    def total_price(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        # Store the current price of the menu item when creating order item
        if not self.price or self.price == 0:
            self.price = self.menu_item.price
        super().save(*args, **kwargs)