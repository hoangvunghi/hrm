from django.http import Http404, HttpResponse, HttpResponseForbidden,JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserRegisterSerializer, UserAccountSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from .models import UserAccount, Attendance, Leave
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
import re,json
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.core.paginator import Paginator,EmptyPage
from drf_spectacular.utils import extend_schema
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
        Q(last_name__icontains=q)|
        Q(position__position_name__icontains=q)| 
        Q(last_name__icontains=q)
    )
    # serializer = UserAccountSerializer(employee, many=True)
    # return Response(serializer.data)
    usernames = employees.values_list('username', flat=True)
    return Response({'usernames': list(usernames),
                     "status":status.HTTP_200_OK},
                    status=status.HTTP_200_OK)


@api_view(["GET",])
def a(request):
    return Response("hello")


# @api_view(["POST"])
# def user_register_view(request):
#     if request.method == "POST":
#         serializer = UserRegisterSerializer(data=request.data)
#         data = {}
#         username = request.data.get('username', '').lower()
#         password = request.data.get('password', '')
#         email=request.data.get("email","").lower()
#         if not username:
#             return Response('Username is required')
#         if not password:
#             return Response('Password is required')
#         if not email:
#             return Response("Email is required")
#         email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#         if not re.match(email_regex, email):
#             return Response("Invalid email format.")
#         if serializer.is_valid():
#             account = serializer.save()
            
#             data['response'] = 'Account has been created'
#             data['username'] = account.username
#             data['email'] = account.email

#             refresh = RefreshToken.for_user(account)
#             data['token'] = {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token)
#             }
#         else:
#             data = serializer.errors
#         return Response(data)

@api_view(["POST"]) 
def user_login_view(request):
    if request.method == "POST":
        try:
            username = request.data.get('username', '').lower()
            password = request.data.get('password', '')

            if not username or not password:
                return Response({'error': 'Username and password are required',
                                 "status":status.HTTP_400_BAD_REQUEST}, 
                                status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                try:
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                except TokenError as e:
                    if isinstance(e, InvalidToken) and e.args[0] == 'Token has expired':
                        return Response({'error': 'Access token has expired. Please refresh the token.',
                                         "status":status.HTTP_401_UNAUTHORIZED}, 
                                        status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        return Response({'error': 'Invalid token.',
                                         "status":status.HTTP_401_UNAUTHORIZED},
                                        status=status.HTTP_401_UNAUTHORIZED)
                data = {
                    'response': 'Login successful',
                    'username': user.username,
                    'email': user.email,
                    'token': {
                        'refresh': str(refresh),
                        'access': access_token,
                    },
                    "status":status.HTTP_200_OK,

                }

                print("Is admin:", user.is_superuser)
                print("Is staff:", user.is_staff)

                return Response(data,status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid username or password',
                                 "status":status.HTTP_401_UNAUTHORIZED}, 
                                status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e),
                             "status":status.HTTP_400_BAD_REQUEST}, 
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def change_password(request, pk):
    if request.method == 'POST':
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({'success': False, 'message': 'New password cannot be empty.',
                             "status":status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

        UserAccount = get_user_model()
        try:
            user_account = UserAccount.objects.get(user_id=pk)
        except UserAccount.DoesNotExist:
            return Response({'success': False, 'message': 'User not found.',
                             "status":status.HTTP_404_NOT_FOUND}
                            ,status=status.HTTP_404_NOT_FOUND)

        if not check_password(current_password, user_account.password):
            return Response({'success': False, 'message': 'Current password is incorrect.',
                             "status":status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

        user_account.set_password(new_password)
        user_account.save()
        return Response({'success': True, 'message': 'Password changed successfully.',
                         "status":status.HTTP_200_OK},status=status.HTTP_200_OK)
    return Response({'success': False, 'message': 'Invalid request method.',
                     "status":status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_employee(request, pk):
    try:
        employee = UserAccount.objects.get(user_id=pk)
    except UserAccount.DoesNotExist:
        return Response({"error": "Employee not found",
                         "status":status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        employee.delete()
        delete_data_if_user_quitte(pk)
        Attendance.objects.filter(employee_id=pk).delete()
        Leave.objects.filter(employee=pk).delete()
        return Response({"message": "Employee deleted successfully",
                         "status":status.HTTP_204_NO_CONTENT}, 
                        status=status.HTTP_204_NO_CONTENT)


def is_valid_type(request): 
    errors = {}
    required_fields = ['username', 'password', 'email', 'phone_number', 
                       'last_name', 'first_name',"position_id","date_of_birth",
                       "attendance_id","check_in_time","check_out_time","status",
                       "department_name","manager","leave_type","employee","start_date",
                       "end_date","reason","position_name","organization_name","tax_id","number_of_employees",
                       "registration_employees","cost_center","phone","tax","email","address_stress",
                       "city","zip_postalcode","country","note"
                       ]
    for field in required_fields:
        if field in request.data and not request.data[field]:
            errors[field] = f'{field.capitalize()} is required'
    if 'username' in request.data and not request.data['username']:
        errors['username'] = 'Username is required'
    if 'password'  in request.data and not request.data['password']:
        errors['password'] = 'Password is required'
    if 'email'  in request.data and not request.data['email']:
        errors['email'] = 'Email is required'
    else:
        new_email = request.data['email'].lower()
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, new_email):
            return Response({"error": "Invalid email format","status":status.HTTP_400_BAD_REQUEST}, 
                            status=status.HTTP_400_BAD_REQUEST)
    if 'phone_number'  in request.data and not request.data['phone_number']:
        errors['phone_number'] = 'Phone number is required'
    else:
        phone_number = request.data['phone_number']
        phone_regex = r'^[0-9]+$'
        if not re.match(phone_regex, phone_number) or len(phone_number) != 10:
            errors['phone_number'] = 'Invalid phone number format.'

    if errors:
        return Response(errors,{"status":status.HTTP_400_BAD_REQUEST} 
                        ,status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Data is valid","status":status.HTTP_200_OK}
                    , status=status.HTTP_200_OK)

# def is_valid_type(request):
#     errors = {}
#     required_fields = ['username', 'password', 'email', 'phone_number', 
#                        'last_name', 'first_name',"position_id","date_of_birth",
#                        "attendance_id","check_in_time","check_out_time","status",
#                        "department_name","manager","leave_type","employee","start_date",
#                        "end_date","reason","position_name","organization_name","tax_id","number_of_employees",
#                        "registration_employees","cost_center","phone","tax","email","address_stress",
#                        "city","zip_postalcode","country","note"
#                        ]
    




@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def create_employee(request):
    serializer = UserAccountSerializer(data=request.data)
    # is_valid_type(serializer.data)
    if 'username' in request.data and not request.data['username']:
        return Response({"message":"Username is required"}, status=status.HTTP_400_BAD_REQUEST)
    if 'password' in request.data and not request.data['password']:
        return Response({"message":"Password is required"}, status=status.HTTP_400_BAD_REQUEST)
    if 'email' in request.data and not request.data['email']:
        return Response({"message":"Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        new_email = request.data['email']
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, new_email):
            return Response({"message": "Invalid email format", "status":status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    if 'phone_number' in request.data and not request.data['phone_number']:
        return Response({"message":"Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        phone_number = request.data['phone_number']
        phone_regex = r'^[0-9]+$'
        if not re.match(phone_regex, phone_number) or len(phone_number) != 10:
            return Response({"message":"Invalid phone number format", "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        user_id = request.data.get('user_id', None)

        if UserAccount.objects.filter(user_id=user_id).exists():
            return Response({"error": "User with this user_id already exists",
                             "status":status.HTTP_400_BAD_REQUEST}, 
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"message": "User created successfully",
                         "status":status.HTTP_201_CREATED}, 
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def validate_account_to_update(obj, request):
    errors= is_valid_type(request)
    if len(errors):
        return Response({"error": errors,"status":status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
    for key in request:
        value= request[key]
        if key in ['username', 'user_id']:
            errors[key]= f"{key} not allowed to change"
        if key=='email' and UserAccount.objects.filter(email= value).exclude(user_id= obj.user_id).exists():
             errors[key]= f"The email address ({value}) already exists."         
    return Response({"error":errors,"status":status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST) 

# def validate_account_to_update(obj, request):
#     # errors= is_valid_type(request.data)
#     errors ={}

#     if len(errors):
#         return Response({"error": errors,"status":status.HTTP_400_BAD_REQUEST},
#                         status=status.HTTP_400_BAD_REQUEST)
#     for key in request:
#         value= request[key]
#         if key in ['username', 'user_id']:
#             errors[key]= f"{key} not allowed to change"
#         if key=='email' and UserAccount.objects.filter(email= value).exclude(user_id= obj.user_id).exists():
#              errors[key]= f"The email address ({value}) already exists."         
#     return Response({"error":errors,"status":status.HTTP_400_BAD_REQUEST},
#                     status=status.HTTP_400_BAD_REQUEST) 

def account_update(obj, validated_data):
    for key in validated_data:
        setattr(obj, key, validated_data[key])
        print(getattr(obj, key))
    obj.save()


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def update_employee(request, pk):
    try:
        employee = UserAccount.objects.get(user_id=pk)
    except UserAccount.DoesNotExist:
        return Response({"error": "Employee not found","status":status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
   
        # validate_account_to_update(employee, request.data)
        # if len(errors):
        #     return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer=UserAccountSerializer(employee)
        
        if 'username' in request.data and not request.data['username']:
            return Response({"message":"Username is required"}, status=status.HTTP_400_BAD_REQUEST)
        if 'password' in request.data and not request.data['password']:
            return Response({"message":"Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        if 'email' in request.data and not request.data['email']:
            return Response({"message":"Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        if 'email' in request.data:
            email = request.data['email']
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, new_email):
                return Response({"message": "Invalid email format", "status":status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
        if 'phone_number' in request.data and not request.data['phone_number']:
            return Response({"message":"Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            phone_number = request.data['phone_number']
            phone_regex = r'^[0-9]+$'
            if not re.match(phone_regex, phone_number) or len(phone_number) != 10:
                return Response({"message":"Invalid phone number format", "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        account_update(employee, request.data)
        return Response({"messeger": "update successfully", "data":str(serializer.data),
                            "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        
        # serializer = UserAccountSerializer(employee, data=request.data, partial=True)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        
        # error= serializer.errors
        # error['messesge']= "ssssss"
        # return Response(error, status=status.HTTP_400_BAD_REQUEST)
    


# @extend_schema(responses=UserAccountSerializer)
@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def list_employee(request, pg):
    page_number = request.GET.get('page', pg)
    
    items_per_page = 20
    order_by = request.GET.get('order_by', 'user_id')  
    allowed_order_fields = ['user_id', 'name', 'date_of_hire', '-user_id', '-date_of_hire']

    if order_by not in allowed_order_fields:
        return Response({"error": f"Invalid order_by value. Allowed values are: {', '.join(allowed_order_fields)}",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)

    total_employees = UserAccount.objects.count()

    all_employees = UserAccount.objects.all().order_by(order_by)
    paginator = Paginator(all_employees, items_per_page)
    

    try:
        current_page_data = paginator.page(page_number)
    except EmptyPage:
        return Response({"error": "Page not found",
                         "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = UserAccountSerializer(current_page_data.object_list, many=True)
    serialized_data = serializer.data
    return Response({
        "total_employees": total_employees,
        "current_page": page_number,
        "data": serialized_data,
        "status": status.HTTP_200_OK,
    }, status=status.HTTP_200_OK)





def delete_data_if_user_quitte(user_id):
    try:
        user = UserAccount.objects.get(user_id=user_id)

        if user.status == 'quitte':
            Attendance.objects.filter(employee_id=user).delete()
            Leave.objects.filter(employee=user).delete()
            return Response(f"Deleted data for user {user.email} because the status is 'quitte'"
                            ,status=status.HTTP_200_OK)
        else:
            return Response(f"No data deletion. User {user.email} has a status other than 'quitte'",
                            status=status.HTTP_204_NO_CONTENT)
    except UserAccount.DoesNotExist:
        return Response(f"User with ID {user_id} does not exist.",
                        status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(f"Error: {str(e)}",
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    


