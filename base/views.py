from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import UserAccount

@api_view(["POST",])
def logout_user(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response({"Message": "You are logged out"}, status=status.HTTP_200_OK)

@api_view(["POST",])
def user_register_view(request):
    if request.method == "POST":
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = 'Account has been created'
            data['username'] = account.username
            data['email'] = account.email

            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        else:
            data = serializer.errors
        return Response(data)
    

@api_view(["POST",])
def user_login_view(request):
    if request.method == "POST":
        try:
            username = request.data.get('username', '').lower()
            password = request.data.get('password', '')

            if not username:
                raise ValueError('Username is required')
            if not password:
                raise ValueError('Password is required')

            data = {}
            try:
                user = UserAccount.objects.get(username=username)
            except UserAccount.DoesNotExist:
                data['error'] = 'User does not exist'
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                data['response'] = 'Login successful'
                data['username'] = user.username
                data['email'] = user.email

                refresh = RefreshToken.for_user(user)
                data['token'] = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            else:
                data['error'] = 'Invalid username or password'
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)

            return Response(data)
        except ValueError as e:
            data = {'error': str(e)}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
