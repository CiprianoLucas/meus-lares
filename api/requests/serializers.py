from rest_framework import serializers
from .models import Request, RequestFiles


class RequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ["status"]
        extra_kwargs = {
            "status": {"write_only": True},
        }


class RequestSerializer(serializers.ModelSerializer):
    place_name = serializers.SerializerMethodField()
    files = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )

    class Meta:
        model = Request
        fields = ["id", "place", "place_name", "title", "description", "type", "status", "files"]
        extra_kwargs = {
            "status": {"read_only": True},
            "place_name": {"read_only": True},
        }

    def create(self, validated_data):
        files = validated_data.pop("files", [])
        request = Request.objects.create(**validated_data)

        for file in files:
            RequestFiles.objects.create(request=request, file=file)
        return request

    def get_place_name(self, obj):
        if obj.place:
            return obj.place.name
        return None

    def delete(self, instance, validated_data=None):
        instance.is_active = False
        instance.save()
        return instance


class StatusRequestSerializer(serializers.Serializer):
    status = serializers.ChoiceField(Request.STATUS_CHOICES, help_text="status")
    username = serializers.CharField(help_text="user_id", read_only=True)
    email = serializers.EmailField(help_text="user_id", read_only=True)
