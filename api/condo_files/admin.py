from soft_components import SoftAdmin
from .models import ContractFiles, AptInspectImages
from django.contrib import admin

class ConstractFilesAdmin(SoftAdmin):
    list_display = ('constract', 'name', 'file', 'created_at')
    list_filter = ('constract', 'constract__content_type__model', 'created_at')
    search_fields = ('constract__content_type__model', 'name')

    class Meta:
        verbose_name = "Arquivo de contrato"
        verbose_name_plural = "Arquivos de contratos"

admin.site.register(ContractFiles, ConstractFilesAdmin)

class AptInspectImagesAdmin(SoftAdmin):
    list_display = ('tenant', 'role', 'created_at')
    list_filter = ('tenant', 'role', 'created_at')

    class Meta:
        verbose_name = "Arquivo de contrato"
        verbose_name_plural = "Arquivos de contratos"

admin.site.register(AptInspectImages, AptInspectImagesAdmin)