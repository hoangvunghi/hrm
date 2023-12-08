from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Organization
from .serializers import OrganizationSerializer
from django.core.exceptions import ObjectDoesNotExist
from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from base.views import is_valid_type
from django.core.paginator import Paginator,EmptyPage



@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def view_organization(request):
    try:
        organization = Organization.objects.get(pk=1) 
        serializer = OrganizationSerializer(organization) 
        return Response(serializer.data)
    except Organization.DoesNotExist:
        return Response({"error": "organization does not exits","status":status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)



@api_view([ 'PATCH'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly])
def update_organization(request):
    try:
        organization_instance = Organization.load()
    except ObjectDoesNotExist:
        return Response(
            {"error": "Organization not found", "status": status.HTTP_404_NOT_FOUND},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'PATCH':
        serializer = OrganizationSerializer(organization_instance, data=request.data)
        is_valid_type(serializer.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Organization information updated", "status": status.HTTP_200_OK},
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": serializer.errors, "status": status.HTTP_400_BAD_REQUEST},
            status=status.HTTP_400_BAD_REQUEST
        )