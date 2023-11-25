from base.models import Leave_Type
from django.contrib.auth import get_user_model
from rest_framework import serializers


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave_Type
        fields = '__all__'