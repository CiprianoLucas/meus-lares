from rest_framework import serializers
from .models import Request

class RequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['status']
        extra_kwargs = {
            'status': {'write_only': True},
        }

class RequestSerializer(serializers.ModelSerializer):
    place_name = serializers.SerializerMethodField()
    class Meta:
        model = Request
        fields = ['id','place' ,'place_name', 'title', 'description', 'type', 'status']
        extra_kwargs = {
            'status': {'read_only': True},
            'place_name': {'read_only': True},
        }
        
    def get_place_name(self, obj):
        if obj.place:
            return obj.place.name
        return None
    
    def delete(self, instance, validated_data=None):
        instance.is_active = False
        instance.save()
        return instance
    
class StatusRequestSerializer(serializers.Serializer):
    status = serializers.ChoiceField(Request.STATUS_CHOICES ,help_text="status")
    username = serializers.CharField(help_text="user_id", read_only=True)
    email = serializers.EmailField(help_text="user_id", read_only=True)