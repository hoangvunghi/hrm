from rest_framework import serializers
from base.models import Employee
from .models import SalaryHistory

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryHistory
        fields = "__all__"         

class EmployeeWithSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        
class SalaryWithEmployeeSerializer(serializers.ModelSerializer):
    employee_id = EmployeeWithSalarySerializer(source='employee', read_only=True)
    class Meta:
        model = SalaryHistory
        fields = '__all__'

        

