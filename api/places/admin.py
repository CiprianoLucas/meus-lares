from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from relations.models import CondoStaff, CondoTenant
from soft_components import SoftAdmin, SoftInline

from .models import Apartment, Condominium, ParkingSpace


class ApartmentsInline(SoftInline):
    model = Apartment


class CondoStaffInline(SoftInline):
    model = CondoStaff


class CondoTenantInline(SoftInline):
    model = CondoTenant


class CondominiumsAdmin(SoftAdmin):
    list_display = (
        "id",
        "name",
        "number",
        "street",
        "city",
        "city__state",
        "is_active",
        "created_at",
        "profile_photo_url",
    )
    list_filter = ("is_active", "city__state")
    search_fields = ("id", "name", "number", "street", "city")
    inlines = [CondoStaffInline, ApartmentsInline]

    class Meta:
        verbose_name = _("Condominium")
        verbose_name_plural = _("Condominiums")

    def profile_photo_url(self, obj):
        if obj.temporary_url():
            return format_html(
                f"""<a href="{obj.temporary_url()}"><img src="{obj.temporary_url()}"
                alt="Foto de perfil" width="50" height="50"></a>"""
            )
        return _("No photo")

    profile_photo_url.short_description = _("Photo")


class ApartmentsAdmin(SoftAdmin):
    list_display = ("id", "condominium", "identifier", "profile_photo_url", "is_active")
    list_filter = ("id", "condominium", "identifier", "is_active")
    search_fields = ("id", "condominium__name", "identifier", "is_active")
    inlines = [CondoTenantInline]
    verbose_name = _("Apartment")
    verbose_name_plural = _("Apartments")

    def profile_photo_url(self, obj):
        if obj.temporary_url():
            return format_html(
                f"""<a href="{obj.temporary_url()}"><img src="{obj.temporary_url()}"
                alt="Foto de perfil" width="50" height="50"></a>"""
            )
        return _("No photo")

    profile_photo_url.short_description = _("Photo")


class ParkingSpaceAdmin(SoftAdmin):
    list_display = ("id", "condominium", "identifier", "apartment")
    list_filter = ("condominium", "apartment")
    search_fields = ("id", "condominium__name", "identifier", "apartment__identifier")
    verbose_name = _("Parking space")
    verbose_name_plural = _("Parking spaces")


admin.site.register(ParkingSpace, ParkingSpaceAdmin)
admin.site.register(Condominium, CondominiumsAdmin)
admin.site.register(Apartment, ApartmentsAdmin)
