from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from datetime import datetime
from .models import Booking
from .serializers import BookingSerializer
from core.models import CanteenTiming  # Make sure core app has this model

class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        now = datetime.now().time()

        # Get canteen timing
        timing = CanteenTiming.objects.first()
        if timing and (now < timing.opening_time or now > timing.closing_time):
            raise ValidationError("Canteen is closed. Booking allowed only during working hours.")

        serializer.save(user=self.request.user)

class CancelBookingView(generics.DestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)