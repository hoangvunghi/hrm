from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from base.models import Employee
from .serializers import RoleSerializer
from .models import Role
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.http import Http404
from base.views import is_valid_type,obj_update
from django.core.paginator import Paginator,EmptyPage



@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def list_role(request):
    page_index = request.GET.get('pageIndex', 1)
    page_size = request.GET.get('pageSize', 10)
    total_leave = Role.objects.count()
    order_by = request.GET.get('sort_by', 'LeaveTypeID')
    search_query = request.GET.get('query', '')
    asc = request.GET.get('asc', 'true').lower() == 'true'  
    order_by = f"{'' if asc else '-'}{order_by}"
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
    role = Role.objects.all()
    if search_query:
        leav = leav.filter(RoleName__icontains=search_query)
    role = role.order_by(order_by)
    paginator = Paginator(leav, page_size)
    try:
        current_page_data = paginator.page(page_index)
    except EmptyPage:
        return Response({"error": "Page not found",
                         "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = RoleSerializer(current_page_data.object_list, many=True)
    serialized_data = serializer.data
    return Response({
        "total_rows": total_leave,
        "current_page": int(page_index),
        "data": serialized_data,
        "status": status.HTTP_200_OK
    }, status=status.HTTP_200_OK) 


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_role(request, pk):
    try:
        role = Role.objects.get(RoleID=pk)
    except Role.DoesNotExist:
        return Response({"error": "Role not found","status":status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if role.RoleID is not None:
            role.delete()
            Role.objects.filter(RoleID=pk).delete()
            return Response({"message": "Role deleted successfully",
                             "status":status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid roleID","status":status.HTTP_400_BAD_REQUEST}
                            , status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def create_role(request):
    serializer = RoleSerializer(data=request.data)
    required_fields = ["RoleName"]

    for field in required_fields:
        if not request.data.get(field):
            return Response({"error": f"{field.capitalize()} is required","status":status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Role created successfully","data":serializer.data,"status":status.HTTP_201_CREATED}
                        , status=status.HTTP_201_CREATED)
    return Response({"errors":serializer.errors, "status":status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST)


def validate_to_update_role(obj, data):
  
    errors={}
    dict=["RoleID"]
    for key in data:
        value= data[key]
        if key in dict:
            errors[key]= f"{key} not allowed to change"    
    return errors 



@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def update_role(request, pk):
    try:
        role = Role.objects.get(RoleID=pk)
    except Role.DoesNotExist:
        return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
        errors= validate_to_update_role(role, request.data)
        if len(errors):
            return Response({"error": errors,"status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        obj_update(role, request.data)
        serializer=RoleSerializer(role)
        return Response({"messeger": "update succesfull", "data": serializer.data}, status=status.HTTP_200_OK)