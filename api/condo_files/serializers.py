from soft_components.serializers import softModelSerializer

from .models import AptInspectImages, CondoTenantContractFiles


class CondoTenantConstractsFilesSerializer(softModelSerializer):
    class Meta:
        model = CondoTenantContractFiles
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
