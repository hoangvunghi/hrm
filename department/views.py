from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from base.models import Employee
from .models import Department
from .serializers import DepartmentSerializer
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.http import Http404
from base.views import is_valid_type
from django.core.paginator import Paginator,EmptyPage



#đã test
@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def list_department(request):
    page_index = request.GET.get('pageIndex', 1)
    page_size = request.GET.get('pageSize', 20)
    order_by = request.GET.get('sort_by', 'DepID')
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

    depart = Department.objects.all()
    depart = depart.order_by(order_by)
    paginator = Paginator(depart, page_size)
    try:
        current_page_data = paginator.page(page_index)
    except EmptyPage:
        return Response({"error": "Page not found",
                         "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = DepartmentSerializer(current_page_data.object_list, many=True)
    serialized_data = serializer.data

    return Response({
        "total_rows": depart.count(),
        "current_page": int(page_index),
        "data": serialized_data,
        "status": status.HTTP_200_OK
    }, status=status.HTTP_200_OK)



def validate_to_update(obj, data):
    # obj da ton tai
    errors={}
    dict=["EmpID"]
    for key in data:
        value= data[key]
        if key in dict:
            errors[key]= f"{key} not allowed to change"        
        # if key=='email' and Employee.objects.filter(Email= value).exclude(EmpID= obj.EmpID).exists():
        #     errors[key]= f"email ({value}) is really exists"        
        if  key=='SalAmount':
            try:
                sal_amount = float(value)
            except ValueError:
                errors[key]= f"amount must be float"        
    return errors 



def obj_update(obj, validated_data):
    for key in validated_data:
        setattr(obj, key, validated_data[key])
    obj.save()



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
    required_fields = [ 'EmpID', 'DepName']
    for field in required_fields:
        if not request.data.get(field):
            return Response({"error": f"{field.capitalize()} is required",
                             "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    EmpID = request.data.get('EmpID', None)
    # if not EmpID.isdigit():
    #     return Response({"error": "EmpID must be a valid integer", "status": status.HTTP_400_BAD_REQUEST},
    #                     status=status.HTTP_400_BAD_REQUEST)
    try:
        employee = Employee.objects.get(EmpID=EmpID)
    except Employee.DoesNotExist:
        return Response({"error": f"Employee with EmpID {EmpID} does not exist.",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
    # department_id = request.data.get('DepID', None)
    department_name = request.data.get('DepName', None)
    # if Department.objects.filter(DepID=department_id).exists():
    #     return Response({"error": "Department with this DepID already exists",
    #                          "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    # if not department_id.isdigit():
    #     return Response({"error": "DepID must be a valid integer", "status": status.HTTP_400_BAD_REQUEST},
    #                     status=status.HTTP_400_BAD_REQUEST)
    # existing_department = Department.objects.filter(DepID=department_id, DepName=department_name).first()
    # if existing_department and existing_department.employee_set.filter(EmpID=EmpID).exists():
    #     return Response({"error": f"""User with this user_id already exists for department_id and 
    #                          department_name """,
    #                          "status": status.HTTP_400_BAD_REQUEST},
    #                         status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Department created successfully","data":serializer.data,
                         "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def update_department(request, pk):
    try:
        department = Department.objects.get(DepID=pk)
    except Department.DoesNotExist:
        return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
        errors = []
        emp_id = request.data.get('EmpID')
        if emp_id is not None:
            try:
                emp_id = int(emp_id)
            except ValueError:
                errors.append("EmpID must be a valid integer")
            else:
                try:
                    employee = Employee.objects.get(EmpID=emp_id)
                except Employee.DoesNotExist:
                    errors.append("Employee not found with the provided EmpID")
        errors= validate_to_update(department, request.data)
        if len(errors):
            return Response({"error": errors, "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        obj_update(department, request.data)
        serializer = DepartmentSerializer(department)
        return Response({"message": "Update successful", "data": serializer.data}, status=status.HTTP_200_OK)
