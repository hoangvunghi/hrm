from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from base.models import Employee
from leave_type.models import LeaveType
from leave.models import LeaveRequest
from .serializers import LeaveTypeSerializer
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.http import Http404
from base.views import is_valid_type,obj_update
from django.core.paginator import Paginator,EmptyPage



@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def list_leave_type(request):
    page_index = request.GET.get('pageIndex', 1)
    page_size = request.GET.get('pageSize', 10)
    total_leave = LeaveRequest.objects.count()
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
    leav = LeaveType.objects.all()
    if search_query:
        leav = leav.filter(LeaveTypeName__icontains=search_query)
    leav = leav.order_by(order_by)
    paginator = Paginator(leav, page_size)
    try:
        current_page_data = paginator.page(page_index)
    except EmptyPage:
        return Response({"error": "Page not found",
                         "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = LeaveTypeSerializer(current_page_data.object_list, many=True)
    serialized_data = serializer.data
    return Response({
        "total_rows": total_leave,
        "current_page": int(page_index),
        "data": serialized_data,
        "status": status.HTTP_200_OK
    }, status=status.HTTP_200_OK)



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
            LeaveRequest.objects.filter(LeaveTypeID=pk).delete()
            return Response({"message": "Leavetype deleted successfully",
                             "status":status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid leave_type_id","status":status.HTTP_400_BAD_REQUEST}
                            , status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def create_leavetype(request):
    serializer = LeaveTypeSerializer(data=request.data)
    required_fields = ["LeaveTypeName","Subsidize","LeaveTypeDescription","LimitedDuration"]

    for field in required_fields:
        if not request.data.get(field):
            return Response({"error": f"{field.capitalize()} is required","status":status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    limit = request.data.get('LimitedDuration', None)
    Subsidize = request.data.get('Subsidize')
    try:
        float(Subsidize)
    except ValueError:
        return Response({"error": "Subsidize must be a valid number or string",
                             "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
    if not limit.isdigit():
        return Response({"error": "LimitedDuration must be a valid integer", "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)


    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Leavetype created successfully","data":serializer.data,"status":status.HTTP_201_CREATED}
                        , status=status.HTTP_201_CREATED)
    return Response({"errors":serializer.errors, "status":status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST)



def validate_to_update(obj, data):
    # obj da ton tai
    errors={}
    dict=["LeaveTypeID"]
    for key in data:
        value= data[key]
        if key in dict:
            errors[key]= f"{key} not allowed to change"    
        if  key=='Subsidize':
            try:
                sal_amount = float(value)
            except ValueError:
                errors[key]= f"Subsidize must be float" 
        if  key=='LimitedDuration':
            try:
                limit = int(value)
            except ValueError:
                errors[key]= f"LimitedDuration must be int" 
    return errors 



@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def update_leavetype(request, pk):
    try:
        leavetype = LeaveType.objects.get(LeaveTypeID=pk)
    except LeaveType.DoesNotExist:
        return Response({"error": "Leave Type not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
        errors= validate_to_update(leavetype, request.data)
        if len(errors):
            return Response({"error": errors,"status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        obj_update(leavetype, request.data)
        serializer=LeaveTypeSerializer(leavetype)
        return Response({"messeger": "update succesfull", "data": serializer.data}, status=status.HTTP_200_OK)