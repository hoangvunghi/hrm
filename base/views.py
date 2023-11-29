from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserRegisterSerializer, UserAccountSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from .models import UserAccount,Attendance,Leave
from base.permission import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.http import Http404, HttpResponseForbidden
from django.http import HttpResponse


@api_view(["POST",])
def logout_user(request): 
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response({"Message": "You are logged out"}, status=status.HTTP_200_OK)

@api_view(["POST"])
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

@api_view(["POST"])
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


# def delete_data_if_user_quitte(user_id):
#     # try:
#         user = UserAccount.objects.get(user_id=user_id)

#         if user.status == 'quitte':
#             Attendance.objects.filter(employee_id=user).delete()
#             Leave.objects.filter(employee=user).delete()
        
        # print(f"Deleted data for user {user.email} because the status is 'quitte'")
        # else:
            # return HttpResponse(f"No data deletion. User {user.email} has a status other than 'quitte'")
    # except UserAccount.DoesNotExist:
        # raise Http404(f"User with ID {user_id} does not exist.")
    # except Exception as e:
        # raise HttpResponseForbidden(f"Error: {str(e)}")



@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_employee(request, pk):
    employee = get_object_or_404(UserAccount, user_id=pk)

    if request.method == 'DELETE':
        employee.delete()
        delete_data_if_user_quitte(pk)
        Attendance.objects.filter(employee_id=pk).delete()
        Leave.objects.filter(employee=pk).delete()
        return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def create_employee(request):
    serializer = UserAccountSerializer(data=request.data)
    if serializer.is_valid():
        user_id = request.data.get('user_id', None)

        if UserAccount.objects.filter(user_id=user_id).exists():
            return Response({"error": "User with this user_id already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def update_employee(request, pk):
    employee = get_object_or_404(UserAccount, user_id=pk)

    if request.method == 'PATCH':
        serializer = UserAccountSerializer(employee, data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('user_id', None)
            if user_id is not None and not UserAccount.objects.filter(user_id=user_id).exists():
                return Response({"error": "Employee not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    



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
        raise Http404(f"User with ID {user_id} does not exist.")
    except Exception as e:
        raise HttpResponseForbidden(f"Error: {str(e)}")



