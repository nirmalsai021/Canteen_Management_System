from django.urls import path
from .views import CanteenTimingView

urlpatterns = [
    path('', CanteenTimingView.as_view(), name='canteen-timing'),
]