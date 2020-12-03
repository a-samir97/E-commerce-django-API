from django.contrib.auth import authenticate

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import LoginSerializer, SignupSerializer

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
                    {"token": user_token.key},
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


class LogoutAPIView(APIView):
    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(
            status=status.HTTP_200_OK
        )