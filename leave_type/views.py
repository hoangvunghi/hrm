from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from base.models import Employee
from leave_type.models import LeaveType
from leave.models import Leave
from .serializers import LeaveTypeSerializer
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.http import Http404
from base.views import is_valid_type,obj_update,validate_to_update
from django.core.paginator import Paginator,EmptyPage



@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def list_leave_type(request):
    page_index = request.GET.get('pageIndex', 1)
    page_size = request.GET.get('pageSize', 20)
    total_leave = Leave.objects.count()
    order_by = request.GET.get('sort_by', '-LeaveID')
    search_query = request.GET.get('query', '')

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
    
    serializer = LeaveTypeSerializer(page_size.object_list, many=True)
    serialized_data = serializer.data
    return Response({
        "total_rows": total_leave,
        "current_page": page_index,
        "data": serialized_data,
        "status":status.HTTP_200_OK
    },status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_leavetype(request, pk):
    try:
        leavetype = LeaveType.objects.get(LeaveTypeID=pk)
    except LeaveType.DoesNotExist:
        return Response({"error": "Leavetype not found","status":status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if leavetype.LeaveTypeID is not None:
            leavetype.delete()
            Leave.objects.filter(LeaveTypeID=pk).delete()
            return Response({"message": "Leavetype deleted successfully",
                             "status":status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid leave_type_id","status":status.HTTP_400_BAD_REQUEST}
                            , status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def create_leavetype(request):
    serializer = LeaveTypeSerializer(data=request.data)
    required_fields = ['LeaveTypeID']

    for field in required_fields:
        if not request.data.get(field):
            return Response({"error": f"{field.capitalize()} is required","status":status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        leave_type_id = request.data.get('LeaveTypeID', None)

        if LeaveType.objects.filter(LeaveTypeID=leave_type_id).exists():
            return Response({"error": "Leavetype with this LeaveTypeID already exists",
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
        leavetype = LeaveType.objects.get(LeaveTypeID=pk)
    except LeaveType.DoesNotExist:
        return Response({"error": "Leave Type not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
        errors= validate_to_update(leavetype, request.data)
        if len(errors):
            return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
        obj_update(leavetype, request.data)
        serializer=LeaveTypeSerializer(leavetype)
        return Response({"messeger": "update succesfull", "data": str(serializer.data)}, status=status.HTTP_200_OK)