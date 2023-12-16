from base.models import  Employee
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Leave


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'
        

class EmployeeWithLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        
class LeaveWithEmployeeSerializer(serializers.ModelSerializer):
    employee_id = EmployeeWithLeaveSerializer(source='employee', read_only=True)

    class Meta:
        model = Leave
        fields = '__all__'

        

