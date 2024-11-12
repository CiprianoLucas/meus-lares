from django.contrib import admin
from django.utils.html import format_html
from .models import Place

class PlacesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number', 'street', 'city', 'city__state', 'is_active', 'created_at', 'representative', 'profile_photo_url')
    list_filter = ('id', 'is_active', 'city','city__state', 'representative')
    search_fields = ('id', 'name', 'number', 'street', 'city', 'representative__username')
    fields = ('representative', 'residents', 'unions', 'name', 'number', 'street', 'city', 'is_active', 'profile_photo')
    list_per_page = 20
    verbose_name = "Local"
    verbose_name_plural = "Locais"
    
    def profile_photo_url(self, obj):
        if obj.temporary_url():
            return format_html(f'<a href="{obj.temporary_url()}"><img src="{obj.temporary_url()}" alt="Foto de usuário" width="50" height="50"></a>')
        return "Sem foto"

    profile_photo_url.short_description = 'Foto'

admin.site.register(Place, PlacesAdmin)