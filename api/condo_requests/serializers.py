from rest_framework import serializers
from soft_components.serializers import softModelSerializer

from .models import CondoRequest
from condo_files.models import RequestFiles
class CondoRequestSerializer(softModelSerializer):
    files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    class Meta:
        model = CondoRequest
        fields = [
            "id",
            "requester",
            "guardian",
            "condominium",
            "apartment",
            "title",
            "description",
            "observations",
            "type",
            "status",
            "anonymous",
            "files"
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "anonymous": {"write_only": True},
        }
        
    def create(self, validated_data):
        files = validated_data.pop("files", None)
        request = super().create(validated_data)
        if files:
            file_request = [RequestFiles(request=request, file=file) for file in files]
            RequestFiles.objects.bulk_create(file_request)

        return request
    
    def to_representation(self, instance: CondoRequest):
        representation = super().to_representation(instance)
        if instance.anonymous:
            representation["requester"] = None
        return representation