from condo_requests.models import CondoRequest
from django.db import models
from meus_lares.storages import PrivateMediaStorage, validate_file
from relations.models import CondoTenant, CondoTenantContract
from soft_components import SoftModel
from django.utils.translation import gettext_lazy as _


class CondoTenantContractFiles(SoftModel):
    contract = models.ForeignKey(
        CondoTenantContract, verbose_name=_("contract"), on_delete=models.DO_NOTHING
    )
    file = models.FileField(
        _("file"),
        upload_to="relations/contracts/files",
        validators=[validate_file],
        storage=PrivateMediaStorage(),
    )
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        verbose_name = _("Contract file")
        verbose_name_plural = _("Contract files")


class AptInspectImages(SoftModel):
    ROLE_CHOICES = [("in", _("In")), ("out", _("Out")), ("inspect", _("Inspect"))]

    tenant = models.ForeignKey(
        CondoTenant, verbose_name=_("tenant"), on_delete=models.DO_NOTHING
    )
    image = models.ImageField(
        _("image"), upload_to="relations/tenant/images", storage=PrivateMediaStorage()
    )
    role = models.CharField(_("role"), max_length=10, choices=ROLE_CHOICES)

    class Meta:
        verbose_name = _("Apartment Inspection Image")
        verbose_name_plural = _("Apartment Inspection Images")


class RequestFiles(SoftModel):
    file = models.FileField(
        _("file"), upload_to="requests/files/", storage=PrivateMediaStorage()
    )
    request = models.ForeignKey(
        CondoRequest, verbose_name=_("request"), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Request file")
        verbose_name_plural = _("Request files")

    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super().delete(*args, **kwargs)
