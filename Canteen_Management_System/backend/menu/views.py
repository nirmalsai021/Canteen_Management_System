from rest_framework import generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import MenuItem
from .serializers import MenuItemSerializer

class IsAdminOrSimpleToken(BasePermission):
    """Custom permission for admin access with simple token"""
    def has_permission(self, request, view):
        # Check for simple admin token
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        print(f'Auth header received: {auth_header}')
        
        if auth_header == 'Bearer admin-token-12345':
            print('Admin token validated successfully')
            return True
        
        # Check for regular admin user
        if request.user and request.user.is_staff:
            print('Regular admin user authenticated')
            return True
            
        print('Authentication failed')
        return False

# Customer Views (Public/Authenticated)
class CustomerMenuListView(generics.ListAPIView):
    """Public view for customers to see available menu items"""
    serializer_class = MenuItemSerializer
    permission_classes = []  # Public access
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'available']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'category']
    ordering = ['category', 'name']

    def get_queryset(self):
        return MenuItem.objects.filter(available=True)

class CustomerMenuDetailView(generics.RetrieveAPIView):
    """Public view for customers to see specific menu item details"""
    serializer_class = MenuItemSerializer
    permission_classes = []  # Public access
    
    def get_queryset(self):
        return MenuItem.objects.filter(available=True)

@api_view(['GET'])
def menu_categories(request):
    """Get all available categories"""
    categories = MenuItem.objects.filter(available=True).values_list('category', flat=True).distinct()
    category_choices = dict(MenuItem.CATEGORY_CHOICES)
    
    result = [
        {
            'value': category,
            'label': category_choices.get(category, category.title())
        }
        for category in categories
    ]
    
    return Response(result)

@api_view(['GET'])
def featured_items(request):
    """Get featured/popular menu items (you can customize this logic)"""
    # For now, just return first 6 available items
    # You can enhance this with popularity logic later
    featured = MenuItem.objects.filter(available=True)[:6]
    serializer = MenuItemSerializer(featured, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_menu(request):
    """Advanced search for menu items"""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    queryset = MenuItem.objects.filter(available=True)

    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    if category:
        queryset = queryset.filter(category=category.strip().lower())  # force lowercase match
    
    if min_price:
        try:
            queryset = queryset.filter(price__gte=float(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            queryset = queryset.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    serializer = MenuItemSerializer(queryset, many=True)
    return Response(serializer.data)

# Admin Views (Existing functionality)
class MenuItemListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrSimpleToken]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'available']
    search_fields = ['name', 'description']

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrSimpleToken]

# Function-based views (for backward compatibility)
@api_view(['GET'])
def list_items(request):
    items = MenuItem.objects.all()
    serializer = MenuItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminOrSimpleToken])
def add_item(request):
    serializer = MenuItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminOrSimpleToken])
def update_item(request, pk):
    try:
        item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MenuItemSerializer(item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminOrSimpleToken])
def delete_item(request, pk):
    try:
        item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    item.delete()
    return Response({'message': 'Item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)