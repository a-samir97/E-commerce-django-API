
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User
from products.models import Product, RateProduct
from comments.models import Comment
from reviews.models import Review

from . import serializers
from .permissions import IsAdmin

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
    serializer_class = serializers.DashboardProductSerializer
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