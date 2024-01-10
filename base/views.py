from django.http import Http404, HttpResponse, HttpResponseForbidden,JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import  UserSerializer,EmployeeSerializer,UserSerializerWithEmployeeSerializer
from .serializers import EmployeeCreateSerializer,ResetPasswordSerializer,ForgotPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from .models import Employee,UserAccount
from job.models import Job
from role.models import Role
from department.models import Department
from timesheet.models import TimeSheet
from leave.models import LeaveRequest
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
import re,json
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer
from django.core.signing import dumps,loads
from datetime import datetime,timedelta
import base64
from django.core.files.base import ContentFile

@api_view(["GET",])
def a(request):
    return Response("hello")

UserAccount = get_user_model()
@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password_view(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    try:
        employee = Employee.objects.get(Email=email)
        user = UserAccount.objects.get(EmpID=employee.EmpID)
    except Employee.DoesNotExist:
        return Response({"message": "Employee not found for the provided email"},
                        status=status.HTTP_404_NOT_FOUND)
    except UserAccount.DoesNotExist:
        return Response({"message": "UserAccount not found for the provided Employee"},
                        status=status.HTTP_404_NOT_FOUND)
    try:
        # refresh = RefreshToken.for_user(user)
        # # reset_token = str(refresh.access_token)
        data={"UserID":user.UserID}
        token=dumps(data, key=settings.SECURITY_PASSWORD_SALT)

    except TokenError as e:
        return Response({"error": "Failed to generate reset token",
                         "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    email_subject = "Password Reset Request"
    email_message = f"Click the following link to reset your password: {settings.BACKEND_URL}/forgot/reset-password/{token}"

    send_mail(
        email_subject,
        email_message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

    return Response({"message": "Password reset email sent successfully",
                     "status": status.HTTP_200_OK},
                    status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password_view(request, token):
    serializer = ResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user_id = loads(token,key=settings.SECURITY_PASSWORD_SALT)["UserID"]
        user = UserAccount.objects.get(UserID=user_id)
    except (TypeError, ValueError, OverflowError, UserAccount.DoesNotExist):
        return Response({"error": "Invalid reset token",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
    new_password = serializer.validated_data['password']
    if not new_password:
        raise ValidationError("New password is required")
    hashed_password = make_password(new_password)
    user.password = hashed_password
    user.save()
    refresh = RefreshToken.for_user(user)

    return Response({"message": "Password reset successfully",
                     "status": status.HTTP_200_OK},
                    status=status.HTTP_200_OK)

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
            username = request.data.get("username", "").lower()
            password = request.data.get("password", "")
            if not username or not password:
                return Response({"error": "Username and password are required",
                                 "status": status.HTTP_400_BAD_REQUEST}, 
                                status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not user.UserStatus:
                    return Response({"error": "Account has been locked.",
                                     "status": status.HTTP_401_UNAUTHORIZED}, 
                                    status=status.HTTP_401_UNAUTHORIZED)

                try:
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                except TokenError as e:
                    if isinstance(e, InvalidToken) and e.args[0] == "Token has expired":
                        return Response({"error": "Access token has expired. Please refresh the token.",
                                         "status": status.HTTP_401_UNAUTHORIZED}, 
                                        status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        return Response({"error": "Invalid token.",
                                         "status": status.HTTP_401_UNAUTHORIZED},
                                        status=status.HTTP_401_UNAUTHORIZED)
                employee_data = EmployeeSerializer(user.EmpID).data
                
                data = {
                    "response": "Login successful",
                    "data": employee_data,
                    'token': {
                        'refresh': str(refresh),
                        'access': access_token,
                    },
                    "status": status.HTTP_200_OK,
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid username or password',
                                 "status": status.HTTP_401_UNAUTHORIZED}, 
                                status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e),
                             "status": status.HTTP_400_BAD_REQUEST}, 
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def reset_employee_password(request, pk):
    try:
        user = UserAccount.objects.get(EmpID=pk)
    except UserAccount.DoesNotExist:
        return Response({"error": "User Account not found",
                         "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)

    new_password = request.data.get('new_password')

    if not new_password:
        return Response({"error": "New password is required",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)

    hashed_password = make_password(new_password)
    
    user.password = hashed_password
    user.save()

    refresh = RefreshToken.for_user(user)
    
    serializer = UserSerializer(user)
    return Response({"message": "Password reset successfully",
                     "data": serializer.data,
                     "status": status.HTTP_200_OK},
                    status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def change_password(request, pk):
    if request.method == 'POST':
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        if not is_strong_password(new_password):
            return Response({'success': False, 'message': 'New password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.',
                             "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

        UserAccount = get_user_model()
        try:
            user_account = UserAccount.objects.get(EmpID=pk)
        except UserAccount.DoesNotExist:
            return Response({'success': False, 'message': 'User not found.',
                             "status": status.HTTP_404_NOT_FOUND},
                            status=status.HTTP_404_NOT_FOUND)
        
        if not check_password(current_password, user_account.password):
            return Response({'success': False, 'message': 'Current password is incorrect.',
                             "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

        # Đặt mật khẩu mới và lưu
        user_account.set_password(new_password)
        user_account.save()
        
        return Response({'success': True, 'message': 'Password changed successfully.',
                         "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

    return Response({'success': False, 'message': 'Invalid request method.',
                     "status": status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST)

def is_strong_password(password):
    if (
        len(password) >= 8
        and any(c.isupper() for c in password)
        and any(c.islower() for c in password)
        and any(c.isdigit() for c in password)
        and any(c in r'!@#$%^&*()-_=+[]{}|;:,.<>?/"`~' for c in password)
    ):
        return True
    else:
        return False



@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_account(request, pk):
    try:
        account = UserAccount.objects.get(EmpID=pk)
    except UserAccount.DoesNotExist:
        return Response({"error": "User Account not found",
                         "status":status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        delete_data_if_user_quitte(pk)

        account.delete()
        return Response({"message": "Employee deleted successfully",
                         "status":status.HTTP_204_NO_CONTENT}, 
                        status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_employee(request, pk):
    try:
        employee = Employee.objects.get(EmpID=pk)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found",
                         "status":status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        employee.delete()
        delete_data_if_user_quitte(pk)
        TimeSheet.objects.filter(EmpID=pk).delete()
        LeaveRequest.objects.filter(EmpID=pk).delete()
        Job.objects.filter(EmpID=pk).delete()
        Department.objects.filter(EmpID=pk).delete()
        return Response({"message": "Employee deleted successfully",
                         "status":status.HTTP_204_NO_CONTENT}, 
                        status=status.HTTP_204_NO_CONTENT)



def is_valid_type(request): 
    errors = {}
    required_fields = []
    for field in required_fields:
        if field in request.data and not request.data[field]:
            errors[field] = f'{field.capitalize()} is required'
    if 'username' in request.data and not request.data['username']:
        errors['username'] = 'Username is required'
    if 'password'  in request.data and not request.data['password']:
        errors['password'] = 'Password is required'
    if 'email'  in request.data and not request.data['email']:
        errors['email'] = 'Email is required'
    if 'email'  in request.data and  request.data['email'] !="":
        new_email = request.data['email'].lower()
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, new_email):
            return Response({"error": "Invalid email format","status":status.HTTP_400_BAD_REQUEST}, 
                            status=status.HTTP_400_BAD_REQUEST)
    
    if 'phone_number'  in request.data and not request.data['phone_number']:
        errors['phone_number'] = 'Phone number is required'
    if 'phone_number'  in request.data and  request.data['phone_number'] !="":
        phone_number = request.data['phone_number']
        phone_regex = r'^[0-9]+$'
        if not re.match(phone_regex, phone_number) or len(phone_number) != 10:
            errors['phone_number'] = 'Invalid phone number format.'

    if errors:
        return Response({'error':errors}
                        ,status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Data is valid","status":status.HTTP_200_OK}
                    , status=status.HTTP_200_OK)

UserAccount = get_user_model()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def create_employee(request):
    serializer = EmployeeCreateSerializer(data=request.data)
    required_fields = ['EmpName',"Email","CCCD","DepID","JobID","RoleID"]
    if 'Email'  in request.data and  request.data['Email'] !="":
        new_email = request.data['Email'].lower()
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, new_email):
            return Response({"error": "Invalid email format","status":status.HTTP_400_BAD_REQUEST}, 
                            status=status.HTTP_400_BAD_REQUEST)
    for field in required_fields:
        if not request.data.get(field):
            return Response({"error": f"{field.capitalize()} is required", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    employee_email = request.data['Email']
    employee_cccd=request.data["CCCD"]
    employee_role=request.data["RoleID"]
    if not Role.objects.filter(RoleID=employee_role).exists():
        return Response({"error": f"Role with RoleID {employee_role} does not exist",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
    # role_name = request.data["RoleName"]
    # try:
    #     role = Role.objects.get(RoleName=role_name)
    # except Role.DoesNotExist:
    #     return Response({"error": f"Role with RoleName {role_name} does not exist",
    #                      "status": status.HTTP_400_BAD_REQUEST},
    #                     status=status.HTTP_400_BAD_REQUEST)
    if not employee_cccd.isdigit() or 9 != len(employee_cccd) or len(employee_cccd)!=12 :
        return Response({"error": f"cccdmust be a numeric value with 9 or 12 digits",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
    if Employee.objects.filter(CCCD=employee_cccd).exists():
        return Response({"error": "This cccd is already associated with an existing employee",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)                        
    if Employee.objects.filter(Email=employee_email).exists():
        return Response({"error": "This email is already associated with an existing employee",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
    dep_id = request.data["DepID"]
    if not Department.objects.filter(DepID=dep_id).exists():
        return Response({"error": f"Department with DepID {dep_id} does not exist",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
    job_id = request.data["JobID"]
    if not Job.objects.filter(JobID=job_id).exists():
        return Response({"error": f"Job with JobID {job_id} does not exist",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
    base64_image = request.data.get('PhotoPath', '')
    if base64_image:
        try:
            image_data = base64.b64decode(base64_image.split(',')[1])
            image_file = ContentFile(image_data, name='uploaded_image.jpg')
            serializer.validated_data['PhotoPath'] = image_file
        except Exception as e:
            return Response({"error": "Error decoding base64 image",
                             "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        # serializer.validated_data['RoleID'] = role.RoleID
        employee = serializer.save()
        emp_id = employee.EmpID
        if not UserAccount.objects.filter(EmpID=emp_id).exists():
            department = employee.DepID
            if not department:
                return Response({"error": "Employee is not associated with any department.",
                                "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
            dep_name = department.DepName
            dep_short_name = department.DepShortName
            position_count = count_employee_department(dep_name)
            formatted_position_count = f"{position_count:03d}"  
            new_user_id = f"{dep_short_name.lower()}{formatted_position_count}"
            user_account=UserAccount.objects.create_user(
                UserID=new_user_id,
                password="123A567a",  
                EmpID=employee
            )

            employee_email = employee.Email
            employee_name = employee.EmpName
            email_subject = "Chào mừng đến với WhiteNeuron"
            email_message = f" Xin chào {employee_name},\n\n"
            email_message += f" Tài khoản của bạn đã được kích hoạt thành công trong hệ thống.\n"
            email_message += f"\tUsername: {new_user_id}\n"
            email_message += f"\tPassword: 123A567a\n\n"  # Đặt mật khẩu mặc định
            email_message += f"Truy cập trang web {settings.BACKEND_URL}/login\n"
            email_message += "\n\n*Đây là email từ hệ thống đề nghị không reply."

            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [employee_email],
                fail_silently=False,
            )
            serializer_data = serializer.data
            serializer_data["UserID"] = user_account.UserID
        return Response({"message": "Employee and UserAccount created successfully. Please check email to get username and password",
                         "data": serializer_data,
                         "status": status.HTTP_201_CREATED},
                        status=status.HTTP_201_CREATED)

    return Response({"error": serializer.errors, "status": status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST)




def validate_to_update(obj, data):
    errors={}
    dict=['UserID', 'EmpID',"SalFrom"]
    for key in data:
        value= data[key]
        if key in dict:
            errors[key]= f"{key} not allowed to change"        
        if  key=='SalAmount':
            try:
                sal_amount = float(value)
            except ValueError:
                errors[key]= f"amount must be float"     
           
    return errors 

def obj_update(obj, validated_data):
    for key, value in validated_data.items():
        if key == 'DepID':
            try:
                department = Department.objects.get(DepID=value)
                setattr(obj, key, department)
            except Department.DoesNotExist:
                raise ValueError(f"Invalid DepID provided: {value}")

        elif key == 'JobID':
            try:
                job = Job.objects.get(JobID=value)
                setattr(obj, key, job)
            except Job.DoesNotExist:
                raise ValueError(f"Invalid JobID provided: {value}")
        elif key == 'PhotoPath':
            # Xử lý ảnh từ chuỗi base64
            try:
                image_data = base64.b64decode(value.split(',')[1])
                image_file = ContentFile(image_data, name='uploaded_image.jpg')
                setattr(obj, key, image_file)
            except Exception as e:
                raise ValueError("Invalid attempt to update PhotoPath")
        else:
            setattr(obj, key, value)

    obj.save()
    
def validate_to_update_account(obj, data):
    errors={}
    dict=['UserID', 'EmpID',]
    if 'UserStatus' in data:
        user_status = data['UserStatus']

        user_status_lower = str(user_status)

        if user_status_lower not in ['True', 'False', '0', '1']:
            errors['UserStatus'] = "UserStatus must be a valid boolean value (True/False or 0/1)."
    for key in data:
        value= data[key]
        if key in dict:
            errors[key]= f"{key} not allowed to change"        
    return errors 

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def update_account(request, pk):
    try:
        employee = UserAccount.objects.get(EmpID=pk)
    except UserAccount.DoesNotExist:
        return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PATCH':
        errors= validate_to_update_account(employee, request.data)
        if len(errors):
            return Response({"error": errors,"status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        obj_update(employee, request.data)
        serializer=UserSerializer(employee)
        return Response({"messeger": "update succesfull", "data": serializer.data,"status":status.HTTP_200_OK},
                        status=status.HTTP_200_OK)    


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def update_employee(request, pk):
    try:
        employee = Employee.objects.get(EmpID=pk)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
        errors= validate_to_update(employee, request.data)
        if len(errors):
            return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
        new_email = request.data.get('Email', '')
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if new_email and not re.match(email_regex, new_email):
            return Response({"error": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST)
        phone_number = request.data.get('Phone', '')
        phone_regex = r'^[0-9]+$'
        if phone_number and (not re.match(phone_regex, phone_number) or len(phone_number) != 10):
            return Response({"error": "Invalid phone number format"}, status=status.HTTP_400_BAD_REQUEST)
        obj_update(employee, request.data)
        serializer=EmployeeSerializer(employee)
        return Response({"messeger": "update succesfull", "data": serializer.data,"status":status.HTTP_200_OK},
                        status=status.HTTP_200_OK)    

        
        
@api_view(["GET",])
@permission_classes([IsAdminOrReadOnly])
def find_employee(request):
    q = request.GET.get('query') if request.GET.get('query') != None else ''
    employees = Employee.objects.filter(
        Q(EmpName__icontains=q)
    )
    employee_data = employees.values('EmpID', 'EmpName',"PhotoPath")

    return Response({'data': employee_data,
                     "status": status.HTTP_200_OK},
                    status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def query_employee(request):
    search_query = request.GET.get('query', '')
    employees = Employee.objects.filter(
        Q(EmpName__icontains=search_query)
    ).order_by('EmpID')
    serialized_data = []

    for employee_data in employees:
        data = {"id": employee_data.EmpID, "value": employee_data.EmpName}
        serialized_data.append(data)

    return Response({
        "data": serialized_data,
        "status": status.HTTP_200_OK,
    }, status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def list_employee(request):
    page_index = request.GET.get('pageIndex', 1)
    page_size = request.GET.get('pageSize', 10)
    order_by = request.GET.get('sort_by', 'EmpID')  
    search_query = request.GET.get('query', '')
    asc = request.GET.get('asc', 'true').lower() == 'true'  
    order_by = f"{'' if asc else '-'}{order_by}"

    employees = Employee.objects.filter(
        Q(EmpName__icontains=search_query)
    )
    gender_filter = request.GET.get('Gender', None)

    if gender_filter:
        gender_values = gender_filter.split(',')
        gender_q_objects = Q()
        for gender_value in gender_values:
            gender_q_objects |= Q(Gender__iexact=gender_value.strip())
        employees = employees.filter(gender_q_objects)
    dep_name_filter = request.GET.get('DepName', None)
    if dep_name_filter:
        dep_name_values = dep_name_filter.split(',')
        dep_name_q_objects = Q()
        for dep_name_value in dep_name_values:
            dep_name_q_objects |= Q(DepID__DepName__iexact=dep_name_value.strip())
        employees = employees.filter(dep_name_q_objects)
    job_name_filter = request.GET.get('JobName', None)
    if job_name_filter:
        job_name_values = job_name_filter.split(',')
        job_name_q_objects = Q()
        for job_name_value in job_name_values:
            job_name_q_objects |= Q(JobID__JobName__iexact=job_name_value.strip())
        employees = employees.filter(job_name_q_objects)

    employees = employees.order_by(order_by)

    try:
        page_size = int(page_size)
    except ValueError:
        return Response({"error": "Invalid value for items_per_page. Must be an integer.",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)

    allowed_values = [10, 20, 30, 40, 50]
    if page_size not in allowed_values:
        return Response({"error": f"Invalid value for items_per_page. Allowed values are: {', '.join(map(str, allowed_values))}.",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)

    total_employees = employees.count()
    paginator = Paginator(employees, page_size)

    try:
        current_page_data = paginator.page(page_index)
    except EmptyPage:
        return Response({"error": "Page not found",
                        "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)

    serialized_data = []

    for employee_data in current_page_data.object_list:
        serializer = EmployeeSerializer(employee_data)
        data = serializer.data
        emp_id = data["EmpID"]

        try:
            user = UserAccount.objects.get(EmpID=emp_id)
            username = UserAccount.objects.get(EmpID=emp_id).UserID
            pass_word = user.get_password()
            data["UserID"] = username
            data["password"] = pass_word
        except UserAccount.DoesNotExist:
            data["UserID"] = None
            data["password"] = None

        job_id = data["JobID"]
        try:
            job_name = Job.objects.get(JobID=job_id).JobName
            data["JobName"] = job_name
        except Job.DoesNotExist:
            data["JobName"] = None

        dep_id = data["DepID"]
        try:
            dep_name = Department.objects.get(DepID=dep_id).DepName
            data["DepName"] = dep_name
        except Department.DoesNotExist:
            data["DepName"] = None

        role_id = data["RoleID"]
        try:
            role_name = Role.objects.get(RoleID=role_id).RoleName
            data["RoleName"] = role_name
        except Role.DoesNotExist:
            data["RoleName"] = None

        serialized_data.append(data)

    return Response({
        "total_rows": total_employees,
        "current_page": int(page_index),
        "data": serialized_data,
        "status": status.HTTP_200_OK,
    }, status=status.HTTP_200_OK)
def delete_data_if_user_quitte(EmpID):
    try:
        user = Employee.objects.get(EmpID=EmpID)
        if user.status == 'quitte':
            TimeSheet.objects.filter(EmpID=user).delete()
            LeaveRequest.objects.filter(EmpID=user).delete()
            UserAccount.objects.filter(EmpID=user).delete()
            return Response(f"Deleted data for user {user.email} because the status is 'quitte'"
                            ,status=status.HTTP_200_OK)
        else:
            return Response(f"No data deletion. User {user.email} has a status other than 'quitte'",
                            status=status.HTTP_204_NO_CONTENT)
    except Employee.DoesNotExist:
        return Response(f"User with ID {EmpID} does not exist.",
                        status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(f"Error: {str(e)}",
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def list_user_password(request):
    page_index = request.GET.get('pageIndex', 1)
    page_size = request.GET.get('pageSize', 10)
    order_by = request.GET.get('sort_by', 'UserID')  
    search_query = request.GET.get('query', '')
    asc = request.GET.get('asc', 'true').lower() == 'true'  
    order_by = f"{'' if asc else '-'}{order_by}"
    
    accounts = UserAccount.objects.filter(
        Q(UserID__icontains=search_query)
    ).order_by(order_by)

    try:
        page_size = int(page_size)
    except ValueError:
        return Response({"error": "Invalid value for items_per_page. Must be an integer.",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
    allowed_values = [10, 20, 30, 40, 50]
    if page_size not in allowed_values:
        return Response({"error": f"Invalid value for items_per_page. Allowed values are: {', '.join(map(str, allowed_values))}.",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
    
    total_userid = accounts.count()
    paginator = Paginator(accounts, page_size)
    
    try:
        current_page_data = paginator.page(page_index)
    except EmptyPage:
        return Response({"error": "Page not found",
                        "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)

    serialized_data = []

    for account_data in current_page_data.object_list:
        serializer = UserSerializer(account_data)
        data = {
            "UserID": serializer.data["UserID"],
            "password": account_data.get_password(),
            "UserStatus": account_data.UserStatus,
            "EmpID": serializer.data["EmpID"],
        }

        emp_id = serializer.data["EmpID"]
        try:
            emp_name = Employee.objects.get(EmpID=emp_id).EmpName
            data["EmpName"] = emp_name
        except Employee.DoesNotExist:
            data["EmpName"] = None

        serialized_data.append(data)

    return Response({
        "total_rows": total_userid,
        "current_page": int(page_index),
        "data": serialized_data,
        "status": status.HTTP_200_OK,
    }, status=status.HTTP_200_OK)


def count_employee_department(department_name):
    department = Department.objects.get(DepName=department_name)
    employee_count = Employee.objects.filter(DepID=department).count()
    return employee_count


from django.utils import timezone

@api_view(["GET"])
def get_birthday_employee(request):
    today = timezone.now()
    three_days_later = today + timedelta(days=3)
    employees = Employee.objects.filter(BirthDate__range=[today.date(), three_days_later.date()])
    number=employees.count()
    employee_data = [
        {
            'EmpName': employee.EmpName,
            "Date of birth":employee.BirthDate.strftime('%d-%m-%Y'),
            'The number of days remaining until the birthday:': (employee.BirthDate - today).days
        }
        for employee in employees
    ]
    return Response({"message":f"{number} people's birthdays approaching","data":employee_data,
                     "status":status.HTTP_200_OK}, status=status.HTTP_200_OK)