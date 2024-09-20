from django.contrib import admin
from .models import Place

class PlacesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number', 'street', 'city', 'state', 'is_active', 'created_at', 'representative')
    list_filter = ('id', 'is_active', 'city', 'state', 'representative')
    search_fields = ('id', 'name', 'number', 'street', 'city', 'state', 'representative__username')
    fields = ('representative', 'residents', 'unions', 'name', 'number', 'street', 'city', 'state', 'is_active', 'profile_photo')
    list_per_page = 20
    verbose_name = "Local"
    verbose_name_plural = "Locais"

admin.site.register(Place, PlacesAdmin)