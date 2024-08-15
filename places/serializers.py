from rest_framework import serializers
from .models import Places

class PlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Places
        fields = ['id', 'name', 'number', 'street', 'city', 'state']
        
class UserPlaceSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(help_text="user_id")