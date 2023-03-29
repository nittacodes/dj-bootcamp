from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import RegisterSerializer

class RegisterView(generics.GenericAPIView):

    serializer_class=RegisterSerializer    
    def post(self, request):
        user = request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)


