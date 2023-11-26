from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from base.models import UserAccount,Leave,Leave_Type,Positions
from .serializers import PositionsSerializer
from rest_framework import permissions
from base.permission import IsAdminOrReadOnly,IsOwnerOrReadonly
from django.shortcuts import get_object_or_404

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_position(request, pk):
    position = get_object_or_404(Positions, position_id=pk)

    if request.method == 'DELETE':
        if position.position_id is not None:
            position.delete()
            return Response({"message": "Position deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid position_id"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def create_position(request):
    serializer = PositionsSerializer(data=request.data)
    if serializer.is_valid():
        position_id = request.data.get('position_id', None)

        if Positions.objects.filter(position_id=position_id).exists():
            return Response({"error": "Position with this position_id already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Position created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def update_position(request, pk):
    position = get_object_or_404(Positions, position_id=pk)

    if request.method == 'PATCH':
        serializer = PositionsSerializer(position, data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('user_id', None)
            if user_id is not None and not UserAccount.objects.filter(user_id=user_id).exists():
                return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
