from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from base.models import Employee, Department
from .serializers import DepartmentSerializer,EmployeeWithDepartmentSerializer,DepartmentWithEmployeeSerializer
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.http import Http404
from base.views import is_valid_type,validate_to_update,obj_update
from django.core.paginator import Paginator,EmptyPage


#đã test
@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])  
def list_department(request):
    page_index = request.GET.get('pageIndex', 1)
    page_size = request.GET.get('pageSize', 20)
    total_department = Department.objects.count()
    order_by = request.GET.get('sort_by', 'DepId')
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

    if search_query:
        try:
            em_name = str(search_query)
            users = Employee.objects.filter(EmpName__icontains=em_name)
            depart = Department.objects.filter(EmpID__in=users)
        except ValueError:
            return Response({"error": "Invalid value for name.",
                            "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        depart = Department.objects.all()

    depart = depart.order_by(order_by)
    paginator = Paginator(depart, page_size)

    try:
        current_page_data = paginator.page(page_index)
    except EmptyPage:
        return Response({"error": "Page not found",
                        "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)

    serialized_data = []
    for department_instance in current_page_data.object_list:
        user_account_data = EmployeeWithDepartmentSerializer(department_instance.EmpID).data
        department_data = DepartmentWithEmployeeSerializer(department_instance).data

        combined_data = {**user_account_data, **department_data}
        serialized_data.append(combined_data)

    return Response({
        "total_rows": total_department,
        "current_page": page_index,
        "data": serialized_data,
        "status": status.HTTP_200_OK
    }, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_department(request, pk):
    try:
        department = Department.objects.get(DepId=pk)
    except Department.DoesNotExist:
        return Response({"error": "Department not found","status":status.HTTP_404_NOT_FOUND}, 
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if department.DepID is not None:
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
    # is_valid_type(serializer.data)
    required_fields = ['DepId',"EmpID"]

    for field in required_fields:
        if not request.data.get(field):
            return Response({"error": f"{field.capitalize()} is required","status":status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
            
    if serializer.is_valid():
        department_id = request.data.get('DepId', None)
        department_name = request.data.get('DepName', None)
        user_id = request.data.get('EmpID', None)
        existing_department = Department.objects.filter(department_id=department_id, department_name=department_name).first()
        if existing_department:
            if existing_department.user_set.filter(user_id=user_id).exists():
                return Response({"error": f"""User with this user_id already exists for department_id {department_id} and 
                                 department_name {department_name}""",
                                 "status":status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Department created successfully",
                         "status":status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def update_department(request, pk):
    try:
        department = Department.objects.get(DepID=pk)
    except Department.DoesNotExist:
        return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
        errors= validate_to_update(department, request.data)
        if len(errors):
            return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
        obj_update(department, request.data)
        serializer=DepartmentSerializer(department)
        

        return Response({"messeger": "update succesfull", "data": str(serializer.data)}, status=status.HTTP_200_OK)

# @api_view(['PATCH'])
# @permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
# def update_department(request, pk):
#     try:
#         department = Department.objects.get(department_id=pk)
#     except Department.DoesNotExist:
#         return Response({"error": "Department not found", "status": status.HTTP_404_NOT_FOUND},
#                         status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'PATCH':
#         validation_response = is_valid_type(request)
#         if validation_response.status_code != status.HTTP_200_OK:
#             return validation_response
#         serializer = DepartmentSerializer(department, data=request.data)
#         validation_response = is_valid_type(request)
#         if validation_response.status_code != status.HTTP_200_OK:
#             return validation_response
#         if serializer.is_valid():
#             user_id = request.data.get('user_id', None)
#             if user_id is not None and not UserAccount.objects.filter(user_id=user_id).exists():
#                 return Response({"error": "UserAccount not found", "status": status.HTTP_400_BAD_REQUEST},
#                                 status=status.HTTP_400_BAD_REQUEST)
#             serializer.save()
#             return Response({"data": str(serializer.data), 'status': status.HTTP_200_OK},
#                             status=status.HTTP_200_OK)
#         return Response(serializer.errors,
#                         status=status.HTTP_400_BAD_REQUEST)

