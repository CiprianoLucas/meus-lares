from rest_framework import serializers
from .models import Request, Images

class RequestSerializer(serializers.ModelSerializer):
    # images = serializers.FileField(write_only=True)
    
    class Meta:
        model = Request
        fields = ['id', 'place', 'title', 'description', 'type', 'images', 'status']
        extra_kwargs = {
            'status': {'read_only': True},
        }
        
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        request = Request.objects.create(**validated_data)
        for image_data in images_data:
            Images.objects.create(request=request, **image_data)
        return request
    
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        instance.images.all().delete()
        for image_data in images_data:
            Images.objects.create(request=instance, **image_data)

        return instance
    
    def delete(self, instance, validated_data=None):
        instance.is_active = False
        instance.save()
        return instance
    
class StatusRequestSerializer(serializers.Serializer):
    status = serializers.ChoiceField(Request.STATUS_CHOICES ,help_text="status")
    username = serializers.CharField(help_text="user_id", read_only=True)
    email = serializers.EmailField(help_text="user_id", read_only=True)