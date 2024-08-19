from django.contrib import admin
from .models import Request

class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'requester', 'guardian', 'type', 'status', 'created_at', 'is_active')
    list_filter = ('type', 'status', 'created_at', 'is_active')
    search_fields = ('title', 'description', 'requester__username', 'guardian__username', 'is_active')
    fields = ('requester', 'guardian', 'title', 'description', 'type', 'status', 'is_active')
    list_per_page = 20
    verbose_name = "Requisição"
    verbose_name_plural = "Requisições"

admin.site.register(Request, RequestAdmin)