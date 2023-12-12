from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Organization
from .serializers import OrganizationSerializer
from django.core.exceptions import ObjectDoesNotExist
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from base.views import is_valid_type,obj_update,validate_to_update
from django.core.paginator import Paginator,EmptyPage



@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def view_organization(request):
    try:
        organization = Organization.objects.get(pk=1) 
        serializer = OrganizationSerializer(organization) 
        return Response({"data":[serializer.data],"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
    except Organization.DoesNotExist:
        return Response({"error": "organization does not exits","status":status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)




@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadonly])
def update_organization(request, pk):
    try:
        org = Organization.load()
    except ObjectDoesNotExist:
        return Response(
            {"error": "Organization not found", "status": status.HTTP_404_NOT_FOUND},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'PATCH':
        errors= validate_to_update(org, request.data)
        if len(errors):
            return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
        obj_update(org, request.data)
        serializer=OrganizationSerializer(org)
        return Response({"messeger": "update succesfull", "data": str(serializer.data)}, status=status.HTTP_200_OK)