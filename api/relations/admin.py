from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from relations.models import CondoStaff, CondoTenant, Contract, PlaceReservation
from soft_components import SoftAdmin


class ConstractsInline(GenericTabularInline):
    model = Contract
    extra = 0
    exclude = ("is_deleted", "history", "created_at")
    can_delete = False


class CondoStaffAdmin(SoftAdmin):
    list_display = ("id", "condominium", "user", "role")
    list_filter = ("condominium", "user", "role")
    search_fields = ("condominium__name", "user__username", "role")
    inlines = [ConstractsInline]

    class Meta:
        verbose_name = "Colaborador do condomínio"
        verbose_name_plural = "Colaboradores do condomínio"


class CondoTenantAdmin(SoftAdmin):
    list_display = (
        "id",
        "apartment",
        "user",
        "is_renter",
        "is_responsible",
        "apartment__condominium",
    )
    list_filter = ("user", "is_renter", "is_responsible", "apartment__condominium")
    search_fields = (
        "apartment__identifier",
        "user__username",
        "apartment__condominium__name",
    )
    inlines = [ConstractsInline]

    class Meta:
        verbose_name = "Morador"
        verbose_name_plural = "Moradores"


class ContractAdmin(SoftAdmin):
    list_display = ("id", "related_object", "start_date", "end_date", "is_active")
    list_filter = ("start_date", "end_date", "content_type")
    search_fields = ("related_object__str", "terms")
    
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
admin.site.register(Contract, ContractAdmin)
admin.site.register(CondoStaff, CondoStaffAdmin)
admin.site.register(CondoTenant, CondoTenantAdmin)
