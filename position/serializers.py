from rest_framework import serializers
from base.models import Employee, Position

class PositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__" 
        

class EmployeeWithPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        
class PositionWithEmployeeSerializer(serializers.ModelSerializer):
    employee_id = EmployeeWithPositionSerializer(source='employee', read_only=True)

    class Meta:
        model = Position
        fields = '__all__'

        

