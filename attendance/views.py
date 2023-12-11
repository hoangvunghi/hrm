from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from base.models import Attendance,UserAccount
from .serializers import AttendanceWithUserAccountSerializer, UserAccountWithAttendanceSerializer,AttendanceSerializer
from base.serializers import UserAccountSerializer
from base.permissions import IsAdminOrReadOnly
from rest_framework import permissions
from django.core.paginator import Paginator,EmptyPage
from base.views import is_valid_type
from django.db.models import Q




#đã test, có thể tìm theo tên


@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])  # Add your custom permission class here if needed
def list_attendance(request):
    page_index = request.GET.get('page_index', 1)
    page_size = request.GET.get('page_size', 20)
    total_attendance = Attendance.objects.count()
    order_by = request.GET.get('order_by', 'attendance_id')
    search_query = request.GET.get('q', '')

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
            users = UserAccount.objects.filter(name__icontains=em_name)
            attens = Attendance.objects.filter(employee_id__in=users)
        except ValueError:
            return Response({"error": "Invalid value for name.",
                            "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        attens = Attendance.objects.all()

    attens = attens.order_by(order_by)
    paginator = Paginator(attens, page_size)

    try:
        current_page_data = paginator.page(page_index)
    except EmptyPage:
        return Response({"error": "Page not found",
                        "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)

    serialized_data = []
    for attendance_instance in current_page_data.object_list:
        user_account_data = UserAccountWithAttendanceSerializer(attendance_instance.employee_id).data
        attendance_data = AttendanceWithUserAccountSerializer(attendance_instance).data

        combined_data = {**user_account_data, **attendance_data}
        serialized_data.append(combined_data)

    return Response({
        "total_attendances": total_attendance,
        "current_page": page_index,
        "data": serialized_data,
        "status": status.HTTP_200_OK
    }, status=status.HTTP_200_OK)






    
    
    
#ok
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_attendance(request, pk):
    try:
        attendance = Attendance.objects.get(attendance_id=pk)
    except Attendance.DoesNotExist:
        return Response({"error": "Attendance not found",
                         "status":status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if attendance.attendance_id is not None:
            attendance.delete()
            return Response({"message": "Attendance deleted successfully",
                             "status":status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid attendance_id",
                             "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


# Đã test 
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def create_attendance(request):
    serializer = AttendanceSerializer(data=request.data)

    required_fields = ['employee_id']

    for field in required_fields:
        if not request.data.get(field):
            return Response({"error": f"{field.capitalize()} is required","status":status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        attendance_id = request.data.get('attendance_id', None)
        if Attendance.objects.filter(attendance_id=attendance_id).exists():
            return Response({"error": "Attendance with this attendance_id already exists",
                             },{"status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Attendance created successfully","data":str(serializer.data),
                         "status":status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
