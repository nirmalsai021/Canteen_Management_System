from rest_framework import generics, permissions
from .models import CanteenTiming
from .serializers import CanteenTimingSerializer

class CanteenTimingView(generics.RetrieveUpdateAPIView):
    queryset = CanteenTiming.objects.all()
    serializer_class = CanteenTimingSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        # Only one timing object in system
        return CanteenTiming.objects.first()