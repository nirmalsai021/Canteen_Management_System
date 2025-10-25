# cart/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Cart, CartItem
from .serializers import (
    CartSerializer, 
    CartItemSerializer, 
    AddToCartSerializer, 
    UpdateCartItemSerializer
)
from menu.models import MenuItem

class CartDetailView(generics.RetrieveAPIView):
    """Get current user's cart"""
    serializer_class = CartSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """Add item to cart or update quantity if item already exists"""
    serializer = AddToCartSerializer(data=request.data)
    
    if serializer.is_valid():
        menu_item_id = serializer.validated_data['menu_item_id']
        quantity = serializer.validated_data['quantity']
        
        # Get or create cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Get menu item
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        
        # Check if item already in cart
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            menu_item=menu_item,
            defaults={'quantity': quantity}
        )
        
        if not item_created:
            # Item already exists, update quantity
            cart_item.quantity += quantity
            cart_item.save()
            message = f"Updated {menu_item.name} quantity to {cart_item.quantity}"
        else:
            message = f"Added {menu_item.name} to cart"
        
        return Response({
            'message': message,
            'cart_item': CartItemSerializer(cart_item).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    """Update quantity of specific cart item"""
    serializer = UpdateCartItemSerializer(data=request.data)
    
    if serializer.is_valid():
        quantity = serializer.validated_data['quantity']
        
        try:
            cart_item = CartItem.objects.get(
                id=item_id,
                cart__user=request.user
            )
            cart_item.quantity = quantity
            cart_item.save()
            
            return Response({
                'message': 'Cart item updated successfully',
                'cart_item': CartItemSerializer(cart_item).data
            })
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    """Remove specific item from cart"""
    try:
        cart_item = CartItem.objects.get(
            id=item_id,
            cart__user=request.user
        )
        item_name = cart_item.menu_item.name
        cart_item.delete()
        
        return Response({
            'message': f'Removed {item_name} from cart'
        }, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response(
            {'error': 'Cart item not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    """Clear all items from cart"""
    try:
        cart = Cart.objects.get(user=request.user)
        cart.clear()
        return Response({
            'message': 'Cart cleared successfully'
        }, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({
            'message': 'Cart is already empty'
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_summary(request):
    """Get cart summary (total items and price)"""
    try:
        cart = Cart.objects.get(user=request.user)
        return Response({
            'total_items': cart.total_items,
            'total_price': cart.total_price,
            'items_count': cart.items.count()
        })
    except Cart.DoesNotExist:
        return Response({
            'total_items': 0,
            'total_price': 0.00,
            'items_count': 0
        })