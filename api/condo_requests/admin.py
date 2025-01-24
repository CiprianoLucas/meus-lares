from django.contrib import admin

from condo_files.models import RequestFiles
from soft_components import SoftAdmin, SoftInline

from .models import CondoRequest


class RequestFilesInline(SoftInline):
    extra = 0
    can_delete = False
    model = RequestFiles


class RequestAdmin(SoftAdmin):
    list_display = (
        "id",
        "requester",
        "guardian",
        "condominium",
        "apartment",
        "title",
        "type",
        "status",
    )
    list_filter = ("requester", "guardian", "condominium", "type", "status")
    search_fields = (
        "id",
        "requester__email",
        "guardian__email",
        "condominium__name",
        "apartment__identfier",
        "title",
    )
    verbose_name = "Requisição"
    verbose_name_plural = "Requisições"
    inlines = [RequestFilesInline]


admin.site.register(CondoRequest, RequestAdmin)
