from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from base.models import UserAccount, Department
from .serializers import DepartmentSerializer
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.http import Http404
from base.views import is_valid_type
from django.core.paginator import Paginator,EmptyPage


@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def list_department(request):
    page_number = request.GET.get('page', 1)
    items_per_page = 20
    total_department = Department.objects.count()
    all_department = Department.objects.all()
    paginator = Paginator(all_department, items_per_page)
    try:
        current_page_data = paginator.page(page_number)
    except EmptyPage:
        return Response({"error": "Page not found",
                         "status":status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = DepartmentSerializer(current_page_data.object_list, many=True)
    serialized_data = serializer.data
    return Response({
        "total_department": total_department,
        "current_page": page_number,
        "data": serialized_data,
        "status":status.HTTP_200_OK
    },status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_department(request, pk):
    try:
        department = Department.objects.get(department_id=pk)
    except Department.DoesNotExist:
        return Response({"error": "Department not found","status":status.HTTP_404_NOT_FOUND}, 
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if department.department_id is not None:
            department.delete()
            return Response({"message": "Department deleted successfully","status":status.HTTP_204_NO_CONTENT}, 
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid department_id","status":status.HTTP_400_BAD_REQUEST}, 
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def create_department(request):
    serializer = DepartmentSerializer(data=request.data)
    is_valid_type(serializer.data)
    if serializer.is_valid():
        department_id = request.data.get('department_id', None)
        department_name = request.data.get('department_name', None)
        user_id = request.data.get('user_id', None)
        existing_department = Department.objects.filter(department_id=department_id, department_name=department_name).first()
        if existing_department:
            if existing_department.user_set.filter(user_id=user_id).exists():
                return Response({"error":"User with this user_id already exists for department_id  and department_name ",
                                 "status":status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Department created successfully",
                         "status":status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,{"status":status.HTTP_400_BAD_REQUEST}, 
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def update_department(request, pk):
    try:
        department = Department.objects.get(department_id=pk)
    except Department.DoesNotExist:
        return Response({"error": "Department not found","status":status.HTTP_404_NOT_FOUND}, 
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = DepartmentSerializer(department, data=request.data)
        is_valid_type(serializer.data)
        if serializer.is_valid():
            user_id = request.data.get('user_id', None)
            if user_id is not None and not UserAccount.objects.filter(user_id=user_id).exists():
                return Response({"error": "UserAccount not found","status":status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, {'status':status.HTTP_200_OK},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,{"status":status.HTTP_400_BAD_REQUEST}, 
                        status=status.HTTP_400_BAD_REQUEST)
