from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from base.models import UserAccount, Leave, Leave_Type
from .serializers import LeaveTypeSerializer
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.http import Http404
from base.views import is_valid_type,obj_update,validate_to_update
from django.core.paginator import Paginator,EmptyPage



@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def list_leave_type(request):
    page_number = request.GET.get('page', 1)
    items_per_page = 20
    total_leave_type = Leave_Type.objects.count()
    all_leave_type = Leave_Type.objects.all()
    paginator = Paginator(all_leave_type, items_per_page)
    try:
        current_page_data = paginator.page(page_number)
    except EmptyPage:
        return Response({"error": "Page not found",
                         "status":status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = LeaveTypeSerializer(current_page_data.object_list, many=True)
    serialized_data = serializer.data
    return Response({
        "total_leave_type": total_leave_type,
        "current_page": page_number,
        "data": serialized_data,
        "status":status.HTTP_200_OK
    },status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_leavetype(request, pk):
    try:
        leavetype = Leave_Type.objects.get(leave_type_id=pk)
    except Leave_Type.DoesNotExist:
        return Response({"error": "Leavetype not found","status":status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if leavetype.leave_type_id is not None:
            leavetype.delete()
            Leave.objects.filter(leave_type_id=pk).delete()
            return Response({"message": "Leavetype deleted successfully",
                             "status":status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid leave_type_id","status":status.HTTP_400_BAD_REQUEST}
                            , status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def create_leavetype(request):
    serializer = LeaveTypeSerializer(data=request.data)
    required_fields = ['leave_type']

    for field in required_fields:
        if not request.data.get(field):
            return Response({"error": f"{field.capitalize()} is required","status":status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        leave_type_id = request.data.get('leave_type_id', None)

        if Leave_Type.objects.filter(leave_type_id=leave_type_id).exists():
            return Response({"error": "Leavetype with this leave_type_id already exists",
                             "status":status.HTTP_400_BAD_REQUEST}, 
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Leavetype created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, {"status":status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def update_leavetype(request, pk):
    try:
        leavetype = Leave_Type.objects.get(leave_type_id=pk)
    except Leave_Type.DoesNotExist:
        return Response({"error": "Leave Type not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
        errors= validate_to_update(leavetype, request.data)
        if len(errors):
            return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
        obj_update(leavetype, request.data)
        serializer=LeaveTypeSerializer(leavetype)
        return Response({"messeger": "update succesfull", "data": str(serializer.data)}, status=status.HTTP_200_OK)