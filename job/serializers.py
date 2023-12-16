from rest_framework import serializers
from base.models import Employee, Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__" 
        

class EmployeeWithJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        
class JobWithEmployeeSerializer(serializers.ModelSerializer):
    employee_id = EmployeeWithJobSerializer(source='employee', read_only=True)

    class Meta:
        model = Job
        fields = '__all__'

        

