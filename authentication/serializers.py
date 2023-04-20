from rest_framework import serializers
from authentication.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username']

    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username", "")

        if not username.isalnum():
            raise serializers.ValidationError(
                'the username is not valid, should only contain alphanumeric')
        return attrs

    def create(self, validated_data):
            return User.objects.create_user(**validated_data)


class EmailverificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


# class LoginSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(max_length=555, min_length=3)
#     password = serializers.CharField(max_length=68, min_length=6, write_only=True)
#     username = serializers.CharField(max_length=255, min_length=3, read_only=True)
#     tokens = serializers.SerializerMethodField()

#     def get_tokens(self, obj):
#         user = User.objects.get(email=obj['email'])
#         print('user is ####', user)

#         return {
#             'refresh': user.tokens()['refresh'],
#             'access': user.tokens()['access']
#         }

#     class Meta:
#         model = User
#         fields = ['email', 'password', 'username', 'tokens']
    
#     print(tokens)

#     def validate(self, data):
#         # user=User.objects.all()
#         # print('user is',user)
#         # email = data.get('email')
#         # password = data.get('password')
       
#         user = authenticate( username=data.get('email', ''),
#                             password=data.get('password', ''))
#         # password = data.get('password')
#         email=data.get('email')
#         filtered_user_by_email = User.objects.filter(email=email)
#         # print(password, email)
#         # user = auth.authenticate(email='mel575725@gmail.com', password='q1w2e3r4')
#         if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
#             raise AuthenticationFailed(
#                 detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)
#         # print(user)
#         # print('#######################################################################################')
        
#         # import pdb
#         # pdb.set_trace()
#         if not user:
#             raise AuthenticationFailed('Invalid credentials bla bla, try again')
#         if not user.is_active:
#             raise AuthenticationFailed("Account disabled contact administartor")    
#         if not user.is_verified:
#             raise AuthenticationFailed("Kindly verify your account")       
        
#         return {    
#             'email': user.email,
#             'username': user.username,
#             'tokens': user.tokens
#         }
        
#         return super().validate(attrs)



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)