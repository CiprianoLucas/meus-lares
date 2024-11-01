from django.contrib import admin
from .models import Place

class PlacesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number', 'street', 'city', 'city__state', 'is_active', 'created_at', 'representative')
    list_filter = ('id', 'is_active', 'city','city__state', 'representative')
    search_fields = ('id', 'name', 'number', 'street', 'city', 'representative__username')
    fields = ('representative', 'residents', 'unions', 'name', 'number', 'street', 'city', 'is_active', 'profile_photo')
    list_per_page = 20
    verbose_name = "Local"
    verbose_name_plural = "Locais"

admin.site.register(Place, PlacesAdmin)