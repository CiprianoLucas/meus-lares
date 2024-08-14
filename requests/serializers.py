from rest_framework import serializers
from .models import Request, Images

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'image']

class RequestSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, required=False)

    class Meta:
        model = Request
        fields = ['id', 'requester', 'guardian', 'place', 'title', 'description', 'type', 'status', 'created_at', 'images']
        extra_kwargs = {
            'requester': {'read_only': True},
            'guardian': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        request = Request.objects.create(**validated_data)
        for image_data in images_data:
            Images.objects.create(request=request, **image_data)
        return request

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        if instance.status in ['A', 'C']:
            raise serializers.ValidationError("Cannot modify request when status is 'Andamento' or 'Concluído'.")

        user = self.context['request'].user
        if user == instance.guardian:
            instance.status = validated_data.get('status', instance.status)
        elif user == instance.requester:
            instance.title = validated_data.get('title', instance.title)
            instance.description = validated_data.get('description', instance.description)
            instance.type = validated_data.get('type', instance.type)
        else:
            raise serializers.PermissionDenied("You do not have permission to update this request.")

        instance.save()

        # Update images
        instance.images.all().delete()  # Remove old images
        for image_data in images_data:
            Images.objects.create(request=instance, **image_data)
        
        return instance
