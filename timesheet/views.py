from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from base.models import Employee
from .models import TimeSheet
from .serializers import TimeSheetWithUserAccountSerializer, UserAccountWithTimeSheetSerializer,TimeSheetSerializer
from base.serializers import EmployeeSerializer
from base.permissions import IsAdminOrReadOnly
from rest_framework import permissions
from django.core.paginator import Paginator,EmptyPage
from base.views import is_valid_type, validate_to_update,obj_update
from django.db.models import Q


#đã test, có thể tìm theo tên
@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])  
def list_timesheet(request):
    page_index = request.GET.get('pageIndex', 1)
    page_size = request.GET.get('pageSize', 20)
    total_attendance = TimeSheet.objects.count()
    order_by = request.GET.get('sort-by', 'TimeID')
    search_query = request.GET.get('query', '')

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
            time = TimeSheet.objects.filter(EmpID__in=users)
        except ValueError:
            return Response({"error": "Invalid value for name.",
                            "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        time = TimeSheet.objects.all()

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
        "current_page": page_index,
        "data": serialized_data,
        "status": status.HTTP_200_OK
    }, status=status.HTTP_200_OK)






    
    
    
#ok
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


# Đã test 
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def create_timesheet(request):
    serializer = TimeSheetSerializer(data=request.data)

    required_fields = ['EmpID']

    for field in required_fields:
        if not request.data.get(field):
            return Response({"error": f"{field.capitalize()} is required","status":status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        timeID = request.data.get('TimeID', None)
        if TimeSheet.objects.filter(TimeID=timeID).exists():
            return Response({"error": "Time sheet with this TimeID already exists",
                             },{"status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "TimeSheet created successfully","data":str(serializer.data),
                         "status":status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
