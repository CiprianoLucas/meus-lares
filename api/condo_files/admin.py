from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from soft_components import SoftAdmin

from .models import AptInspectImages, CondoTenantContractFiles


class CondoTenantConstractFilesAdmin(SoftAdmin):
    list_display = ("contract", "name", "file", "created_at")
    list_filter = ("contract", "created_at")
    search_fields = ("name",)

    class Meta:
        verbose_name = _("Contract file")
        verbose_name_plural = _("Contract files")


admin.site.register(CondoTenantContractFiles, CondoTenantConstractFilesAdmin)


class AptInspectImagesAdmin(SoftAdmin):
    list_display = ("tenant", "role", "created_at")
    list_filter = ("tenant", "role", "created_at")

    class Meta:
        verbose_name = _("Instruction image")
        verbose_name_plural = _("Instruction images")


admin.site.register(AptInspectImages, AptInspectImagesAdmin)
