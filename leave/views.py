from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from base.models import UserAccount, Leave
from .serializers import LeaveSerializer,UserAccountWithLeaveSerializer,LeaveWithUserAccountSerializer
from rest_framework import permissions
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.http import Http404
from base.views import is_valid_type
from django.core.paginator import Paginator,EmptyPage

@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])  
def list_leave(request):
    page_index = request.GET.get('page_index', 1)
    page_size = request.GET.get('page_size', 20)
    total_leave = Leave.objects.count()
    order_by = request.GET.get('order_by', '-leave_id')
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
            leav = Leave.objects.filter(employee__in=users)
        except ValueError:
            return Response({"error": "Invalid value for name.",
                            "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        leav = Leave.objects.all()

    leav = leav.order_by(order_by)
    paginator = Paginator(leav, page_size)

    try:
        current_page_data = paginator.page(page_index)
    except EmptyPage:
        return Response({"error": "Page not found",
                        "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)

    serialized_data = []
    for leave_instance in current_page_data.object_list:
        user_account_data = UserAccountWithLeaveSerializer(leave_instance.employee).data
        leave_data = LeaveWithUserAccountSerializer(leave_instance).data

        combined_data = {**user_account_data, **leave_data}
        serialized_data.append(combined_data)

    return Response({
        "total_leave": total_leave,
        "current_page": page_index,
        "data": serialized_data,
        "status": status.HTTP_200_OK
    }, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def delete_leave(request, pk):
    try:
        leave = Leave.objects.get(leave_id=pk)
    except Leave.DoesNotExist:
        return Response({"error": "Leave not found",
                         "status": status.HTTP_404_NOT_FOUND}, 
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if leave.leave_id is not None:
            leave.delete()
            return Response({"message": "Leave deleted successfully", 
                             "status": status.HTTP_204_NO_CONTENT},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid leave_id", 
                             "status": status.HTTP_400_BAD_REQUEST}, 
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def create_leave(request):
    serializer = LeaveSerializer(data=request.data)
    required_fields = ["leave_type"]

    for field in required_fields:
        if not request.data.get(field):
            return Response({"error": f"{field.capitalize()} is required","status":status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        leave_id = request.data.get('leave_id', None)

        if Leave.objects.filter(leave_id=leave_id).exists():
            return Response({"error": "Leave with this leave_id already exists", 
                             "status": status.HTTP_400_BAD_REQUEST}, 
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Leave created successfully", 
                         "status": status.HTTP_201_CREATED},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors,{"status":status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def update_leave(request, pk):
    try:
        leave = Leave.objects.get(leave_id=pk)
    except Leave.DoesNotExist:
        return Response({"error": "Leave not found", 
                         "status": status.HTTP_404_NOT_FOUND}, 
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = LeaveSerializer(leave, data=request.data)
        validation_response = is_valid_type(request)
        if validation_response.status_code != status.HTTP_200_OK:
            return validation_response
        if serializer.is_valid():
            user_id = request.data.get('user_id', None)
            if user_id is not None and not UserAccount.objects.filter(user_id=user_id).exists():
                return Response({"error": "UserAccount not found", 
                                 "status": status.HTTP_400_BAD_REQUEST}, 
                                status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data,{"status":status.HTTP_200_OK}, 
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,{"status":status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)

