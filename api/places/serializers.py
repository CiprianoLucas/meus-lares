import re
from rest_framework import serializers
from .models import Place, City
class PlacesSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    class Meta:
        model = Place
        fields = ['id', 'name', 'number', 'complement', 'neighborhood', 'street', 'city', 'cep', 'city_name', 'state']
        extra_kwargs = {
            "id": {"read_only": True},
            "city_name": {"read_only": True},
            "state": {"read_only": True},
        }
    
    def get_state(self, obj):
        if obj.city:
            return obj.city.state.acronym
        return None
    
    def get_city_name(self, obj):
        if obj.city:
            return obj.city.name
        return None

    def to_internal_value(self, data):
        data = data.copy()
        if 'cep' in data:
            data['cep'] = re.sub(r'\D', '', data['cep'])
        return super().to_internal_value(data)
        
    def delete(self, instance, validated_data=None):
        instance.is_active = False
        instance.save()
        return instance
        
class UserPlaceSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    
class CitySerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    class Meta:
        model = City
        fields = ["id", "name", "state"]
        extra_kwargs = {
            "id": {"read_only": True},
            "name": {"read_only": True},
            "state": {"read_only": True},
        }

    def get_state(self, obj):
        if obj.state:
            return obj.state.acronym
        return None

class FullAddressSerializer(serializers.Serializer):
    state = serializers.CharField()
    city = serializers.IntegerField(required=False, allow_null=True)
    neighborhood = serializers.CharField(required=False, allow_null=True)
    street = serializers.CharField(required=False, allow_null=True)
