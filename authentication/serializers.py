from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model=User
        fields=[ 'email', 'password']

    def validate(self, attrs):
        email= attrs.get("email", "")
        username=attrs.get("username", "")
        

        if not username.isalnum():
            raise serializers.ValidationError(' the username is not valid, should only contain alphanumeric')
        return attrs

    def create(self, validated_data):
            return User.objects.create_user(**validated_data)   


class EmailverificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model=User
        fields=['token']

class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=555, min_length=3)
    password=serializers.CharField(max_length=68, min_length=6)
    

    def validate(self, attrs):
        email=attrs.get('email', '')
        password=attrs.get('password', '')

        user=auth.authenticate(email='email', password='password')

        if not user.is_active:
            raise AuthenticationFailed("Account disabled contact administartor")
        if not user.is_verified:
            raise AuthenticationFailed("Kindly verify your account")
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        return super().validate(attrs)

        return (
            'email': user.email
            'username': user.username
            'token':
        )