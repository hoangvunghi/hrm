from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from base.models import UserAccount, Leave, Leave_Type
from .serializers import LeaveTypeSerializer
from base.permission import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.http import Http404

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_leavetype(request, pk):
    try:
        leavetype = Leave_Type.objects.get(leave_type_id=pk)
    except Leave_Type.DoesNotExist:
        return Response({"error": "Leavetype not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if leavetype.leave_type_id is not None:
            leavetype.delete()
            Leave.objects.filter(leave_type_id=pk).delete()
            return Response({"message": "Leavetype deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid leave_type_id"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def create_leavetype(request):
    serializer = LeaveTypeSerializer(data=request.data)
    if serializer.is_valid():
        leave_type_id = request.data.get('leave_type_id', None)

        if Leave_Type.objects.filter(leave_type_id=leave_type_id).exists():
            return Response({"error": "Leavetype with this leave_type_id already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Leavetype created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def update_leavetype(request, pk):
    try:
        leavetype = Leave_Type.objects.get(leave_type_id=pk)
    except Leave_Type.DoesNotExist:
        return Response({"error": "Leavetype not found","status":status.HTTP_404_NOT_FOUND}
                        , status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = LeaveTypeSerializer(leavetype, data=request.data)
        if serializer.is_valid():
            leave_type_id = request.data.get('leave_type_id', None)
            if leave_type_id is not None and not Leave.objects.filter(leave_type_id=leave_type_id).exists():
                return Response({"error": "Leavetype not found","status":status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data,{"status":status.HTTP_200_OK},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,{"status":status.HTTP_400_BAD_REQUEST} ,
                        status=status.HTTP_400_BAD_REQUEST)
