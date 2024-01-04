from base.models import  Employee
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import LeaveRequest


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        # fields =["LeaveTypeID","LeaveStartDate","LeaveEndDate","Reason","LeaveStatus"]
        fields="__all__"
    def save(self, *args, **kwargs):
        # Chuyển đổi Duration về kiểu int
        self.validated_data['Duration'] = int(self.validated_data['Duration'])

        # Tiếp tục với việc lưu bình thường
        super().save(*args, **kwargs)
        
class EmployeeWithLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        
class LeaveWithEmployeeSerializer(serializers.ModelSerializer):
    employee_id = EmployeeWithLeaveSerializer(source='employee', read_only=True)
    class Meta:
        model = LeaveRequest
        fields = '__all__'

        

