from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    GenericAPIView
)

from .serializers import(
    ProductSerializer, 
    CreateRateProductSerializer, 
    ProductDetailSerializer
) 

from .models import Product

from categories.models import Category, SubCategory

#######################
#### Product APIS #####
#######################
class ProductAPIViewSet(ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProductSerializer
        else:
            return ProductDetailSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = (permissions.AllowAny,)
        else:
            permission_classes = (permissions.IsAuthenticated,)
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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

class AutomaticBiddingProductAPI(APIView):
    def post(self, request, product_id):
        get_product = Product.objects.filter(id=product_id).first()
        if get_product: 
                # if less than limit 
                if get_product.bidding_limit > get_product.price:
                    get_product.price += 1
                    get_product.save()

                return Response(
                    {"data": get_product.price},
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'error': 'product is not exists'},
                status=status.HTTP_404_NOT_FOUND
            )

class FixedPriceProducts(ListAPIView):
    queryset = Product.objects.filter(is_fixed=True)
    serializer_class = ProductSerializer

class VariablePriceProducts(ListAPIView):
    queryset = Product.objects.filter(is_fixed=False)
    serializer_class = ProductSerializer

class LatestProducts(ListAPIView):
    queryset = Product.objects.order_by('-created_at')
    serializer_class = ProductSerializer

class HighPriceProducsts(ListAPIView):
    queryset = Product.objects.all().order_by('-price')
    serializer_class = ProductSerializer

class LowPriceProducts(ListAPIView):
    queryset = Product.objects.all().order_by('price')
    serializer_class = ProductSerializer

class SearchByCategory(APIView):
    
    def post(self, request):
        try:
            category = Category.objects.get(name=request.data['name'])
        except Category.DoesNotExist:
            return Response(
                {'error': 'category does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        queryset = category.products.all()
        product_serializer = ProductSerializer(queryset, many=True)
        return Response(product_serializer.data, status=status.HTTP_200_OK)

class SearchBySubCategory(APIView):

    def post(self, request):
        try:
            sub_category = SubCategory.objects.get(name=request.data['name'])
        except SubCategory.DoesNotExist:
            return Response(
                {'error': 'sub category does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        queryset = sub_category.products.all()
        product_serializer = ProductSerializer(queryset, many=True)
        return Response(product_serializer.data, status=status.HTTP_200_OK)

class SearchByName(APIView):
    def post(self, request):
        if request.data.get('name'):        
            products = Product.objects.filter(name__icontains=request.data['name'])
            product_serializer = ProductSerializer(products, many=True)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'please add param for category name '},
                status=status.HTTP_400_BAD_REQUEST
            )

#######################
#### RateProduct APIS #####
#######################

class RequestRateProduct(CreateAPIView):
    serializer_class = CreateRateProductSerializer

    def create(self, request):
        serializer = CreateRateProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)