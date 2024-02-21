from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from base.models import Employee
from .models import LeaveRequest
from .serializers import LeaveSerializer,EmployeeWithLeaveSerializer,LeaveWithEmployeeSerializer
from rest_framework import permissions
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from base.views import obj_update
from django.core.paginator import Paginator,EmptyPage
from leave_type.models import LeaveType
from django.db.models import Sum
from datetime import datetime, timedelta


@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])  
def list_leave(request):
    page_index = request.GET.get('pageIndex', 1)
    page_size = request.GET.get('pageSize', 10)
    order_by = request.GET.get('sort_by', 'LeaveRequestID')
    leave_type_name = request.GET.get('LeaveTypeName', '')
    leave_status = request.GET.get('LeaveStatus', '')
    search_query = request.GET.get('query', '')
    asc = request.GET.get('asc', 'true').lower() == 'true'  
    order_by = f"{'' if asc else '-'}{order_by}"
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
    if search_query:
        try:
            em_name = str(search_query)
            users = Employee.objects.filter(EmpName__icontains=em_name)
            leav = LeaveRequest.objects.filter(EmpID__in=users)
        except ValueError:
            return Response({"error": "Invalid value for name.",
                             "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        leav = LeaveRequest.objects.all()
    if leave_type_name:
        leav = leav.filter(LeaveTypeID__LeaveTypeName__icontains=leave_type_name)

    if leave_status:
        leav = leav.filter(LeaveStatus__icontains=leave_status)
    
    leav = leav.order_by(order_by)
    paginator = Paginator(leav, page_size)
    try:
        current_page_data = paginator.page(page_index)
    except EmptyPage:
        return Response({"error": "Page not found",
                         "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)

    serialized_data = []
    
    for leave_instance in current_page_data.object_list:
        user_account_data = EmployeeWithLeaveSerializer(leave_instance.EmpID).data
        leave_data = LeaveWithEmployeeSerializer(leave_instance).data

        leave_type_name = leave_instance.LeaveTypeID.LeaveTypeName
        leave_data["LeaveTypeName"] = leave_type_name

        combined_data = {**user_account_data, **leave_data}
        serialized_data.append(combined_data)

    return Response({
        "total_rows": leav.count(),
        "current_page": int(page_index),
        "data": serialized_data,
        "status": status.HTTP_200_OK
    }, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsOwnerOrReadonly])  
def list_leave_nv(request):
    page_index = request.GET.get('pageIndex', 1)
    page_size = request.GET.get('pageSize', 10)
    order_by = request.GET.get('sort_by', 'LeaveRequestID')
    asc = request.GET.get('asc', 'true').lower() == 'true'  
    order_by = f"{'' if asc else '-'}{order_by}"
    
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
    

    current_employee = request.user.EmpID.EmpID

    leav = LeaveRequest.objects.filter(EmpID=current_employee)
    leave_type_name = request.GET.get('LeaveTypeName', '')
    if leave_type_name:
        leav = leav.filter(LeaveTypeID__LeaveTypeName__icontains=leave_type_name)

    leave_status = request.GET.get('LeaveStatus', '')
    if leave_status:
        leav = leav.filter(LeaveStatus__icontains=leave_status)

    total_taken_leave_days = leav.aggregate(total=Sum('Duration'))['total']
    if total_taken_leave_days is None:
        total_taken_leave_days = 0

    allowed_leave_limit = 30
    remaining_leave_days = max(0, allowed_leave_limit - total_taken_leave_days)

    leav = leav.order_by(order_by)
    paginator = Paginator(leav, page_size)
    
    try:
        current_page_data = paginator.page(page_index)
    except EmptyPage:
        return Response({"error": "Page not found",
                         "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)
    
    serialized_data = []
    
    for leave_instance in current_page_data.object_list:
        user_account_data = EmployeeWithLeaveSerializer(leave_instance.EmpID).data
        leave_data = LeaveWithEmployeeSerializer(leave_instance).data

        leavetypeid = leave_data.get("LeaveTypeID")
        if leavetypeid is not None:
            try:
                leavetypename = LeaveType.objects.get(LeaveTypeID=leavetypeid).LeaveTypeName
                leave_data["LeaveTypeName"] = leavetypename
            except LeaveType.DoesNotExist:
                leave_data["LeaveTypeName"] = None
        else:
            leave_data["LeaveTypeName"] = None

        combined_data = {**user_account_data, **leave_data}
        serialized_data.append(combined_data)


    return Response({
        "total_rows": leav.count(),
        "current_page": int(page_index),
        "data": serialized_data,
        "remaining_leave_days": remaining_leave_days,  
        "status": status.HTTP_200_OK
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_leave(request, pk):
    try:
        leave = LeaveRequest.objects.get(LeaveRequestID=pk)
    except LeaveRequest.DoesNotExist:
        return Response({"error": "Leave Request not found",
                         "status": status.HTTP_404_NOT_FOUND}, 
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        if leave.LeaveRequestID is not None:
            leave.delete()
            return Response({"message": "Leave deleted successfully", 
                             "status": status.HTTP_200_OK},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid LeaveID", 
                             "status": status.HTTP_400_BAD_REQUEST}, 
                            status=status.HTTP_400_BAD_REQUEST)
            


def total_leave_days_in_year(employee_id, year):
    first_day = datetime(year, 1, 1)
    last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    total_leave_days = LeaveRequest.objects.filter(
        EmpID=employee_id,
     LeaveStartDate__range=[first_day, last_day]
    ).aggregate(total=Sum('Duration'))['total']
    if total_leave_days is None:
        total_leave_days = 0
    return total_leave_days
from django.db import transaction
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from django.db import models



def validate_to_update(obj, data):
    errors = {}
    allowed_fields = ['LeaveRequestID', 'EmpID']
    date_fields = ['LeaveStartDate', 'LeaveEndDate']

    for key in data:
        value = data[key]

        if key in date_fields:
            try:
                day, month, year = map(int, value.split('/'))
                data[key] = f"{year:04d}-{month:02d}-{day:02d}"
            except (ValueError, IndexError):
                errors[key] = f"Invalid date format for {key}. It must be in dd/mm/yyyy format."

        if key in allowed_fields:
            errors[key] = f"{key} not allowed to change"

    return errors


def obj_update(obj, validated_data):
    for key, value in validated_data.items():
        if key == 'LeaveTypeID':
            try:
                leavetype = LeaveType.objects.get(LeaveTypeID=value)
                setattr(obj, key, leavetype)
            except LeaveType.DoesNotExist:
                raise ValueError(f"Invalid LeaveTypeID provided: {value}")
        else:
            setattr(obj, key, value)
    obj.save()

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def update_leave(request, pk):
    try:
        leave = LeaveRequest.objects.get(LeaveRequestID=pk)
    except LeaveRequest.DoesNotExist:
        return Response({"error": "Leave Request not found"}, status=status.HTTP_404_NOT_FOUND)
    leavetypeid = request.data.get('LeaveTypeID', None)
    if leavetypeid !=None:
        try:
            leavetypeid = LeaveType.objects.get(LeaveTypeID=leavetypeid)
        except LeaveType.DoesNotExist:
            return Response({"error": f"LeaveType with LeaveTypeID {leavetypeid} does not exist.",
                            "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PATCH':
        errors= validate_to_update(leave, request.data)
        if len(errors):
            return Response({"error": errors,"status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        obj_update(leave, request.data)
        serializer=LeaveSerializer(leave)
        return Response({"messeger": "update succesfull", "data": serializer.data}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsOwnerOrReadonly])
def get_leave_remainder(request, pk):
    try:
        employee = Employee.objects.get(EmpID=pk)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    leave_types = LeaveType.objects.all()
    leave_remainder = {}

    for leave_type in leave_types:
        total_taken_leave_days = LeaveRequest.objects.filter(EmpID=employee, LeaveTypeID=leave_type, LeaveStatus='Đã phê duyệt').aggregate(total=Sum('Duration'))['total']
        if total_taken_leave_days is None:
            total_taken_leave_days = 0

        pending_approval_days = LeaveRequest.objects.filter(EmpID=employee, LeaveTypeID=leave_type, LeaveStatus='Chờ phê duyệt').aggregate(total=Sum('Duration'))['total']
        pending1_approval_days = LeaveRequest.objects.filter(EmpID=employee, LeaveTypeID=leave_type, LeaveStatus='Chờ xác nhận').aggregate(total=Sum('Duration'))['total']

        if pending_approval_days is None:
            pending_approval_days = 0
        if pending1_approval_days is None:
            pending1_approval_days = 0

        remaining_leave_days = max(0, leave_type.LimitedDuration - total_taken_leave_days - pending1_approval_days)
        
        leave_remainder[leave_type.LeaveTypeName] = {
            "cho_phep": leave_type.LimitedDuration,
            "da_dung": total_taken_leave_days,
            "cho_xac_nhan": pending1_approval_days,
            "cho_phe_duyet": pending_approval_days,
            "kha_dung": remaining_leave_days
        }

    return Response({
        "employee_id": employee.EmpID,
        "leave_remainder": leave_remainder,
        "status": status.HTTP_200_OK
    }, status=status.HTTP_200_OK)
from django.db.models.functions import Coalesce
from django.utils import timezone


def get_remaining_leave_days_for_year(employee_id, leave_type, year):
    total_taken_leave_days = LeaveRequest.objects.filter(
        EmpID=employee_id,
        LeaveTypeID=leave_type,
        LeaveStartDate__year=year,
        LeaveStatus='Đã phê duyệt'
    ).aggregate(total=Coalesce(Sum('Duration'), 0))['total']

    pending1_approval_days = LeaveRequest.objects.filter(
        EmpID=employee_id,
        LeaveTypeID=leave_type,
        LeaveStartDate__year=year,
        LeaveStatus='Chờ xác nhận'
    ).aggregate(total=Coalesce(Sum('Duration'), 0))['total']

    return max(0, leave_type.LimitedDuration - total_taken_leave_days - pending1_approval_days)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@transaction.atomic
def create_leave(request):
    data = request.data
    employee_id = request.user.EmpID.EmpID

    try:
        leave_type = LeaveType.objects.get(LeaveTypeID=data['LeaveTypeID'])
    except LeaveType.DoesNotExist:
        return Response({"error": "Leave type not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        employee = Employee.objects.get(EmpID=employee_id)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    leave_start_date_str = data['LeaveStartDate']
    leave_end_date_str = data['LeaveEndDate']

    try:
        leave_start_date = datetime.strptime(leave_start_date_str, '%d/%m/%Y')
        leave_end_date = datetime.strptime(leave_end_date_str, '%d/%m/%Y')
    except ValueError:
        return Response({"error": "Invalid date format. It must be in dd/mm/yyyy format."},
                        status=status.HTTP_400_BAD_REQUEST)

    current_year = timezone.now().year
    remaining_leave_days = get_remaining_leave_days_for_year(employee_id, leave_type, current_year)

    duration = (leave_end_date - leave_start_date).days + 1

    if duration > remaining_leave_days:
        return Response({"error": "Not enough remaining leave days for this leave type"},
                        status=status.HTTP_400_BAD_REQUEST)

    leave_request_data = {
        'EmpID': employee,
        'LeaveStartDate': leave_start_date,
        'LeaveEndDate': leave_end_date,
        'LeaveTypeID': leave_type,
        'Reason': data['Reason'],
        'LeaveStatus': 'Chờ xác nhận',
    }

    leave_request = LeaveRequest.objects.create(**leave_request_data)

    response_data = {
        "LeaveRequestID": leave_request.LeaveRequestID,
        "EmpID": employee_id,
        "LeaveTypeID": leave_type.LeaveTypeID,
        "LeaveStartDate": leave_start_date_str,
        "LeaveEndDate": leave_end_date_str,
        "Reason": data['Reason'],
        "LeaveStatus": 'Chờ xác nhận',
    }

    if leave_start_date.year == current_year:
        remaining_leave_days = get_remaining_leave_days_for_year(employee_id, leave_type, current_year)
    
    data={
        "message": "successfully",
        "data": response_data,
        "remaining_leave_days": remaining_leave_days,
        "status": status.HTTP_201_CREATED
    }
    return Response(data, status=status.HTTP_201_CREATED)

