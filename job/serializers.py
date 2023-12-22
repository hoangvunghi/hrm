from rest_framework import serializers
from base.models import Employee
from .models import Job
from base.serializers import EmployeeSerializer

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        # fields = ["JobID","JobName","JobChangeHour"]
        fields="__all__"

class EmployeeWithJobSerializer(serializers.Serializer):
    job = JobSerializer()
        
class JobWithEmployeeSerializer(serializers.ModelSerializer):
    employee_id = EmployeeWithJobSerializer(source='employee', read_only=True)
    class Meta:
        model = Job
        fields = '__all__'

class TotalEmployeeWithJobSerializer(serializers.Serializer):
    employee = EmployeeSerializer()
    job = JobSerializer()
