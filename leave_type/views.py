from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.models import Leave,Leave_Type
from .serializers import LeaveTypeSerializer
# Create your views here.

@api_view(['DELETE'])
def delete_leavetype(request, pk):
    try:
        leave_type = Leave_Type.objects.get(leave_type_id=pk)
    except Leave_Type.DoesNotExist:
        return Response({"message": "Leave type not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        leave_type_id = leave_type.leave_type_id
        if leave_type_id is not None and not Leave_Type.objects.filter(leave_type_id=leave_type_id).exists():
            return Response({"error": "Leave type not found"}, status=status.HTTP_400_BAD_REQUEST)

        
        leave_type.delete()
        return Response({"message": "Leave type deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
def create_leavetype(request):
    if request.method == 'POST':
        serializer = LeaveTypeSerializer(data=request.data)
        if serializer.is_valid():
            leave_type_id = request.data.get('leave_type_id', None) 
            if leave_type_id is not None and not Leave.objects.filter(leave_type_id=leave_type_id).exists():
                return Response({"error": "Leave type not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_leavetype(request, pk):
    try:
        leave_type = Leave_Type.objects.get(leave_type_id=pk)
    except Leave_Type.DoesNotExist:
        return Response({"message": "Leave type not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = LeaveTypeSerializer(leave_type, data=request.data)
        if serializer.is_valid():
            # Kiểm tra sự tồn tại của leave_type_id trong Leave
            leave_type_id = request.data.get('leave_type_id', None)
            if leave_type_id is not None and not Leave.objects.filter(leave_type_id=leave_type_id).exists():
                return Response({"error": "Leave type not found in Leave"}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
