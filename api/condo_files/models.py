from condo_requests.models import CondoRequest
from django.db import models
from meus_lares.storages import PrivateMediaStorage, validate_file
from relations.models import CondoTenant, CondoTenantContract
from soft_components import SoftModel


class CondoTenantContractFiles(SoftModel):
    contract = models.ForeignKey(CondoTenantContract, on_delete=models.DO_NOTHING)
    file = models.FileField(
        upload_to="relations/contracts/files",
        validators=[validate_file],
        storage=PrivateMediaStorage(),
    )
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Arquivo de contrato"
        verbose_name_plural = "Arquivos de contratos"


class AptInspectImages(SoftModel):
    ROLE_CHOICES = [("in", "In"), ("out", "Out"), ("inspect", "Inspect")]

    tenant = models.ForeignKey(CondoTenant, on_delete=models.DO_NOTHING)
    image = models.ImageField(
        upload_to="relations/tenant/images", storage=PrivateMediaStorage()
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        verbose_name = "Imagem de Inspeção de Apartamento"
        verbose_name_plural = "Imagens de Inspeção de Apartamentos"


class RequestFiles(SoftModel):
    file = models.FileField(upload_to="requests/files/", storage=PrivateMediaStorage())
    request = models.ForeignKey(CondoRequest, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Arquivo da requisição"
        verbose_name_plural = "Arquivos das requisições"

    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super().delete(*args, **kwargs)
