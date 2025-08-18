# cart/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem
from menu.models import MenuItem

class CartItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menu_item_price = serializers.DecimalField(source='menu_item.price', max_digits=6, decimal_places=2, read_only=True)
    menu_item_category = serializers.CharField(source='menu_item.category', read_only=True)
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    menu_item_available = serializers.BooleanField(source='menu_item.available', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'menu_item', 'menu_item_name', 'menu_item_price', 'menu_item_category', 
                 'menu_item_available', 'quantity', 'total_price', 'added_at']
        read_only_fields = ['added_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class AddToCartSerializer(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, max_value=50)

    def validate_menu_item_id(self, value):
        try:
            menu_item = MenuItem.objects.get(id=value)
            if not menu_item.available:
                raise serializers.ValidationError("This menu item is not available.")
        except MenuItem.DoesNotExist:
            raise serializers.ValidationError("Menu item does not exist.")
        return value

class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, max_value=50)