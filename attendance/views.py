from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from base.models import Attendance
from .serializers import AttendanceSerializer
from base.permission import IsAdminOrReadOnly,IsOwnerOrReadonly
from rest_framework import permissions

# Create your views here.

from django.shortcuts import get_object_or_404

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_attendance(request, pk):
    attendance = get_object_or_404(Attendance, attendance_id=pk)

    if request.method == 'DELETE':
        if attendance.attendance_id is not None:
            attendance.delete()
            return Response({"message": "Attendance deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid attendance_id"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def create_attendance(request):

    serializer = AttendanceSerializer(data=request.data)
    if serializer.is_valid():
        attendance_id = request.data.get('attendance_id', None)

        if Attendance.objects.filter(attendance_id=attendance_id).exists():
            return Response({"error": "Attendance with this attendance_id already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Attendance created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PATCH'])
# def update_attendance(request, pk):
#     try:
#         attendance = Attendance.objects.get(attendance_id=pk)
#     except Attendance.DoesNotExist:
#         return Response({"message": "Attendance not found"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PATCH':
#         serializer = AttendanceSerializer(attendance, data=request.data)
#         if serializer.is_valid():
#             employee_id = request.data.get('employee_id', None)
#             if employee_id is not None and not UserAccount.objects.filter(user_id=employee_id).exists():
#                 return Response({"error": "Employee not found"}, status=status.HTTP_400_BAD_REQUEST)
            
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
