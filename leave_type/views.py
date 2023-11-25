from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.models import UserAccount,Leave,Leave_Type
from .serializers import LeaveTypeSerializer
# Create your views here.

@api_view(['DELETE'])
def delete_leavetype(request, pk):
    try:
        leavetype = Leave_Type.objects.get(department_id=pk)
    except Leave_Type.DoesNotExist:
        return Response({"message": "Leavetype not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if leavetype.leave_type_id is not None:
            leavetype.delete()
            return Response({"message": "Leavetype deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid leave_type_id"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
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
def update_leavetype(request, pk):
    try:
        leavetype = Leave_Type.objects.get(department_id=pk)
    except Leave_Type.DoesNotExist:
        return Response({"message": "Leavetype not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = LeaveTypeSerializer(leavetype, data=request.data)
        if serializer.is_valid():
            leave_type_id = request.data.get('leave_type_id', None)
            if leave_type_id is not None and not Leave.objects.filter(leave_type_id=leave_type_id).exists():
                return Response({"error": "Leavetype not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
