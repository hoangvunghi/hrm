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



@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])  
def list_leave(request):
    page_index = request.GET.get('pageIndex', 1)
    page_size = request.GET.get('pageSize', 20)
    order_by = request.GET.get('sort_by', 'LeaveRequestID')
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
        combined_data = {**user_account_data, **leave_data}
        serialized_data.append(combined_data)
    return Response({
        "total_rows": leav.count(),
        "current_page": int(page_index),
        "data": serialized_data,
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
                             "status": status.HTTP_204_NO_CONTENT},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid LeaveID", 
                             "status": status.HTTP_400_BAD_REQUEST}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
from django.db.models import Sum
from datetime import datetime, timedelta

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


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def create_leave(request):
    employee_id = request.user.EmpID.EmpID
    request.data['EmpID'] = employee_id
    current_year = datetime.now().year
    total_leave_days = total_leave_days_in_year(employee_id, current_year)
    requested_days = request.data.get('Duration', 0)
    if total_leave_days + requested_days > 30:  
        return Response({"error": "Exceeds the allowed leave limit for the year",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
    request.data['Duration'] = requested_days
    serializer = LeaveSerializer(data=request.data)
    required_fields = ["LeaveTypeID", "LeaveStartDate", "LeaveEndDate", "Reason"]
    for field in required_fields:
        if field not in request.data:
            return Response({"error": f"{field.capitalize()} is required",
                             "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    leavetypeid = request.data.get('LeaveTypeID', None)
    try:
        leavetypeid = LeaveType.objects.get(LeaveTypeID=leavetypeid)
    except LeaveType.DoesNotExist:
        return Response({"error": f"LeaveType with LeaveTypeID {leavetypeid} does not exist.",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
    start = datetime.strptime(request.data['LeaveStartDate'], '%Y-%m-%d')
    end = datetime.strptime(request.data['LeaveEndDate'], '%Y-%m-%d')
    duration = (end - start).days+1
    request.data['Duration'] = requested_days
    if serializer.is_valid():
        total_leave_days_after = total_leave_days_in_year(employee_id, current_year)+duration
        if total_leave_days_after >= 30:
            return Response({"error": "Exceeds the allowed leave limit for the year",
                             "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            serializer.save()
        return Response({"message": "Leave Request created successfully", "data": serializer.data,
                         "status": status.HTTP_201_CREATED},
                        status=status.HTTP_201_CREATED)
    
    return Response({"error": str(serializer.errors), "status": status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST)



def validate_to_update(obj, data):
    errors={}
    dict=['LeaveRequestID', 'EmpID']
    for key in data:
        value= data[key]
        if key in dict:
            errors[key]= f"{key} not allowed to change"        
    return errors



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