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
        if department.department_id is not None:
            department.delete()
            return Response({"message": "Department deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid department_id"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_department(request):
    serializer = DepartmentSerializer(data=request.data)
    if serializer.is_valid():
        department_id = request.data.get('department_id', None)

        if Department.objects.filter(department_id=department_id).exists():
            return Response({"error": "Department with this department_id already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Department created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
def update_department(request, pk):
    try:
        department = Department.objects.get(department_id=pk)
    except Department.DoesNotExist:
        return Response({"message": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('user_id', None)
            if user_id is not None and not UserAccount.objects.filter(user_id=user_id).exists():
                return Response({"error": "UserAccount not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
