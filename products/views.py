from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .serializers import ProductSerializer
from .models import Product

class ProductAPIViewSet(ModelViewSet):

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = (permissions.AllowAny,)
        else:
            permission_classes = (permissions.IsAuthenticated,)
        return [permission() for permission in permission_classes]
        
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ToggleFavoriteProductAPI(APIView):

    def post(self, request, product_id):
        get_product = Product.objects.filter(id=product_id).first()
        current_user = request.user

        if get_product:
            # if product exists in fav product of the current user,
            # remove product from the fav list of the current user 
            if get_product in current_user.favorite_products.all():
                current_user.favorite_products.remove(get_product)
                return Response(
                    {'data': 'product is removed from your favroite products list'},
                    status=status.HTTP_200_OK
                    )
            # if product doesn't exist in fav products of the current user,
            # add product to the fav products of the current user 
            else:
                current_user.favorite_products.add(get_product)
                return Response(
                    {'data': 'product is added to your favroite products list'},
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'error': 'product id is not exist'},
                status=status.HTTP_404_NOT_FOUND
                )


class BiddingProductAPI(APIView):
    def post(self, request, product_id):
        new_price = request.data['new_price']
        get_product = Product.objects.filter(id=product_id).first()
        if get_product:
            # check if the new price is greater than old price
            if new_price > get_product.price:
                # change the old price to the new one 
                # and save changes after that to commit the database
                get_product.price = new_price
                get_product.save()

                return Response(
                    {"data": 'you bidded successfully'},
                    status=status.HTTP_200_OK
                )
            # else if .. 
            # new price is less than or equal old price 
            else:
                return Response(
                    {'error': 'please put higer price than current price'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'error': 'product is not exists'},
                status=status.HTTP_404_NOT_FOUND
            )