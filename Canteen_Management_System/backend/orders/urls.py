# orders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Customer order endpoints
    path('', views.CustomerOrderListView.as_view(), name='customer-order-list'),
    path('history/', views.customer_order_history, name='customer-order-history'),
    path('<int:pk>/', views.CustomerOrderDetailView.as_view(), name='customer-order-detail'),
    path('place/', views.place_order, name='place-order'),
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel-order'),
    
    # Admin order endpoints
    path('admin/', views.AdminOrderListView.as_view(), name='admin-order-list'),
    path('admin/<int:pk>/', views.AdminOrderDetailView.as_view(), name='admin-order-detail'),
    path('admin/<int:order_id>/update-status/', views.update_order_status, name='update-order-status'),
    path('admin/summary/today/', views.daily_order_summary, name='daily-order-summary'),
    
    # Admin cancel order (same endpoint as customer but with admin auth)
    path('<int:order_id>/cancel/', views.cancel_order, name='admin-cancel-order'),
]