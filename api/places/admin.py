from django.contrib import admin
from .models import Places

class PlacesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number', 'street', 'city', 'state', 'is_active', 'created_at', 'representative')
    list_filter = ('id', 'is_active', 'city', 'state', 'representative')
    search_fields = ('id', 'name', 'number', 'street', 'city', 'state', 'representative__username')
    fields = ('representative', 'residents', 'unions', 'name', 'number', 'street', 'city', 'state', 'is_active', 'profile_photo')
    list_per_page = 20
    verbose_name = "Lugar"
    verbose_name_plural = "Lugares"

admin.site.register(Places, PlacesAdmin)