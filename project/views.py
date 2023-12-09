from rest_framework.decorators import api_view, permission_classes
from base.models import Project, UserAccount
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from rest_framework.response import Response
from rest_framework import status, permissions
# Create your views here.
from .serializers import ProjectSerializer
from rest_framework import permissions
from django.db.models import Q
# from django.http import Http404

def is_valid(data):
    errors = {}
    proj_name = data.get('proj_name','')
    proj_value = data.get('proj_value', '')
    # date_start = data.get('date_start', '')
    # date_end = data.get('data_end', '')
    proj_description = data.get('proj_description', '').lower()
    manager_id = data.get('manager_id', '')
    if not proj_name:
        errors['proj_name']= 'proj_name is required'
    if not proj_value:
        errors['proj_value']= 'proj_value is required'
    # if not date_start:
    #     errors['date_start']= "date_start is required"
    # if not date_end:
    #     errors['date_end']= "date_end number is required"
    if not proj_description:
        errors['proj_description']= "proj_description number is required"
    if not manager_id:
        errors['manager_id']= "manager_id number is required"
    return errors

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def create_project(request):

    errors = is_valid(request.data)
    if len(errors):
        return Response({"error":errors}, status=status.HTTP_400_BAD_REQUEST)
    
    project = ProjectSerializer(data=request.data)

    if project.is_valid():
        proj_id = request.data.get('proj_id', None)
        manager_id = request.data.get('manager_id', None)

        if Project.objects.filter(proj_id=proj_id).exists():
            return Response({"error": f"Project with id {proj_id} already exist", "status":status.HTTP_400_BAD_REQUEST}, 
                            status=status.HTTP_400_BAD_REQUEST)

        project.save()
        return Response({"message": "Project's create successfully", "status":status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    data= project.errors
    return Response(project.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def update_project(request, id):
    try:
        project = Project.objects.get(proj_id=id)
    except Project.DoesNotExist:
        return Response({"error": "Project not found", "status":status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        prj = ProjectSerializer(project, data=request.data)
        if prj.is_valid():
            prj.save()
            return Response(prj.data, status=status.HTTP_200_OK)
        return Response(prj.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def delete_project(request, id):
    try:
        project = Project.objects.get(proj_id = id)
    except Project.DoesNotExist:
        return Response({"error": "Project not found", "status":status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        if project.proj_id is not None:
            project.delete()
            return Response({"message": "Project deleted successfully", "status":status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid proj_id", "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"]) 
def find_project(request):
    try:
        q = request.GET.get('q', '')
        project = Project.objects.filter(
            Q(proj_id__icontains=q)|
            Q(proj_name__icontains=q)|
            Q(manager_id__icontains=q)|
            Q(proj_description__icontains=q)|
            Q(complete__icontains=q)|
            Q(date_start__icontains=q)|
            Q(date_end__icontains=q)
        )
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error':str(e), "status":status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
def project_list(request):
    project = Project.objects.all().order_by('-date_start')
    serializer = ProjectSerializer(project, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)