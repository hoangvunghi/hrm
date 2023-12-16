from rest_framework import serializers
from base.models import Employee
from .models import TimeSheet

class TimeSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSheet
        fields = "__all__" 
        

class UserAccountWithTimeSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        
class TimeSheetWithUserAccountSerializer(serializers.ModelSerializer):
    employee_id = UserAccountWithTimeSheetSerializer(source='employee', read_only=True)

    class Meta:
        model = TimeSheet
        fields = '__all__'

        

