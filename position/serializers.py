from base.models import Positions
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers


class PositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positions
        fields = '__all__'