from rest_framework import serializers
from .models import Places

class PlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Places
        fields = ['id', 'representative', 'residents', 'unions', 'name', 'number', 'street', 'city', 'state', 'enabled', 'created_at']
        extra_kwargs = {
            'representative': {'read_only': True},
            'created_at': {'read_only': True}
        }
