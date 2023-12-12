from base.models import Department, UserAccount
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        

class UserAccountWithDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('user_id', 'email', 'name', 'is_active', 'is_staff', 'username', 
                  'first_name', 'last_name', 'phone_number', 'address', 'date_of_birth', 'date_of_hire', 'status')

class DepartmentWithUserAccountSerializer(serializers.ModelSerializer):
    employee_id = UserAccountWithDepartmentSerializer(source='employee', read_only=True)

    class Meta:
        model = Department
        fields = '__all__'

        

