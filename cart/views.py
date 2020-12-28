from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import (
    Cart,
    CartItem
)

from products.models import Product

from .serializers import CartItemSerializers

class GetCartAPI(APIView):

    def get(self, request):
        
        # get user cart
        try:
            get_user_cart = Cart.objects.get(user=request.user, is_ordered=False)

        except Cart.DoesNotExist:
            return Response(
                {'error': 'user does not have cart'},
                status=status.HTTP_404_NOT_FOUND
            )
        cart_item_objects = get_user_cart.products.all()
        cart_item_serializer = CartItemSerializers(cart_item_objects, many=True)
        
        return Response(
            {
                'data':cart_item_serializer.data,
                'price': get_user_cart.calculate_price(),
                'taxes': get_user_cart.calculate_taxes(),
                'total_price': get_user_cart.calculate_total_price()
            },
            status=status.HTTP_200_OK
        )

class AddCartProductAPI(APIView):

    def post(self, request, product_id):
        # get user cart
        get_user_cart, _ = Cart.objects.get_or_create(user=request.user, is_ordered=False)

        # get product by product id 
        try:
            get_product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'error': "product is not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # get quantity from requested data
        try:
            quantity = request.data['quantity']
        except:
            return Response(
                {'error': 'please add quantity to the requested data'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # check if the product in the cart 
        get_cart_item, created = CartItem.objects.get_or_create(
            product=get_product,
            cart=get_user_cart
        )

        if created:
            get_cart_item.quantity = quantity
            get_cart_item.save()
            return Response(
                {'data': 'added to the cart successfully.'},
                status=status.HTTP_201_CREATED
            )
        else:
            get_cart_item.quantity = quantity
            get_cart_item.save()
            return Response(
                {'data': 'product exists in the cart but updated the quantity'},
                status=status.HTTP_201_CREATED
            )

class RemoveCartProduct(APIView):
    def delete(self, request, product_id):
        
        # get the cart 
        try:
            get_user_cart = Cart.objects.get(user=request.user, is_ordered=False)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'user does not have cart'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # get product by product id 
        try:
            get_product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'error': "product is not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            get_cart_item = CartItem.objects.get(product=get_product, cart=get_user_cart)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'product is not exists in the cart'}
            )
        
        # delete cart item from cart
        get_cart_item.delete()
        return Response(
            {'data': 'product item is deleted from the cart'},
            status=status.HTTP_204_NO_CONTENT
        )