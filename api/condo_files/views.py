from soft_components.views import SoftModelsViewSet

from .models import AptInspectImages, CondoTenantContractFiles
from .serializers import (AptInspectImagesSerializer,
                          CondoTenantConstractsFilesSerializer)


class CondoTenantContractsFilesView(SoftModelsViewSet):
    serializer_class = CondoTenantConstractsFilesSerializer

    def get_queryset(self):
        user = self.request.user
        images = CondoTenantContractFiles.objects.filter(
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
