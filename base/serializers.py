from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserAccount

User=get_user_model()


        
# class UserRegisterSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#     number_phone = serializers.CharField(required=True) 
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'password2','number_phone']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
    
#     def save(self):
#         password = self.validated_data['password']
#         password2 = self.validated_data['password2']
        
#         if password != password2:
#             raise serializers.ValidationError({"Error": "Password Does not match"})
        
#         if User.objects.filter(email = self.validated_data['email']).exists():
#             raise serializers.ValidationError({"Error": "Email already exist"})
        
#         account = User(email=self.validated_data['email'], username=self.validated_data['username'])
#         account.set_password(password)
#         account.save()
#         account.number_phone = self.validated_data['number_phone']
#         account.save()
        
#         return account
    


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'
        extra_kwargs = {
        'password': {'write_only': True},
        }
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def create(self, validated_data):
        password = validated_data.get('password')
        user = UserAccount.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        validated_data.update(self.initial_data)
        return super().update(instance=instance, validated_data=validated_data)
    
    # def validate(self, data):
    #     print("ffff",data)
    #     request = self.context.get('request')
    #     print(request)
    #     current_user_id = request.UserAccount.id if request and request.UserAccount else None
    #     print(current_user_id)
    #     if UserAccount.objects.filter(username=data['username']).exclude(id=current_user_id).exists():
    #          raise serializers.ValidationError("User already exists")
        
    #     return data


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['name', 'username', 'email', 'password', 'password2'
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
        
        if User.objects.filter(email = data['email']).exists():
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
        return User.objects.create_user(**validate_data)

