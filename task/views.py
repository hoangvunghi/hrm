from rest_framework.decorators import api_view, permission_classes
from base.models import Task, Project, UserAccount
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from rest_framework.response import Response
from rest_framework import status, permissions
# Create your views here.
from .serializers import TaskSerializer
from rest_framework import permissions
from django.http import Http404
from django.db.models import Q

def is_valid(data):
    errors = {}
    proj_id = data.get('proj_id', '')
    user_id = data.get('user_id', '')
    if not proj_id:
        errors['proj_id'] = 'proj_id is required'
    if not user_id:
        errors['user_id'] = 'user_id is required'
    return errors

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def create_task(request):

    errors = is_valid(request.data)
    if len(errors):
        return Response({"errors":errors}, status=status.HTTP_400_BAD_REQUEST)
    
    task = TaskSerializer(data=request.data)
    if task.is_valid():
        proj_id = request.data.get('proj_id', None)
        user_id = request.data.get('user_id', None)

        if Project.objects.filter(proj_id=proj_id).exists() and UserAccount.objects.filter(user_id=user_id).exists():
            return Response({"error": f"Task with id {proj_id}, user {user_id} already exist", 
                             "status":status.HTTP_400_BAD_REQUEST}, 
                            status=status.HTTP_400_BAD_REQUEST)

        task.save()
        return Response({"message": "Task's create successfully", 
                         "status":status.HTTP_201_CREATED}, 
                         status=status.HTTP_201_CREATED)
    
    return Response(task.errors, 
                    {"status":status.HTTP_400_BAD_REQUEST}, 
                    status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def update_task(request, id):
    try:
        task = Task.objects.get(proj_id=id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found", 
                         "status":status.HTTP_404_NOT_FOUND}, 
                         status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = TaskSerializer(serializer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 
                            {'status':status.HTTP_200_OK}, 
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        {"status":status.HTTP_400_BAD_REQUEST}, 
                        status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_task(request, id):
    try:
        task = Task.objects.get(proj_id = id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found", 
                         "status":status.HTTP_404_NOT_FOUND}, 
                         status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        if task.proj_id is not None:
            task.delete()
            return Response({"message": "Task deleted successfully", 
                             "status":status.HTTP_204_NO_CONTENT}, 
                             status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid proj_id",
                              "status":status.HTTP_400_BAD_REQUEST}, 
                              status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def find_task(request):
    try:
        # Lấy giá trị từ tham số q trong request.GET hoặc mặc định là ''
        q = request.GET.get('q', '')

        # Thực hiện truy vấn
        tasks = Task.objects.filter(
            Q(proj_id__icontains=q) |
            Q(user_id__icontains=q) |
            Q(description__icontains=q)
        )

        # Sử dụng serializer để chuyển đổi dữ liệu thành định dạng JSON
        serializer = TaskSerializer(tasks, many=True)

        # Trả về kết quả tìm kiếm dưới dạng JSON
        return Response(serializer.data)

    except Exception as e:
        # Trả về thông báo lỗi nếu có vấn đề xảy ra trong quá trình xử lý
        return Response({'error': str(e), "status":status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)