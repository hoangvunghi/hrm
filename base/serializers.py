from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Employee,UserAccount
from job.models import Job
from department.models import Department

# UserAccount=get_user_model()
# class JobSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Job
#         fields = ('JobName',)

# class DepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Department
#         fields = ('DepName',)
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields="__all__"

class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields="__all__"
        # fields=["EmpID","EmpName"]

# class EmployeeSerializerData(serializers.ModelSerializer):
#     Job = JobSerializer()
#     Department = DepartmentSerializer()

#     class Meta:
#         model = Employee
#         fields = ('EmpID', 'EmpName', 'Phone', 'HireDate', 'BirthDate', 'Address', 'PhotoPath', 'Email', 'EmpStatus', 'Job', 'Department')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'
        extra_kwargs = {
        'password': {'write_only': True},
        }
    def create(self, validated_data):
        password = validated_data.get('password')
        user = UserAccount.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    def update(self, instance, validated_data):
        validated_data.update(self.initial_data)
        return super().update(instance=instance, validated_data=validated_data)
    
class UserSerializerWithEmployeeSerializer(serializers.ModelSerializer):
    employee_id = UserSerializer(source='employee', read_only=True)
    class Meta:
        model = Employee
        fields = '__all__'
    def create(self, validated_data):
        user_data = validated_data.pop('employee', {})
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        employee = Employee.objects.create(EmpID=user, **validated_data)
        return employee
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token, if needed
        token['UserID'] = user.UserID
        return token

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = UserAccount
        # fields = '__all__'
        fields = [   'password', 'password2'
                #   ,'phone_number', 'date_of_birth', 'date_of_hire', 'first_name', 'last_name', 
                #   'address', 'status'
                  ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'read_only': True}
        }
    def __validate__(self, data):
        error= {}
        password = data['password']
        password2 = data['password2']
        if password != password2:
            error['password']= "Password Does not match"
        # if UserAccount.objects.filter(email = data['email']).exists():
        #     error["email"] = "Email already exist"
        return error
    def is_valid(self, *, raise_exception=False):
        error= self.__validate__(self.initial_data)
        if len(error)>0:
            self._errors= error
        return super().is_valid(raise_exception=raise_exception)
    def create(self, validate_data):
        validate_data.pop('password2')
        print(validate_data)
        return UserAccount.objects.create_user(**validate_data)