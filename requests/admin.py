from django.contrib import admin
from .models import Request

class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'requester', 'guardian', 'type', 'status', 'created_at')
    list_filter = ('type', 'status', 'created_at')
    search_fields = ('title', 'description', 'requester__username', 'guardian__username')
    fields = ('requester', 'guardian', 'title', 'description', 'type', 'status')
    list_per_page = 20
    verbose_name = "Requisição"
    verbose_name_plural = "Requisições"

admin.site.register(Request, RequestAdmin)