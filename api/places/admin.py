from django.contrib import admin
from django.utils.html import format_html
from .models import Condominium, Apartment
from relations.models import CondoManager, CondoOwner, CondoTenant

class CondoManagerInline(admin.TabularInline):
    model = CondoManager
    extra = 0
    fields = ('user', 'start_day', 'end_day', 'is_active', 'notes')
    readonly_fields = ('created_at', 'deleted_at')
    can_delete = False

class CondoOwnerInline(admin.TabularInline):
    model = CondoOwner
    extra = 0
    fields = ('user', 'start_day', 'end_day', 'is_active', 'notes')
    readonly_fields = ('created_at', 'deleted_at')
    can_delete = False

class CondoTenantInline(admin.TabularInline):
    model = CondoTenant
    extra = 0
    fields = ('user', 'start_day', 'end_day', 'is_active', 'notes')
    readonly_fields = ('created_at', 'deleted_at')
    can_delete = False

class CondominiumsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number', 'street', 'city', 'city__state', 'is_active', 'created_at', 'profile_photo_url')
    list_filter = ('id', 'is_active', 'city','city__state')
    search_fields = ('id', 'name', 'number', 'street', 'city')
    fields = ('name', 'number', 'street', 'city', 'is_active', 'profile_photo')
    inlines = [CondoManagerInline, CondoOwnerInline]
    list_per_page = 20
    verbose_name = "Condomínio"
    verbose_name_plural = "Condomínios"
    
    def profile_photo_url(self, obj):
        if obj.temporary_url():
            return format_html(f'<a href="{obj.temporary_url()}"><img src="{obj.temporary_url()}" alt="Foto de perfil" width="50" height="50"></a>')
        return "Sem foto"

    profile_photo_url.short_description = 'Foto'

class ApartmentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'condominium', 'identifier', 'profile_photo_url', 'is_active')
    list_filter = ('id', 'condominium', 'identifier','is_active')
    search_fields = ('id', 'condominium', 'identifier', 'is_active')
    fields = ('condominium', 'identifier', 'profile_photo', 'is_active', 'complement')
    inlines = [CondoTenantInline]
    list_per_page = 20
    verbose_name = "Apartamento"
    verbose_name_plural = "Apartamentos"
    
    def profile_photo_url(self, obj):
        if obj.temporary_url():
            return format_html(f'<a href="{obj.temporary_url()}"><img src="{obj.temporary_url()}" alt="Foto de perfil" width="50" height="50"></a>')
        return "Sem foto"

    profile_photo_url.short_description = 'Foto'

admin.site.register(Condominium, CondominiumsAdmin)
admin.site.register(Apartment, ApartmentsAdmin)