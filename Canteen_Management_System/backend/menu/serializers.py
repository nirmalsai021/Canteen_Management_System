from rest_framework import serializers
from .models import MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError("Image is required.")
        return value