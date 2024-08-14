from django.contrib import admin
from .models import Places

class PlacesAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'street', 'city', 'state', 'enabled', 'created_at', 'representative')
    list_filter = ('enabled', 'city', 'state', 'representative')
    search_fields = ('name', 'number', 'street', 'city', 'state', 'representative__username')
    fields = ('representative', 'residents', 'unions', 'name', 'number', 'street', 'city', 'state', 'enabled')
    list_per_page = 20
    verbose_name = "Lugar"
    verbose_name_plural = "Lugares"

admin.site.register(Places, PlacesAdmin)