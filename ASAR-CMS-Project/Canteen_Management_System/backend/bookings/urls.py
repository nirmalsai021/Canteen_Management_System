from django.urls import path
from .views import BookingListCreateView, CancelBookingView

urlpatterns = [
    path('', BookingListCreateView.as_view(), name='booking-list-create'),
    path('<int:pk>/cancel/', CancelBookingView.as_view(), name='cancel-booking'),
]