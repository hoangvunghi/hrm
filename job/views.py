from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from base.models import Employee
from .models import Job
from department.models import Department
from .serializers import JobSerializer,EmployeeWithJobSerializer,JobWithEmployeeSerializer,TotalEmployeeWithJobSerializer
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.http import Http404
from base.views import is_valid_type,obj_update
from django.core.paginator import Paginator,EmptyPage



@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def list_job(request):
    page_index = request.GET.get('pageIndex', 1)
    page_size = request.GET.get('pageSize', 10)
    order_by = request.GET.get('sort_by', 'JobID')
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
    if search_query:
        try:
            em_name = str(search_query)
            jobs = Job.objects.filter(Employee__EmpName__icontains=em_name)
        except ValueError:
            return Response({"error": "Invalid value for name.",
                             "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        jobs = Job.objects.all()
    jobs = jobs.order_by(order_by)
    paginator = Paginator(jobs, page_size)
    try:
        current_page_data = paginator.page(page_index)
    except EmptyPage:
        return Response({"error": "Page not found",
                         "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)
    serialized_data = []
    for job_instance in current_page_data.object_list:
        serializer = JobSerializer(job_instance)
        data = serializer.data
        
        dep_id = data["DepID"]
        try:
            dep_name = Department.objects.get(DepID=dep_id).DepName
            data["DepName"] = dep_name
        except Department.DoesNotExist:
            data["DepName"] = None

        serialized_data.append(data)    
    return Response({
        "total_rows": jobs.count(),
        "current_page": int(page_index),
        "data": serialized_data,
        "status": status.HTTP_200_OK
    }, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_job(request, pk):
    try:
        position = Job.objects.get(JobID=pk)
    except Job.DoesNotExist:
        return Response({"error": "Position not found","status":status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        if position.JobID is not None:
            position.delete()
            return Response({"message": "Job deleted successfully",
                             "status":status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid JobID","status":status.HTTP_400_BAD_REQUEST
                             }, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def create_job(request):
    serializer = JobSerializer(data=request.data)
    required_fields = ['JobName',"JobID","DepID"]
    for field in required_fields:
        if not request.data.get(field):
            return Response({"error": f"{field} is required","status":status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    DepID = request.data.get('DepID', None)
   
    try:
        department = Department.objects.get(DepID=DepID)
    except Department.DoesNotExist:
        return Response({"error": f"Department with DepID {DepID} does not exist.",
                         "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Job created successfully","data":serializer.data,
                         "status":status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    return Response({"error":serializer.errors,"status":status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST)



def validate_to_update(obj, data):

    errors={}
    dict=['JobID']
    for key in data:
        value= data[key]
        if key in dict:
            errors[key]= f"{key} not allowed to change"        
      

    return errors 



@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def update_job(request, pk):
    try:
        possition = Job.objects.get(JobID=pk)
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
    DepID = request.data.get('DepID', None)
    if DepID!=None:
        try:
            department = Department.objects.get(DepID=DepID)
        except Department.DoesNotExist:
            return Response({"error": f"Department with DepID {DepID} does not exist.",
                            "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PATCH':
        errors= validate_to_update(possition, request.data)
        if len(errors):
            return Response({"error": errors,"status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        obj_update(possition, request.data)
        serializer=JobSerializer(possition)
        return Response({"messeger": "update succesfull", "data": serializer.data,"status":status.HTTP_200_OK}, status=status.HTTP_200_OK)