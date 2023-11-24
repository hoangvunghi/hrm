from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
User=get_user_model()


        
class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    number_phone = serializers.CharField(required=True) 
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2','number_phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({"Error": "Password Does not match"})
        
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({"Error": "Email already exist"})
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        account.number_phone = self.validated_data['number_phone']
        account.save()
        
        return account