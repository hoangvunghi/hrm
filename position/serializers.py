from rest_framework import serializers
from base.models import UserAccount, Positions

class PositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positions
        fields = "__all__" 
        

class UserAccountWithPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('user_id', 'email', 'name', 'is_active', 'is_staff', 'username', 'first_name', 'last_name', 'phone_number', 'address', 'date_of_birth', 'date_of_hire', 'status')

class PositionWithUserAccountSerializer(serializers.ModelSerializer):
    employee_id = UserAccountWithPositionSerializer(source='employee', read_only=True)

    class Meta:
        model = Positions
        fields = '__all__'

        

