from rest_framework import serializers

from .models import User

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    email = serializers.CharField(
        required=True,
        style={'placeholder': 'Email'}
    )
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'])

        user.set_password(validated_data['password'])
        user.save()
        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'email', 'phone_number',
            'company_name', 'company_address',
            'location', 'gender', 'img', 'local_visa',
            'global_visa', 'bank_name')

class UserDataSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name',
            'email', 'phone_number',
            'company_name', 'company_address',
            'location', 'gender', 'is_gold', 'img'
        )
    def get_img(self, obj):
        if obj.img:
            return obj.img.url
        else:
            None