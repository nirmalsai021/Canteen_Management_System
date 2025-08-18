# orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price', 'created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_amount', 'total_items', 'created_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'id']
    readonly_fields = ['total_amount', 'total_items', 'created_at', 'updated_at']
    list_editable = ['status']
    inlines = [OrderItemInline]
    
    actions = ['mark_as_confirmed', 'mark_as_preparing', 'mark_as_ready', 'mark_as_delivered']
    
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='CONFIRMED')
    mark_as_confirmed.short_description = "Mark selected orders as Confirmed"
    
    def mark_as_preparing(self, request, queryset):
        queryset.update(status='PREPARING')
    mark_as_preparing.short_description = "Mark selected orders as Preparing"
    
    def mark_as_ready(self, request, queryset):
        queryset.update(status='READY')
    mark_as_ready.short_description = "Mark selected orders as Ready"
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='DELIVERED')
    mark_as_delivered.short_description = "Mark selected orders as Delivered"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'menu_item', 'quantity', 'price', 'total_price', 'created_at']
    list_filter = ['created_at', 'menu_item__category']
    search_fields = ['order__id', 'menu_item__name', 'order__user__username']
    readonly_fields = ['total_price', 'created_at']