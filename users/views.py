from django.contrib.auth import authenticate

from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.generics import UpdateAPIView

from .models import User
from .serializers import( 
    LoginSerializer, 
    SignupSerializer,
    UpdateUserSerializer,
    UserDataSerializer
)

from reviews.serializers import ReviewSerializer

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
            user_serialzer = LoginSerializer(data=request.data)
            if user_serialzer.is_valid():
                user_token, _ = Token.objects.get_or_create(user=user)

                return Response(
                    {
                        "token": user_token.key,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "phone_number": user.phone_number,
                        'gender': user.gender,
                        'is_gold': user.is_gold,
                        'id': user.id
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

class SignupAPIView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignupSerializer

    def post(self, request):
        user_serializer = SignupSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(
                {'data': user_serializer.data},
                status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                {'error': user_serializer.errors}
            )

class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer

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

class GetUserReviews(ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        return self.request.user.reviews.filter(approved=True)

class GetUserData(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDataSerializer