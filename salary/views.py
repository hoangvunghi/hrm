from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import SalaryHistory
from base.models import Employee
from .serializers import SalarySerializer,EmployeeWithSalarySerializer,SalaryWithEmployeeSerializer
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.http import Http404
from base.views import is_valid_type,obj_update,validate_to_update
from django.core.paginator import Paginator,EmptyPage


@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def list_salary(request):
    page_index = request.GET.get('pageIndex', 1)
    page_size = request.GET.get('pageSize', 10)
    total_salary = SalaryHistory.objects.count()
    order_by = request.GET.get('sort_by', 'EmpID')
    search_query = request.GET.get('query', '')
    asc = request.GET.get('asc', 'true').lower() == 'true'  
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
            posi = SalaryHistory.objects.filter(EmpId__in=users)
        except ValueError:
            return Response({"error": "Invalid value for name.",
                             "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        posi = SalaryHistory.objects.all()
    order_by = f"{'' if asc else '-'}{order_by}"
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
        user_account_data = EmployeeWithSalarySerializer(position_instance.EmpID).data
        position_data = SalaryWithEmployeeSerializer(position_instance).data
        combined_data = {**user_account_data, **position_data}
        serialized_data.append(combined_data)
    return Response({
        "total_rows": total_salary,
        "current_page": int(page_index),
        "data": serialized_data,
        "status": status.HTTP_200_OK
    }, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_salary(request, pk,gk):
    try:
        position = SalaryHistory.objects.get(EmpID=pk,SalFrom=gk)
    except SalaryHistory.DoesNotExist:
        return Response({"error": "Salary not found","status":status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if position.EmpID is not None and position.SalFrom is not None:
            position.delete()
            return Response({"message": "Salary History deleted successfully",
                             "status":status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid SalFrom or EmpID","status":status.HTTP_400_BAD_REQUEST
                             }, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def create_salary(request):
    serializer = SalarySerializer(data=request.data)
    required_fields = ['SalFrom','SalAmount','EmpID',"SalEnd"]
    emp_id = request.data.get('EmpID', None)
    salfrom=request.data.get("SalFrom",None)
    try:
        employee = Employee.objects.get(EmpID=emp_id)
    except Employee.DoesNotExist:
        return Response({"error": f"Employee with EmpID {emp_id} does not exist.",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
    SalAmount = request.data.get('SalAmount')
    try:
        float(SalAmount)
    except ValueError:
        return Response({"error": "SalAmount must be a valid number or string",
                             "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    for field in required_fields:
        if not request.data.get(field):
            return Response({"error": f"{field.capitalize()} is required","status":status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    if SalaryHistory.objects.filter(EmpID=emp_id, SalFrom=salfrom).exists():
        return Response({"error": f"Salary record for EmpID {emp_id} and SalFrom {salfrom} already exists.",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Salary History created successfully",
                         "status":status.HTTP_201_CREATED,"data":serializer.data
                         ,"status":status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    return Response({"error":serializer.errors,"status":status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def update_salary(request, pk,gk):
    try:
        possition = SalaryHistory.objects.get(EmpID=pk,SalFrom=gk)
    except SalaryHistory.DoesNotExist:
        return Response({"error": "Salary history not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
        errors= validate_to_update(possition, request.data)
        if len(errors):
            return Response({"error": errors,"status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        obj_update(possition, request.data)
        serializer=SalarySerializer(possition)
        return Response({"messeger": "update succesfull", "data": serializer.data}, status=status.HTTP_200_OK)