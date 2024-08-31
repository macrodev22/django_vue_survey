from django.shortcuts import render
from django.http import response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView,ListCreateAPIView
from .forms import RegisterForm,LoginForm
from .models import User
from .serializers import UserSerializer
import datetime

# Create your views here.

class AuthRegister(APIView):
    def post(self, request):
        form = RegisterForm(request.data)
        if form.is_valid():
            # Create new user
            cleaned_data = form.cleaned_data
            user = User(email=cleaned_data['email'], name=cleaned_data['fullname'])
            user.set_password(cleaned_data['password'])

            try:
                user.save()
                #TODO: add a cookie
                serializer = UserSerializer(user)
                return Response({ "user": serializer.data, "token": user.createToken() }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({ "error": str(e) }, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(form.errors)
    
class AuthLogin(APIView):
    def post(self, request):
        form = LoginForm(request.data)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            user = User.objects.get(email=cleaned_data['email'])

            if user.check_password(cleaned_data['password']):
                # TODO: Add a cookie
                serializer = UserSerializer(user)
                return Response({
                    "user": serializer.data,
                    "token": user.createToken()
                }, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({ "message": "Invalid username or password" }, status=status.HTTP_401_UNAUTHORIZED)

        # Invalid data 
        else:
            return Response(form.errors)