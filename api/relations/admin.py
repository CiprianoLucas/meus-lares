from django.contrib import admin
from relations.models import CondoStaff, CondoTenant, Contract
from soft_components import SoftAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html

class ConstractsInline(GenericTabularInline):
    model = Contract
    extra = 0
    exclude = ('is_deleted', 'history', 'created_at')
    can_delete = False

class CondoStaffAdmin(SoftAdmin):
    list_display = ('id', 'condominium', 'user', 'role')
    list_filter = ('condominium','user', 'role')
    search_fields = ('condominium__name', 'user__username', 'role')
    inlines = [ConstractsInline]

    class Meta:
        verbose_name = "Colaborador do condomínio"
        verbose_name_plural = "Colaboradores do condomínio"

class CondoTenantAdmin(SoftAdmin):
    list_display = ('apartment', 'user', 'is_renter', 'is_responsible', 'apartment__condominium')
    list_filter = ('user', 'is_renter', 'is_responsible', 'apartment__condominium')
    search_fields = ('apartment__identifier', 'user__username', 'apartment__condominium__name')
    inlines = [ConstractsInline]

    class Meta:
        verbose_name = "Morador"
        verbose_name_plural = "Moradores"


class ConstractsAdmin(SoftAdmin):
    list_display = ('content_type', 'object_id', 'is_renter', 'is_responsible')
    list_filter = ('user', 'is_renter', 'is_responsible', 'apartment__condominium')
    search_fields = ('apartment__identifier', 'user__username', 'apartment__condominium__name')
    inlines = [ConstractsInline]

    class Meta:
        verbose_name = "Morador"
        verbose_name_plural = "Moradores"

class ContractAdmin(SoftAdmin):
    list_display = ('id', 'related_object', 'start_date', 'end_date', 'is_active')
    list_filter = ('start_date', 'end_date', 'content_type')
    search_fields = ('related_object__str', 'terms')

admin.site.register(Contract, ContractAdmin)
admin.site.register(CondoStaff, CondoStaffAdmin)
admin.site.register(CondoTenant, CondoTenantAdmin)