from soft_components.views import SoftModelsViewSet

from .models import AptInspectImages, ContractFiles
from .serializers import AptInspectImagesSerializer, ContractsFilesSerializer


class ContractsFilesView(SoftModelsViewSet):
    serializer_class = ContractsFilesSerializer

    def get_queryset(self):
        user = self.request.user
        images = ContractFiles.objects.filter(
            tenant__apartment__condominium__condostaff__user=user,
            tenant__apartment__condominium__condostaff__role__in=["owner", "manager"],
        )
        return images


class AptInspectImagesView(SoftModelsViewSet):
    serializer_class = AptInspectImagesSerializer

    def get_queryset(self):
        user = self.request.user
        images = AptInspectImages.objects.filter(
            tenant__apartment__condominium__condostaff__user=user,
            tenant__apartment__condominium__condostaff__role__in=["owner", "manager"],
        )
        return images
