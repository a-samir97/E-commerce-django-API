from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from rest_framework.generics import ListAPIView, GenericAPIView, UpdateAPIView, CreateAPIView
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User
from products.models import Product, RateProduct
from comments.models import Comment
from reviews.models import Review
from categories.models import Category, SubCategory

from products.serializers import ProductSerializer
from categories.serializers import CategorySerializer, SubCategorySerializer
from users.serializers import LoginSerializer, UserDataSerializer

from . import serializers
from .permissions import IsAdmin


########################################
####### Login API in Dashboard #########
########################################

class DashboardLoginAPIView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    
    def post(self, request):
        
        username = User.objects.filter(phone_number=request.data['email']).first()
        if not username:
            username = User.objects.filter(email=request.data['email']).first()

            if not username:
                return Response(
                    {'error': 'your email or phone number is not exist in our database'},
                    status=status.HTTP_404_NOT_FOUND
                )

        user = authenticate(request, username=username.email, password=request.data['password'])
        
        if user:
            
            if user.user_type == 'U':
                return Response(
                    {'error': 'you are not admin to login to dashboard'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user_serialzer = LoginSerializer(data=request.data)
            if user_serialzer.is_valid():
                user_token, _ = Token.objects.get_or_create(user=user)
                serializer = UserDataSerializer(user)
                return Response(
                    {
                        "token": user_token.key,
                        "user": serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': user_serialzer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'error': 'make sure about your email and your password please'},
                status=status.HTTP_404_NOT_FOUND
            )

########################################
######### User APIs in Dashboard ######
########################################

class ListAllUserAPI(ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.DashboardUserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

class DeleteUserAPI(APIView):

    permission_classes = (permissions.IsAuthenticated, IsAdmin)

    def delete(self, request, user_id):

        try:
            get_user = User.objects.get(id=user_id)
            get_user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except User.DoesNotExist:
            return Response(
                {'error': 'user does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

class ToggleBlockUserAPI(APIView):

    permission_classes = (permissions.IsAuthenticated, IsAdmin)

    def post(self, request, user_id):
        try:
            get_user = User.objects.get(id=user_id)
            if get_user.is_blocked:
                get_user.is_blocked = False
            else:
                get_user.is_blocked = True
            get_user.save()
            return Response(status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {'error': 'user does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

class ToggleGoldenUserAPI(APIView):

    permission_classes = (permissions.IsAuthenticated, IsAdmin)

    def post(self, request, user_id):
        try:
            get_user = User.objects.get(id=user_id)
            if get_user.is_gold:
                get_user.is_gold = False
            else:
                get_user.is_gold = True
            get_user.save()
            return Response(status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {'error': 'user does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

########################################
######### Product APIs in Dashboard ####
########################################

class ListAllProductAPI(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

class DeleteProductAPI(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

    def delete(self, request, product_id):

        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist:
            return Response(
                {'error': 'product does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

class UpdateProductAPI(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

class ListCommentsForProduct(APIView):

    permission_classes = (permissions.IsAuthenticated, IsAdmin)

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            all_comments = product.comments.all()
            comments_serializer = serializers.DashboardCommentSerializer(all_comments, many=True)
            return Response(
                comments_serializer.data,
                status=status.HTTP_200_OK
            )

        except Product.DoesNotExist:
            return Response(
                {'error': 'product does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

class DeleteCommentAPI(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

    def delete(self, request, comment_id):

        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist:
            return Response(
                {'error': 'comment does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
    

########################################
##### RateProduct APIs in Dashboard ####
########################################

class ListAllRateProductAPI(ListAPIView):
    queryset = RateProduct.objects.all()
    serializer_class = serializers.DashboardRateProductSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

class CreateRatingForProduct(APIView):
    '''
        params:
            price : integer
    '''
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

    def post(self, request, rate_product_id):

        try:
            rate_product = RateProduct.objects.get(id=rate_product_id)
            if request.data.get('price'):
                rate_product.price = request.data['price']
                rate_product.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'please add price to the product'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except RateProduct.DoesNotExist:
            return Response(
                {'error': 'Product does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

########################################
##### Reviews APIs in Dashboard ########
########################################

class ListAllReviews(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.DashboardReviewSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

class ToggleApproveReview(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

    def post(self, request, review_id):
        try:
            review_object = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response(
                {'error': 'review id is not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        if review_object.approved:
            review_object.approved = False
            review_object.save()
            return Response({'approved': review_object.approved},status=status.HTTP_200_OK)
        else:
            review_object.approved = True
            review_object.save()
            return Response({'approved': review_object.approved},status=status.HTTP_200_OK)

class DeleteReviewAPI(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

    def delete(self, request, review_id):
        try:
            review_object = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response(
                {'error': 'review id is not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        review_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

########################################
##### Categories APIs in Dashboard #####
########################################

class ListAllCategory(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

class AddCategoryAPI(CreateAPIView):
    '''
        params:
            name_en: category name in English 
            name_ar: category name in Arabic
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

class AddSubcategoryAPI(CreateAPIView):
    '''
        params:
        name_en: subcategory name in English
        name_ar: subcategory name in Arabic 
        category: category id 
    '''
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
