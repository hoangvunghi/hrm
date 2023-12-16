from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Employee,UserAccount

UserAccount=get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee

        fields='__all__'

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
        fields = [ 'username', 'email', 'password', 'password2'
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
        
        if UserAccount.objects.filter(email = data['email']).exists():
            error["email"] = "Email already exist"

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

