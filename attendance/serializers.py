from rest_framework import serializers
from base.models import UserAccount, Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__" 
        

class UserAccountWithAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('user_id', 'email', 'name', 'is_active', 'is_staff', 'username', 'first_name', 'last_name', 'phone_number', 'address', 'date_of_birth', 'date_of_hire', 'status')

class AttendanceWithUserAccountSerializer(serializers.ModelSerializer):
    employee_id = UserAccountWithAttendanceSerializer(source='employee', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'

        

