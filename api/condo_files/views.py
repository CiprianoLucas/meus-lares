from soft_components.views import SoftModelsViewSet

from .models import AptInspectImages, ContractFiles
from .serializers import AptInspectImagesSerializer, ContractsFilesSerializer


class ContractsFilesView(SoftModelsViewSet):
    serializer_class = ContractsFilesSerializer

    def get_queryset(self):
        images = ContractFiles.objects.all()
        return images


class AptInspectImagesView(SoftModelsViewSet):
    serializer_class = AptInspectImagesSerializer

    def get_queryset(self):
        user = self.request.user
        images = AptInspectImages.objects.filter(
            tenant__apartment__condominium__condostaff__user=user,
            tenant__apartment__condominium__condostaff__rule__in=["owner", "manager"],
        )
        return images
