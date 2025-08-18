from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.ReadOnlyField(source='menu_item.name')

    class Meta:
        model = Booking
        fields = ['id', 'user', 'menu_item', 'menu_item_name', 'date', 'quantity', 'created_at']
        read_only_fields = ['user', 'created_at']