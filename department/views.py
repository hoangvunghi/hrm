from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.models import UserAccount,Department
from .serializers import DepartmentSerializer
# Create your views here.

@api_view(['DELETE'])
def delete_department(request, pk):
    try:
        department = Department.objects.get(department_id=pk)
    except Department.DoesNotExist:
        return Response({"message": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        manager_id = department.manager_id
        if manager_id is not None and not UserAccount.objects.filter(user_id=manager_id).exists():
            return Response({"error": "Manager not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        department.delete()
        return Response({"message": "Department deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
def create_department(request):
    if request.method == 'POST':
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            manager_id = request.data.get('manager_id', None)
            if manager_id is not None and not UserAccount.objects.filter(user_id=manager_id).exists():
                return Response({"error": "Manager not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def update_department(request, pk):
    try:
        department = Department.objects.get(department_id=pk)
    except Department.DoesNotExist:
        return Response({"message": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            manager_id = request.data.get('manager_id', None)
            if manager_id is not None and not UserAccount.objects.filter(user_id=manager_id).exists():
                return Response({"error": "Manager not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)