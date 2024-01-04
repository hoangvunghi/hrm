from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from base.models import Employee
from .models import TimeSheet
from .serializers import TimeSheetWithUserAccountSerializer, UserAccountWithTimeSheetSerializer,TimeSheetSerializer
from base.permissions import IsAdminOrReadOnly,IsOwnerOrReadonly
from rest_framework import permissions
from django.core.paginator import Paginator,EmptyPage
from django.utils import timezone

#đã test, có thể tìm theo tên
@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def list_timesheet(request):
    page_index = request.GET.get('pageIndex', 1) 
    page_size = request.GET.get('pageSize', 20) 
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



@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_timesheet(request, pk):
    try:
        timesheet = TimeSheet.objects.get(TimeID=pk)
    except TimeSheet.DoesNotExist:
        return Response({"error": "Time sheet not found",
                         "status":status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if timesheet.TimeID is not None:
            timesheet.delete()
            return Response({"message": "Time sheet deleted successfully",
                             "status":status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid TimeID",
                             "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


# # Đã test 
# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticatedOrReadOnly])
# def create_timesheet(request):
#     request.data['EmpID'] = request.user.EmpID.EmpID
#     serializer = TimeSheetSerializer(data=request.data)
#     required_fields = ['EmpID',"TimeIn","TimeOut"]
#     emp_id = request.data.get('EmpID', None)
#     if emp_id != None:
#         try:
#             employee = Employee.objects.get(EmpID=emp_id)
#         except Employee.DoesNotExist:
#             return Response({"error": f"Employee with EmpID does not exist.",
#                             "status": status.HTTP_400_BAD_REQUEST},
#                             status=status.HTTP_400_BAD_REQUEST)
#     for field in required_fields:
#         if not request.data.get(field):
#             return Response({"error": f"{field.capitalize()} is required","status":status.HTTP_400_BAD_REQUEST},
#                             status=status.HTTP_400_BAD_REQUEST)
#     if serializer.is_valid():
#         serializer.validated_data["EmpID"] = request.user.EmpID
#         serializer.save()
#         return Response({"message": "TimeSheet created successfully","data":serializer.data,
#                          "status":status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors,
#                     status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsOwnerOrReadonly])
def list_timesheet_nv(request):
    page_index = request.GET.get('pageIndex', 1)
    page_size = request.GET.get('pageSize', 20)
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
    

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def check_in(request):

    existing_timesheet = TimeSheet.objects.filter(EmpID=request.user.EmpID, TimeIn__date=timezone.now().date()).first()

    if existing_timesheet:
        return Response({"error": "Cannot check in. Already checked in today.",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)


    timesheet = TimeSheet.objects.create(EmpID=request.user.EmpID, TimeIn=timezone.now())

    serializer = TimeSheetSerializer(timesheet)
    return Response({"message": "Checked in successfully", "data": serializer.data,
                     "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def check_out(request):

    existing_timesheet = TimeSheet.objects.filter(EmpID=request.user.EmpID, TimeOut__isnull=False, TimeIn__date=timezone.now().date()).first()

    if existing_timesheet:
        return Response({"error": "Cannot check out. Already checked out today.",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)

    timesheet = TimeSheet.objects.filter(EmpID=request.user.EmpID, TimeOut__isnull=True, TimeIn__date=timezone.now().date()).first()

    if timesheet:
        timesheet.TimeOut = timezone.now()
        timesheet.save()

        serializer = TimeSheetSerializer(timesheet)
        return Response({"message": "Checked out successfully", "data": serializer.data,
                         "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Cannot check out. Not checked in today.",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
