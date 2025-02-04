from django.contrib import admin
from relations.models import (CondoStaff, CondoTenant, CondoTenantContract,
                              PlaceReservation)
from soft_components import SoftAdmin, SoftInline


class CondoTenantConstractsInline(SoftInline):
    model = CondoTenantContract


class CondoStaffAdmin(SoftAdmin):
    list_display = ("id", "condominium", "user", "role")
    list_filter = ("condominium", "user", "role")
    search_fields = ("condominium__name", "user__full_name", "role")

    class Meta:
        verbose_name = "Colaborador do condomínio"
        verbose_name_plural = "Colaboradores do condomínio"


class CondoTenantAdmin(SoftAdmin):
    list_display = (
        "id",
        "apartment",
        "user",
        "is_responsible",
        "apartment__condominium",
    )
    list_filter = ("user", "is_responsible", "apartment__condominium")
    search_fields = (
        "apartment__identifier",
        "user__full_name",
        "apartment__condominium__name",
    )
    inlines = [CondoTenantConstractsInline]

    class Meta:
        verbose_name = "Morador"
        verbose_name_plural = "Moradores"


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
        verbose_name = "Reserva de espaço"
        verbose_name_plural = "Reservas de espaços"


admin.site.register(PlaceReservation, PlaceReservationAdmin)
admin.site.register(CondoTenantContract, CondoTenantContractAdmin)
admin.site.register(CondoStaff, CondoStaffAdmin)
admin.site.register(CondoTenant, CondoTenantAdmin)
