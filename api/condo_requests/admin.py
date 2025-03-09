from django.contrib import admin
from django.utils.translation import gettext_lazy as _

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
    verbose_name = _("Request")
    verbose_name_plural = _("Requests")
    inlines = [RequestFilesInline]


admin.site.register(CondoRequest, RequestAdmin)
