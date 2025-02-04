from django.contrib import admin
from soft_components import SoftAdmin

from .models import AptInspectImages, CondoTenantContractFiles


class CondoTenantConstractFilesAdmin(SoftAdmin):
    list_display = ("contract", "name", "file", "created_at")
    list_filter = ("contract", "created_at")
    search_fields = ("name",)

    class Meta:
        verbose_name = "Arquivo de contrato"
        verbose_name_plural = "Arquivos de contratos"


admin.site.register(CondoTenantContractFiles, CondoTenantConstractFilesAdmin)


class AptInspectImagesAdmin(SoftAdmin):
    list_display = ("tenant", "role", "created_at")
    list_filter = ("tenant", "role", "created_at")

    class Meta:
        verbose_name = "Arquivo de contrato"
        verbose_name_plural = "Arquivos de contratos"


admin.site.register(AptInspectImages, AptInspectImagesAdmin)
