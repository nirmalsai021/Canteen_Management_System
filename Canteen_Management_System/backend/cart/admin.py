# cart/admin.py
from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['total_price', 'added_at']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['total_items', 'total_price', 'created_at', 'updated_at']
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'menu_item', 'quantity', 'total_price', 'added_at']
    list_filter = ['added_at', 'menu_item__category']
    search_fields = ['cart__user__username', 'menu_item__name']
    readonly_fields = ['total_price', 'added_at']