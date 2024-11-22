from django.contrib import admin
from django.utils.html import format_html
from .models import Condominium, Apartment
from relations.models import CondoStaff, CondoTenant
from soft_components import SoftAdmin, SoftInline

class CondoStaffInline(SoftInline):
    model = CondoStaff


class CondoTenantInline(SoftInline):
    model = CondoTenant

class CondominiumsAdmin(SoftAdmin):
    list_display = ('id', 'name', 'number', 'street', 'city', 'city__state', 'is_active', 'created_at', 'profile_photo_url')
    list_filter = ('is_active','city__state')
    search_fields = ('id', 'name', 'number', 'street', 'city')
    inlines = [CondoStaffInline]

    class Meta:
        verbose_name = "Condomínio"
        verbose_name_plural = "Condomínios"
    
    def profile_photo_url(self, obj):
        if obj.temporary_url():
            return format_html(f'<a href="{obj.temporary_url()}"><img src="{obj.temporary_url()}" alt="Foto de perfil" width="50" height="50"></a>')
        return "Sem foto"

    profile_photo_url.short_description = 'Foto'

class ApartmentsAdmin(SoftAdmin):
    list_display = ('id', 'condominium', 'identifier', 'profile_photo_url', 'is_active')
    list_filter = ('id', 'condominium', 'identifier','is_active')
    search_fields = ('id', 'condominium__name', 'identifier', 'is_active')
    inlines = [CondoTenantInline]
    verbose_name = "Apartamento"
    verbose_name_plural = "Apartamentos"
    
    def profile_photo_url(self, obj):
        if obj.temporary_url():
            return format_html(f'<a href="{obj.temporary_url()}"><img src="{obj.temporary_url()}" alt="Foto de perfil" width="50" height="50"></a>')
        return "Sem foto"

    profile_photo_url.short_description = 'Foto'

admin.site.register(Condominium, CondominiumsAdmin)
admin.site.register(Apartment, ApartmentsAdmin)