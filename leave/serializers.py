from base.models import Leave, UserAccount
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'
        

class UserAccountWithLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('user_id', 'email', 'name', 'is_active', 'is_staff', 'username', 
                  'first_name', 'last_name', 'phone_number', 'address', 'date_of_birth', 'date_of_hire', 'status')

class LeaveWithUserAccountSerializer(serializers.ModelSerializer):
    employee_id = UserAccountWithLeaveSerializer(source='employee', read_only=True)

    class Meta:
        model = Leave
        fields = '__all__'

        

