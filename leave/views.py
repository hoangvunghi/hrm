from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.models import UserAccount,Leave
from .serializers import LeaveSerializer
# Create your views here.

@api_view(['DELETE'])
def delete_leave(request, pk):
    try:
        leave = Leave.objects.get(leave_id=pk)
    except Leave.DoesNotExist:
        return Response({"message": "Leave not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if leave.leave_id is not None:
            leave.delete()
            return Response({"message": "Leave deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid leave_id"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_leave(request):
    serializer = LeaveSerializer(data=request.data)
    if serializer.is_valid():
        leave_id = request.data.get('leave_id', None)

        if Leave.objects.filter(leave_id=leave_id).exists():
            return Response({"error": "Leave with this position_id already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Leave created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
def update_leave(request, pk):
    try:
        leave = Leave.objects.get(leave_id=pk)
    except Leave.DoesNotExist:
        return Response({"message": "Leave not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = LeaveSerializer(leave, data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('user_id', None)
            if user_id is not None and not UserAccount.objects.filter(user_id=user_id).exists():
                return Response({"error": "UserAccount not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
