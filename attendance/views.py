from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from base.models import Attendance
from .serializers import AttendanceSerializer
from base.permissions import IsAdminOrReadOnly
from rest_framework import permissions
from django.core.paginator import Paginator,EmptyPage
from base.views import is_valid_type

@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def list_attendance(request):
    page_number = request.GET.get('page', 1)
    items_per_page = 20
    total_attendance = Attendance.objects.count()
    all_attendance = Attendance.objects.all()
    paginator = Paginator(all_attendance, items_per_page)
    try:
        current_page_data = paginator.page(page_number)
    except EmptyPage:
        return Response({"error": "Page not found",
                         "status":status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = AttendanceSerializer(current_page_data.object_list, many=True)
    serialized_data = serializer.data
    return Response({
        "total_attendances": total_attendance,
        "current_page": page_number,
        "data": serialized_data,
        "status":status.HTTP_200_OK
    },status=status.HTTP_200_OK)

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



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def create_attendance(request):
    serializer = AttendanceSerializer(data=request.data)
    is_valid_type(serializer.data)
    if serializer.is_valid():
        attendance_id = request.data.get('attendance_id', None)
        if Attendance.objects.filter(attendance_id=attendance_id).exists():
            return Response({"error": "Attendance with this attendance_id already exists",
                             "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Attendance created successfully",
                         "status":status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,{"status":status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST)
