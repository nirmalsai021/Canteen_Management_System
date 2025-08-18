# cart/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Cart management
    path('', views.CartDetailView.as_view(), name='cart-detail'),
    path('summary/', views.cart_summary, name='cart-summary'),
    
    # Cart item operations
    path('add/', views.add_to_cart, name='add-to-cart'),
    path('items/<int:item_id>/update/', views.update_cart_item, name='update-cart-item'),
    path('items/<int:item_id>/remove/', views.remove_from_cart, name='remove-from-cart'),
    path('clear/', views.clear_cart, name='clear-cart'),
]