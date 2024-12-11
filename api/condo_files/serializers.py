from soft_components.serializers import softModelSerializer

from .models import AptInspectImages, ContractFiles


class ContractsFilesSerializer(softModelSerializer):
    class Meta:
        model = ContractFiles
        fields = [
            "id",
            "contract",
            "file",
            "name",
        ]
        extra_kwargs = {"id": {"read_only": True}}


class AptInspectImagesSerializer(softModelSerializer):
    class Meta:
        model = AptInspectImages
        fields = [
            "id",
            "tenant",
            "image",
            "role",
        ]
        extra_kwargs = {"id": {"read_only": True}}
