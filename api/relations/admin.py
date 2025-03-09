from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from relations.models import (
    CondoStaff,
    CondoTenant,
    CondoTenantContract,
    PlaceReservation,
)
from soft_components import SoftAdmin, SoftInline


class CondoTenantConstractsInline(SoftInline):
    model = CondoTenantContract


class CondoStaffAdmin(SoftAdmin):
    list_display = ("id", "condominium", "user", "role")
    list_filter = ("condominium", "user", "role")
    search_fields = ("condominium__name", "user__full_name", "role")

    class Meta:
        verbose_name = _("Condominium staff")
        verbose_name_plural = _("Condominium staffs")


class CondoTenantAdmin(SoftAdmin):

    def condominium(self, obj: CondoTenant):
        return obj.apartment.condominium if obj.apartment else None

    condominium.short_description = _("Condominium")

    list_display = (
        "id",
        "apartment",
        "user",
        "is_responsible",
        "condominium",
    )
    list_filter = ("user", "is_responsible", "apartment__condominium")
    search_fields = (
        "apartment__identifier",
        "user__full_name",
        "apartment__condominium__name",
    )

    inlines = [CondoTenantConstractsInline]

    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")


class CondoTenantContractAdmin(SoftAdmin):
    list_display = ("id", "start_date", "end_date", "is_active")
    list_filter = ("start_date", "end_date")


class PlaceReservationAdmin(SoftAdmin):
    list_display = ("place", "tenant", "date", "start_time", "end_time")
    list_filter = ("place", "tenant", "date", "start_time", "end_time")
    search_fields = (
        "place__name",
        "tenant__user__fullname",
        "date",
    )

    class Meta:
        verbose_name = _("Space reservation")
        verbose_name_plural = _("Space Reservations")


admin.site.register(PlaceReservation, PlaceReservationAdmin)
admin.site.register(CondoTenantContract, CondoTenantContractAdmin)
admin.site.register(CondoStaff, CondoStaffAdmin)
admin.site.register(CondoTenant, CondoTenantAdmin)
