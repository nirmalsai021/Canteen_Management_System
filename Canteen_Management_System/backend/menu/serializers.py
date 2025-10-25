from rest_framework import serializers
from .models import MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = MenuItem
        fields = '__all__'

    def validate_image(self, value):
        if value and hasattr(value, 'size'):
            # Validate file size (max 5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Image file size should be less than 5MB")
            
            # Validate file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if hasattr(value, 'content_type') and value.content_type not in allowed_types:
                raise serializers.ValidationError("Only JPEG, PNG, and GIF images are allowed")
        
        return value
    
    def update(self, instance, validated_data):
        # Handle image field specially for updates
        image = validated_data.get('image')
        
        # If image is empty string or None, don't update the image field
        if image == '' or image is None:
            validated_data.pop('image', None)
        
        return super().update(instance, validated_data)