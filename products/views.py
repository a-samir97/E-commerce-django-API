from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from payment.views import get_client_ip
from payment import secrets
import json , requests , hashlib
from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    GenericAPIView
)

from .serializers import(
    ProductSerializer, 
    CreateRateProductSerializer, 
    ProductDetailSerializer,
    ListRateProductSerializer
) 

from .models import (
    Product,
    ProductImage,
    ProductRateImage,
    RateProduct
)

from .pagination import ProductPagination

from categories.models import Category, SubCategory
from users.serializers import UserDataSerializer
from cart.models import Cart, CartItem

from utils import send_sms_messages, send_single_message

import datetime
import asyncio

#######################
#### Product APIS #####
#######################
class ProductAPIViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-created_at').filter(in_stock__gte=1)
    pagination_class = ProductPagination

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
        product = serializer.save(owner=self.request.user)
        images = dict((self.request.data).lists())['images']
        for image in images:
            ProductImage.objects.create(
                product=product,
                img=image
            )
        send_sms_messages(self.request.user.following.all())


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

class GetUserFavoriteProductsAPI(ListAPIView):
    
    def get_queryset(self):
        return self.request.user.favorite_products.all()
    
    serializer_class = ProductSerializer

class BiddingProductAPI(APIView):
    def post(self, request, product_id):

        get_product = Product.objects.filter(id=product_id).first()
        if not get_product:
            return Response(
                {'error': 'product is not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        if get_product.is_fixed:
            return Response(
                {'error': 'this product has a fixed price'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # normal bidding 
        if request.data.get('new_price'):
            new_price = request.data['new_price']

            # check if the new price is greater than current price 
            # and check also if the new price is greater than the current bidding limit 
            
            if new_price <= get_product.price:
                return Response(
                    {'error': 'new price should be higher than the current price'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            elif new_price > get_product.price and new_price >= get_product.bidding_limit:
                get_product.price = new_price
                get_product.last_user_bid = request.user
                get_product.save()
            
            else:
                get_product.price = new_price + 1
                get_product.save()

            # user serializer 
            user_serializer = UserDataSerializer(get_product.last_user_bid)

            return Response(
                {
                    'new_price': get_product.price,
                    'user': user_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        # automatic bidding
        elif request.data.get('limit'):
            limit = request.data['limit']
            # check if the limit is greater than the current price
            # and also greater than the bidding limit 
            if limit == '0':
                if request.user != get_product.last_user_bid:
                    return Response(
                        {'error': 'last user bid only should stop the automatic bidding'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                get_product.bidding_limit = 0
                get_product.save()

                # user serializer
                user_serializer = UserDataSerializer(get_product.last_user_bid)

                return Response(
                    {
                        'price': get_product.price,
                        'limit': get_product.bidding_limit,
                        'user': user_serializer.data
                    }
                )

            elif limit <= get_product.price or limit <= get_product.bidding_limit:
                return Response(
                    {'error': 'your limit should be greater than product price and product bidding limit'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            else: 
                # limit > get_product.price and limit > get_product.bidding_limit:
                get_product.last_user_bid = request.user
                get_product.price += 1 
                get_product.bidding_limit = limit

                get_product.save()

                # user serializer 
                user_serializer = UserDataSerializer(get_product.last_user_bid)
                return Response(
                    {
                        'new_price': get_product.price,
                        'limit': limit,
                        'user': user_serializer.data
                    },
                    status=status.HTTP_201_CREATED
                    
                )

        else:
            return Response(
                {'error': 'user should put new price or bidding limit'},
                status=status.HTTP_400_BAD_REQUEST
            )

class AutomaticBiddingProductAPI(APIView):
    
    permission_classes = (permissions.AllowAny,)

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
    queryset = Product.objects.filter(is_fixed=True, in_stock__gte=1)
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)

class VariablePriceProducts(ListAPIView):
    queryset = Product.objects.filter(is_fixed=False,in_stock__gte=1)
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)

class LatestProducts(ListAPIView):
    queryset = Product.objects.order_by('-created_at').filter(in_stock__gte=1)
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)

class HighPriceProducsts(ListAPIView):
    queryset = Product.objects.order_by('-price').filter(in_stock__gte=1)
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)

class LowPriceProducts(ListAPIView):
    queryset = Product.objects.order_by('price').filter(in_stock__gte=1)
    serializer_class = ProductSerializer
    permissions = (permissions.AllowAny,)
    
class SearchByCategory(APIView):
    
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            category = Category.objects.get(id=request.data['id'])
        except Category.DoesNotExist:
            return Response(
                {'error': 'category does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        queryset = category.products.filter(in_stock__gte=1)
        product_serializer = ProductSerializer(queryset, many=True)
        return Response(product_serializer.data, status=status.HTTP_200_OK)

class SearchBySubCategory(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            sub_category = SubCategory.objects.get(id=request.data['id'])
        except SubCategory.DoesNotExist:
            return Response(
                {'error': 'sub category does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        queryset = sub_category.products.filter(in_stock__gte=1)
        product_serializer = ProductSerializer(queryset, many=True)
        return Response(product_serializer.data, status=status.HTTP_200_OK)

class SearchByName(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        if request.data.get('name'):        
            products = Product.objects.filter(name__icontains=request.data['name'], in_stock__gte=1)
            product_serializer = ProductSerializer(products, many=True)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'please add param for category name '},
                status=status.HTTP_400_BAD_REQUEST
            )

class EndProductDuration(APIView):
    def post(self, request, product_id):
        
        # check if the product exist
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {'error': 'product is not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if request.user == product.owner:
            product.duration = datetime.datetime.now()
            product.save()

            if product.last_user_bid:
                asyncio.run(send_single_message(product.last_user_bid, 'تهانينا لك, لقد فزت بالمزاد ويجب عليك التوجه الي سلة المشتريات الخاصة بحسابك الشخصي'))
                get_cart, _ = Cart.objects.get_or_create(user=product.last_user_bid)

                # add product to the cart item 
                CartItem.objects.create(
                    product=product,
                    quantity=1,
                    cart=get_cart
                )
                
            product_serializer = ProductSerializer(product)
            return Response(
                product_serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'user should be the owner of the product'},
                status=status.HTTP_400_BAD_REQUEST
            )
###########################
#### RateProduct APIS #####
###########################

class RequestRateProduct(CreateAPIView):
    '''
        name: name of the product
        description: description of the product
        images : one or more than one images
        uploaded_photo: "True" or "False"
        category: category id
    '''
    serializer_class = CreateRateProductSerializer

    #
    # def perform_create(self, serializer):
    #     rate_product = serializer.save(owner=self.request.user)
    #     if "images" in self.request.data:
    #         images = dict((self.request.data).lists())['images']
    #         for image in images:
    #             ProductRateImage.objects.create(
    #                 rate_product=rate_product,
    #                 img=image
    #             )
    #         print(self.request.user)
    def post(self, request):
        rate_product = self.serializer_class(data=request.data)
        ip_address = get_client_ip(request)
        data = []
        if rate_product.is_valid(raise_exception=True):
            rate_product.save(owner=self.request.user)
            get_rate_product = RateProduct.objects.get(id=int(rate_product.data['id']))
            images = dict((self.request.data))['images']
            for image in images:
                product_rate_image = ProductRateImage(
                    rate_product=get_rate_product,
                    img=image
                )
                product_rate_image.save()
            get_rate_product = RateProduct.objects.get(id=int(rate_product.data['id']))
            if get_rate_product.uploaded_photo == True:
                get_rate_product.price = get_rate_product.category.uploaded_price + (get_rate_product.category.uploaded_price * 0.04)
                get_rate_product.save()
            else:
                get_rate_product.price = get_rate_product.category.msawm_team_price + (get_rate_product.category.msawm_team_price * 0.04)
                get_rate_product.save()

            # get_rate_product.price = get_rate_product.calculate_user_pay()
            # print(get_rate_product.price)
            # get_rate_product.save()
            '''
            Payment operation for Rate Product Request
            '''
            posted = {
                'terminalId': secrets.TERMINAL_ID,
                'password': secrets.PASSWORD,
                'secret': secrets.MERCHANT_SECRET_KEY,
                'currency': secrets.CURRENCY,
                'country': secrets.COUNTRY,
                'action': secrets.ACTION,
                'trackid': str(get_rate_product.id),
                'customerEmail': request.user.email,
                'merchantIp': ip_address,
                'amount': str(get_rate_product.price),
                'udf1': "Request Rate Product",
                'udf2': "http://581f6f004c50.ngrok.io/payment/payment_receipt/",
                "udf3": request.user.id,
            }
            hashSequence = posted['trackid'] + "|" + posted["terminalId"] + "|" + posted["password"] + "|" + posted["secret"] + "|" + posted["amount"] + "|" + posted["currency"]
            hashVarsSeq = hashSequence.split('|')
            hash = hashlib.sha256(hashSequence.encode()).hexdigest()
            posted["requestHash"] = hash
            name = json.dumps(posted)
            apiURL = "https://payments-dev.urway-tech.com/URWAYPGService/transaction/jsonProcess/JSONrequest"
            response = requests.request("POST", apiURL, data=name)
            res = response.json()
            pymentID = json.dumps(res["payid"])
            target_url = json.dumps(res["targetUrl"])
            redirectURL = (target_url + "?paymentid=" + pymentID).replace('"', '')
            if 'null' in redirectURL:
                return Response(
                    {'error': 'there is something wrong, please try again'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            data.append({"data":rate_product.data,"payment_url": redirectURL})
            return Response(
                data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(rate_product.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllRatedProduct(APIView):
    
    def get(self, request):
        queryset = RateProduct.objects.filter(owner=self.request.user, is_rated=True)
        serializer = ListRateProductSerializer(queryset, many=True)
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )