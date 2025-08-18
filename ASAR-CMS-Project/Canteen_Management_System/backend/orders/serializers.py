# orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from menu.models import MenuItem

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menu_item_category = serializers.CharField(source='menu_item.category', read_only=True)
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'menu_item_category', 
                 'quantity', 'price', 'total_price', 'created_at']
        read_only_fields = ['price', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_username', 'status', 'total_amount', 
                 'total_items', 'notes', 'items', 'created_at', 'updated_at']
        read_only_fields = ['user', 'total_amount', 'created_at', 'updated_at']

class OrderCreateSerializer(serializers.Serializer):
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True)

    def create(self, validated_data):
        user = self.context['request'].user
        
        # Get user's cart
        from cart.models import Cart
        try:
            cart = Cart.objects.get(user=user)
            if not cart.items.exists():
                raise serializers.ValidationError("Cart is empty")
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Cart not found")

        # Create order
        order = Order.objects.create(
            user=user,
            notes=validated_data.get('notes', ''),
            total_amount=0
        )

        # Create order items from cart items
        for cart_item in cart.items.all():
            # Check if menu item is still available
            if not cart_item.menu_item.available:
                order.delete()  # Clean up
                raise serializers.ValidationError(
                    f"{cart_item.menu_item.name} is no longer available"
                )
            
            OrderItem.objects.create(
                order=order,
                menu_item=cart_item.menu_item,
                quantity=cart_item.quantity,
                price=cart_item.menu_item.price
            )

        # Calculate total amount
        order.calculate_total()
        
        # Clear cart after successful order
        cart.clear()
        
        return order

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        if value not in ['CONFIRMED', 'PREPARING', 'READY', 'DELIVERED', 'CANCELLED']:
            raise serializers.ValidationError("Invalid status")
        return value