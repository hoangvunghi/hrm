from base.models import LeaveType
from django.contrib.auth import get_user_model
from rest_framework import serializers


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'