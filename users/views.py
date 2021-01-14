from django.contrib.auth import authenticate

from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import MultiPartParser

from .models import User
from .serializers import( 
    LoginSerializer, 
    SignupSerializer,
    UpdateUserSerializer,
    UserDataSerializer
)

from reviews.serializers import ReviewSerializer
from products.serializers import ProductSerializer

import random
import asyncio
from utils import send_single_message

class LoginAPIView(GenericAPIView):
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
            if user.is_verified:
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
                    {'error': "user is not verified"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'error': 'make sure about your email and your password please'},
                status=status.HTTP_404_NOT_FOUND
            )

class SignupAPIView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignupSerializer

    def post(self, request):
        user_serializer = SignupSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            user.pass_code = random.randint(1000,9999)
            asyncio.run(send_single_message(user, 'Verification code %s' %(user.pass_code,)))
            user.save()
            return Response(
                {'data': user_serializer.data},
                status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                {'error': user_serializer.errors}
            )

class Verification(APIView):
    '''
        verification user 
        params:
            - code : pass code 
    '''
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        
        if not request.data.get('code'):
            return Response(
                {'error': 'please add your pass code'}
            )
        try:
            pass_code = int(request.data.get('code'))
        except:
            return Response(
                {'error': 'please enter valid code'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            get_user = User.objects.get(pass_code=pass_code)
            get_user.is_verified = True
            get_user.pass_code = 0
            get_user.save()
            return Response(
                {'data': 'user verified'},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'you have entered wrong pass code'},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UpdateUserSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            self.perform_update(serializer)
            user_serializer = UserDataSerializer(instance=instance)
            return Response(
                {'data': user_serializer.data},
                status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

class LogoutAPIView(APIView):
    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(
            status=status.HTTP_200_OK
        )

class ChangePassword(APIView):
    def post(self, request):
        current_user = request.user
        # check if the old password is correct 
        old_password = request.data['old_password']
        user = authenticate(request=request, username=current_user.email, password=old_password)

        if user:
            user.set_password(request.data['new_password'])
            user.save()
            return Response(
                {'data': 'password is changed successfully'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'incorrect password'},
                status=status.HTTP_400_BAD_REQUEST
            )

class GetCurrentUserReviews(ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        return self.request.user.reviews.filter(approved=True)

class GetUserReviews(APIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.AllowAny,)
    def get(self, request, user_id):
        try:
            get_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'user is not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        reviews = get_user.reviews.filter(approved=True)
        user_reviews = ReviewSerializer(reviews, many=True)
        return Response(
            {'data': user_reviews.data},
            status=status.HTTP_200_OK
        )

class GetUserData(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = (permissions.AllowAny,)

class GetUserProduct(APIView):
    def get(self, request):
        queryset = self.request.user.products.all()
        serializer_class = ProductSerializer(queryset, many=True)
        return Response(
            {'data': serializer_class.data},
            status=status.HTTP_200_OK
        )

class ToggleFollow(APIView):
    def post(self, request, user_id):

        # check if user exists
        try:
            get_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'user is not exists'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # check if user in following list 
        if get_user in request.user.following.all():
            request.user.following.remove(get_user)
            request.user.save()
            return Response(
                {'data': '%s unfollowed %s' % (request.user.first_name, get_user.first_name)}
            )
        else:
            request.user.following.add(get_user)
            request.user.save()
            return Response(
                {'data': '%s followed %s' % (request.user.first_name, get_user.first_name)}
            )

class FollowingUsers(APIView):
    def get(self, request):
        following_users = request.user.following.all()
        serializer = UserDataSerializer(following_users, many=True)
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )