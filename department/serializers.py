from base.models import Employee
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()
    class Meta:
        model = Department
        fields = ['employee_count','DepID','DepName',"DepShortName",'ManageID']
    def get_employee_count(self, department):
        return Employee.objects.filter(DepID=department).count()
# class EmployeeWithDepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         fields = '__all__'
        
# class DepartmentWithEmployeeSerializer(serializers.ModelSerializer):
#     employee_id = EmployeeWithDepartmentSerializer(source='employee', read_only=True)
#     class Meta:
#         model = Department
#         fields = '__all__'

        

