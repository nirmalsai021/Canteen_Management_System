# menu/urls.py (Enhanced)
from django.urls import path
from . import views

urlpatterns = [
    # Customer menu endpoints (public)
    path('customer/', views.CustomerMenuListView.as_view(), name='customer-menu-list'),
    path('customer/<int:pk>/', views.CustomerMenuDetailView.as_view(), name='customer-menu-detail'),
    path('customer/categories/', views.menu_categories, name='menu-categories'),
    path('customer/featured/', views.featured_items, name='featured-items'),
    path('customer/search/', views.search_menu, name='search-menu'),
    
    # Admin menu endpoints
    path('admin/', views.MenuItemListCreateView.as_view(), name='admin-menu-list-create'),
    path('admin/<int:pk>/', views.MenuItemDetailView.as_view(), name='admin-menu-detail'),
    
    # Legacy endpoints (for backward compatibility)
    path('', views.list_items, name='list-items'),
    path('add/', views.add_item, name='add-item'),
    path('<int:pk>/update/', views.update_item, name='update-item'),
    path('<int:pk>/delete/', views.delete_item, name='delete-item'),
]