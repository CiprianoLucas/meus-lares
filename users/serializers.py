from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'cpf', 'phone_number', 'full_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}
