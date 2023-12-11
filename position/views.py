from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from base.models import UserAccount, Positions
from .serializers import PositionsSerializer
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.http import Http404
from base.views import is_valid_type
from django.core.paginator import Paginator,EmptyPage



@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def list_position(request):
    page_number = request.GET.get('page', 1)
    items_per_page = 20
    total_position = Positions.objects.count()
    all_position = Positions.objects.all()
    paginator = Paginator(all_position, items_per_page)
    try:
        current_page_data = paginator.page(page_number)
    except EmptyPage:
        return Response({"error": "Page not found",
                         "status":status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = PositionsSerializer(current_page_data.object_list, many=True)
    serialized_data = serializer.data
    return Response({
        "total_position": total_position,
        "current_page": page_number,
        "data": serialized_data,
        "status":status.HTTP_200_OK
    },status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_position(request, pk):
    try:
        position = Positions.objects.get(position_id=pk)
    except Positions.DoesNotExist:
        return Response({"error": "Position not found","status":status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if position.position_id is not None:
            position.delete()
            return Response({"message": "Position deleted successfully",
                             "status":status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid position_id","status":status.HTTP_400_BAD_REQUEST
                             }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def create_position(request):
    serializer = PositionsSerializer(data=request.data)
    required_fields = ['position_name']

    for field in required_fields:
        if not request.data.get(field):
            return Response({"error": f"{field.capitalize()} is required","status":status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        position_id = request.data.get('position_id', None)

        if Positions.objects.filter(position_id=position_id).exists():
            return Response({"error": "Position with this position_id already exists",
                             "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Position created successfully",
                         "status":status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,{"status":status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def update_position(request, pk):
    try:
        position = Positions.objects.get(position_id=pk)
    except Positions.DoesNotExist:
        return Response({"error": "Position not found",
                         "status":status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = PositionsSerializer(position, data=request.data)
        validation_response = is_valid_type(request)
        if validation_response.status_code != status.HTTP_200_OK:
            return validation_response
        if serializer.is_valid():
            user_id = request.data.get('user_id', None)
            if user_id is not None and not UserAccount.objects.filter(user_id=user_id).exists():
                return Response({"error": "User not found",
                                 "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, {"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
        return Response({"error":str(serializer.errors,),"status":status.HTTP_400_BAD_REQUEST} 
                        ,status=status.HTTP_400_BAD_REQUEST)
