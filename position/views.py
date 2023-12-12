from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from base.models import UserAccount, Positions
from .serializers import PositionsSerializer,UserAccountWithPositionSerializer,PositionWithUserAccountSerializer
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.http import Http404
from base.views import is_valid_type,obj_update,validate_to_update
from django.core.paginator import Paginator,EmptyPage



@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])  
def list_position(request):
    page_index = request.GET.get('page_index', 1)
    page_size = request.GET.get('page_size', 20)
    total_position = Positions.objects.count()
    order_by = request.GET.get('order_by', 'position_id')
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
            posi = Positions.objects.filter(position_id__in=users)
        except ValueError:
            return Response({"error": "Invalid value for name.",
                            "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        posi = Positions.objects.all()

    posi = posi.order_by(order_by)
    paginator = Paginator(posi, page_size)

    try:
        current_page_data = paginator.page(page_index)
    except EmptyPage:
        return Response({"error": "Page not found",
                        "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)

    serialized_data = []
    for position_instance in current_page_data.object_list:
        user_account_data = UserAccountWithPositionSerializer(position_instance.position_id).data
        position_data = PositionWithUserAccountSerializer(position_instance).data

        combined_data = {**user_account_data, **position_data}
        serialized_data.append(combined_data)

    return Response({
        "total_position": total_position,
        "current_page": page_index,
        "data": serialized_data,
        "status": status.HTTP_200_OK
    }, status=status.HTTP_200_OK)



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
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def update_position(request, pk):
    try:
        possition = Positions.objects.get(position_id=pk)
    except Positions.DoesNotExist:
        return Response({"error": "Position not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
        errors= validate_to_update(possition, request.data)
        if len(errors):
            return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
        obj_update(possition, request.data)
        serializer=PositionsSerializer(possition)
        return Response({"messeger": "update succesfull", "data": str(serializer.data)}, status=status.HTTP_200_OK)