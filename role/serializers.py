from .models import Role
# from django.contrib.auth import get_user_model
from rest_framework import serializers


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'