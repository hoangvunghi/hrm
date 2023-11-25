from base.models import Leave
from django.contrib.auth import get_user_model
from rest_framework import serializers


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'