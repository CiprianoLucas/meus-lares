from rest_framework import serializers
from .models import Places
class PlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Places
        fields = ['id', 'name', 'number', 'street', 'city', 'state']
        
    def delete(self, instance, validated_data=None):
        instance.is_active = False
        instance.save()
        return instance
        
class UserPlaceSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField()
