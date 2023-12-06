from django.http import Http404, HttpResponse, HttpResponseForbidden
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserRegisterSerializer, UserAccountSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from .models import UserAccount, Attendance, Leave
from base.permission import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
import re
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
# from django.shortcuts import redirect


# def check_user(request):
#     if request.user.is_superuser:
#         return redirect('admin:index')  

#     if request.user.is_staff and not request.user.is_superuser:
#         return redirect('hr_admin:index')

#     return redirect('user')

        


@api_view(["POST",])
def find_employee(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    employees=UserAccount.objects.filter(
        Q(username__icontains=q) |
        Q(name__icontains=q)|
        Q(first_name__icontains=q)|
        Q(last_name__icontains=q)
    ) 
    # serializer = UserAccountSerializer(employee, many=True)
    # return Response(serializer.data)
    usernames = employees.values_list('username', flat=True)
    return Response({'usernames': list(usernames)})

@api_view(["GET",])

def a(request):
    return Response("hello")
# @api_view(["POST",])
# def logout_user(request): 
#     if request.method == "POST":
#         request.user.auth_token.delete()
#         return Response({"Message": "You are logged out"}, status=status.HTTP_200_OK)

@api_view(["POST"])
def user_register_view(request):
    if request.method == "POST":
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        username = request.data.get('username', '').lower()
        password = request.data.get('password', '')
        email=request.data.get("email","").lower()
        if not username:
            return Response('Username is required')
        if not password:
            return Response('Password is required')
        if not email:
            return Response("Email is required")
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            return Response("Invalid email format.")
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

@api_view(["POST"])
def user_login_view(request):
    if request.method == "POST":
        try:
            username = request.data.get('username', '').lower()
            password = request.data.get('password', '')

            if not username or not password:
                return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                try:
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                except TokenError as e:
                    if isinstance(e, InvalidToken) and e.args[0] == 'Token has expired':
                        return Response({'error': 'Access token has expired. Please refresh the token.'}, status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


                data = {
                    'response': 'Login successful',
                    'username': user.username,
                    'email': user.email,
                    'token': {
                        'refresh': str(refresh),
                        'access': access_token
                    }
                }

                print("Is admin:", user.is_superuser)
                print("Is staff:", user.is_staff)

                return Response(data)
            else:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def change_password(request, pk):
    if request.method == 'POST':
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({'success': False, 'message': 'New password cannot be empty.'})

        UserAccount = get_user_model()
        try:
            user_account = UserAccount.objects.get(user_id=pk)
        except UserAccount.DoesNotExist:
            return Response({'success': False, 'message': 'User not found.'})

        if not check_password(current_password, user_account.password):
            return Response({'success': False, 'message': 'Current password is incorrect.'})

        user_account.set_password(new_password)
        user_account.save()
        return Response({'success': True, 'message': 'Password changed successfully.'})
    return Response({'success': False, 'message': 'Invalid request method.'})

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_employee(request, pk):
    try:
        employee = UserAccount.objects.get(user_id=pk)
    except UserAccount.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        employee.delete()
        delete_data_if_user_quitte(pk)
        Attendance.objects.filter(employee_id=pk).delete()
        Leave.objects.filter(employee=pk).delete()
        return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


def is_valid(data):
    errors= {}
    username = data.get('username', '').lower()
    password = data.get('password', '')
    email=data.get("email","").lower()
    phone_number=data.get("phone_number")
    if not username:
        errors['username']= 'Username is required'
    if not password:
        errors['password']= 'Password is required'
    if not email:
        errors['email']= "Email is required"
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        errors['email']= "Invalid email format."
    if not phone_number:
        errors['phone_number']= "Phone number is required"
    phone_regex = r'^[0-9]$'
    if not re.match(phone_regex, phone_number) or len(phone_number)!=10:
        errors['email']= "Phone number email format."
    return errors

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def create_employee(request):
    errors= is_valid(request.data)
    if len(errors):
        return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
        
    serializer = UserAccountSerializer(data=request.data)
    
    if serializer.is_valid():
        user_id = request.data.get('user_id', None)

        if UserAccount.objects.filter(user_id=user_id).exists():
            return Response({"error": "User with this user_id already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def validate_account_to_update(obj, data):
    errors= {} 
    for key in data:
        value= data[key]
        if key in ['username', 'user_id']:
            errors[key]= f"{key} khong duoc phep thay doi"
        if key=='email' and UserAccount.objects.filter(email= value).exclude(user_id= obj.user_id).exists():
             errors[key]= f"email ({value}) da ton tai"         
    return errors 

def account_update(obj, validated_data):
    for key in validated_data:
        setattr(obj, key, validated_data[key])
        print(getattr(obj, key))
    obj.save()


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def update_employee(request, pk):
    print(request.data)
    try:
        employee = UserAccount.objects.get(user_id=pk)
    except UserAccount.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
        errors= validate_account_to_update(employee, request.data)
        if len(errors):
            return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
        account_update(employee, request.data)
        return Response({"messeger": "Cap nhat thanh cong", "data": str(employee.__dict__)}, status=status.HTTP_200_OK)
        
        # serializer = UserAccountSerializer(employee, data=request.data, partial=True)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        
        # error= serializer.errors
        # error['messesge']= "ssssss"
        # return Response(error, status=status.HTTP_400_BAD_REQUEST)
    
    


def delete_data_if_user_quitte(user_id):
    try:
        user = UserAccount.objects.get(user_id=user_id)

        if user.status == 'quitte':
            Attendance.objects.filter(employee_id=user).delete()
            Leave.objects.filter(employee=user).delete()
            return HttpResponse(f"Deleted data for user {user.email} because the status is 'quitte'")
        else:
            return HttpResponse(f"No data deletion. User {user.email} has a status other than 'quitte'")
    except UserAccount.DoesNotExist:
        return Response(f"User with ID {user_id} does not exist.")
    except Exception as e:
        return Response(f"Error: {str(e)}")
    
    
    


