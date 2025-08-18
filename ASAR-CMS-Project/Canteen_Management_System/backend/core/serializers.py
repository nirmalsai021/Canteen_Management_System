from rest_framework import serializers
from .models import CanteenTiming

class CanteenTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CanteenTiming
        fields = '__all__'