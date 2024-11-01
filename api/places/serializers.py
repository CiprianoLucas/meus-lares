from rest_framework import serializers
from .models import Place, City
class PlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'name', 'number', 'street', 'city']
        
    def delete(self, instance, validated_data=None):
        instance.is_active = False
        instance.save()
        return instance
        
class UserPlaceSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    
class CitySerializer(serializers.ModelSerializer):
    state_acronym = serializers.SerializerMethodField()
    class Meta:
        model = City
        fields = ["id", "name", "state_acronym"]
        extra_kwargs = {
            "id": {"read_only": True},
            "name": {"read_only": True},
            "state_acronym": {"read_only": True},
        }
    
    def get_state_acronym(self, obj):
        if obj.place:
            return obj.state.acronym
        return None
