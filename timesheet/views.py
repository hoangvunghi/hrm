from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from base.models import Employee
from .models import TimeSheet
from .serializers import TimeSheetWithUserAccountSerializer, UserAccountWithTimeSheetSerializer,TimeSheetSerializer
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from rest_framework import permissions
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from datetime import timedelta
import platform
import subprocess

@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def list_timesheet(request):
    page_index = request.GET.get('pageIndex', 1) 
    page_size = request.GET.get('pageSize', 10) 
    total_attendance = TimeSheet.objects.count()
    order_by = request.GET.get('sort-by', 'TimeID')
    asc = request.GET.get('asc', 'true').lower() == 'true'  
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
    if search_query := request.GET.get('query', ''):
        try:
            em_name = str(search_query)
            users = Employee.objects.filter(EmpName__icontains=em_name)
            time = TimeSheet.objects.filter(EmpID__in=users)
        except ValueError:
            return Response({"error": "Invalid value for name.",
                            "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        time = TimeSheet.objects.all()
    order_by = f"{'' if asc else '-'}{order_by}"
    time = time.order_by(order_by)
    paginator = Paginator(time, page_size)
    try:
        current_page_data = paginator.page(page_index)
    except EmptyPage:
        return Response({"error": "Page not found",
                        "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)
    serialized_data = []
    for attendance_instance in current_page_data.object_list:
        user_account_data = UserAccountWithTimeSheetSerializer(attendance_instance.EmpID).data
        attendance_data = TimeSheetWithUserAccountSerializer(attendance_instance).data
        combined_data = {**user_account_data, **attendance_data}
        serialized_data.append(combined_data)
    return Response({
        "total_rows": total_attendance,
        "current_page": int(page_index),
        "data": serialized_data,
        "status": status.HTTP_200_OK
    }, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsOwnerOrReadonly])
def list_timesheet_nv(request):
    page_index = request.GET.get('pageIndex', 1)
    page_size = request.GET.get('pageSize', 10)
    order_by = request.GET.get('sort_by', 'TimeID')
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
    time = TimeSheet.objects.filter(EmpID=current_employee)
    time = time.order_by(order_by)
    paginator = Paginator(time, page_size)
    try:
        current_page_data = paginator.page(page_index)
    except EmptyPage:
        return Response({"error": "Page not found",
                         "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)
    serialized_data = []
    for attendance_instance in current_page_data.object_list:
        user_account_data = UserAccountWithTimeSheetSerializer(attendance_instance.EmpID).data
        attendance_data = TimeSheetWithUserAccountSerializer(attendance_instance).data
        combined_data = {**user_account_data, **attendance_data}
        serialized_data.append(combined_data)

    return Response({
        "total_rows": time.count(),
        "current_page": int(page_index),
        "data": serialized_data,
        "status": status.HTTP_200_OK
    }, status=status.HTTP_200_OK)


def get_existing_timesheet(emp_id, date):
    return TimeSheet.objects.filter(EmpID=emp_id, TimeIn__date=date).first()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def check_in(request):
    emp_id = request.user.EmpID
    current_date = timezone.now().date()
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    print(user_agent)
    print("------------")
    
    serial_number = get_serial_number(user_agent)

    if not serial_number:
        return Response({"error": "Không thể lấy số serial"}, status=status.HTTP_400_BAD_REQUEST)

    existing_timesheet_with_serial = TimeSheet.objects.filter(serial_number=serial_number, TimeIn__date=current_date).first()

    if existing_timesheet_with_serial:
        return Response({"error": "Số serial này đã được sử dụng bởi người dùng khác trong ngày hôm nay"}, status=status.HTTP_400_BAD_REQUEST)

    existing_timesheet = get_existing_timesheet(emp_id, current_date)

    if existing_timesheet:
        if existing_timesheet.serial_number == serial_number:
            return Response({"error": "Bạn đã check-in với số serial này trước đó trong ngày hôm nay"}, status=status.HTTP_400_BAD_REQUEST)
        
    checkin_time = timezone.now() + timedelta(hours=7)
    if not existing_timesheet:
        timesheet = TimeSheet.objects.create(EmpID=emp_id, TimeIn=checkin_time, serial_number=serial_number)
    else:
        existing_timesheet.data_dict.setdefault("checkin", []).append(checkin_time.strftime("%Y-%m-%d %H:%M:%S"))
        existing_timesheet.serial_number = serial_number
        existing_timesheet.save()
        timesheet = existing_timesheet

    serializer = TimeSheetSerializer(timesheet)
    return Response({"message": "Checked in successfully", "data": serializer.data, "status": status.HTTP_200_OK})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def check_out(request):
    emp_id = request.user.EmpID
    current_date = timezone.now().date()
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    serial_number = get_serial_number(user_agent)
    if not serial_number:
        return Response({"error": "Không thể lấy số serial"}, status=status.HTTP_400_BAD_REQUEST)

    existing_timesheet = get_existing_timesheet(emp_id, current_date)

    if not existing_timesheet or not existing_timesheet.TimeIn:
        return Response({"error": "Cannot check out. Not checked in today.", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

    checkout_time = timezone.now()
    checkout_time_data = timezone.now() + timedelta(hours=7)
    existing_timesheet.TimeOut = checkout_time
    existing_timesheet.data_dict.setdefault("checkout", []).append(checkout_time_data.strftime("%Y-%m-%d %H:%M:%S"))
    existing_timesheet.serial_number = serial_number  
    existing_timesheet.save()

    serializer = TimeSheetSerializer(existing_timesheet)
    return Response({"message": "Checked out successfully", "data": serializer.data, "status": status.HTTP_200_OK})


def get_serial_number(system):
    if system == 'Windows':
        try:
            output = subprocess.check_output(['wmic', 'diskdrive', 'get', 'serialnumber']).decode().strip()
            serial_number = output.split('\n')[1].strip()
            return serial_number
        except Exception as e:
            print(f"Error: {e}")
            return None
    elif system == 'Linux':
        try:
            output = subprocess.check_output(['cat', '/proc/cpuinfo']).decode().strip()
            for line in output.split('\n'):
                if 'Serial' in line:
                    serial_number = line.split(':')[-1].strip()
                    return serial_number
        except Exception as e:
            print(f"Error: {e}")
            return None
    elif system == 'Darwin':
        try:
            output = subprocess.check_output(['system_profiler', 'SPHardwareDataType']).decode().strip()
            for line in output.split('\n'):
                if 'Serial Number' in line:
                    serial_number = line.split(':')[-1].strip()
                    return serial_number
        except Exception as e:
            print(f"Error: {e}")
            return None
    else:
        print("Unsupported operating system.")
        return None
