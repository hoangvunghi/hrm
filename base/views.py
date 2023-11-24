from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserRegisterSerializer,UserAccountSerializer
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
    
    
#Thêm nhân viên
@api_view(['POST'])
def add_employee(request):
    if request.method == 'POST':
        serializer = UserAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#sửa thông tin nhân viên
@api_view(['PUT'])
def update_employee(request, pk):
    try:
        employee = UserAccount.objects.get(user_id=pk)
    except UserAccount.DoesNotExist:
        return Response({"message": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserAccountSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
#xóa nhân viên
@api_view(['DELETE'])
def delete_employee(request, pk):
    try:
        employee = UserAccount.objects.get(user_id=pk)
    except UserAccount.DoesNotExist:
        return Response({"message": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        employee.delete()
        return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


