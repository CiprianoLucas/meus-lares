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
    id = serializers.UUIDField(help_text="user_id")
    username = serializers.CharField(help_text="user_id", read_only=True)
    email = serializers.EmailField(help_text="user_id", read_only=True)
