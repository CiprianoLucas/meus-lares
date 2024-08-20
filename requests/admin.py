from django.contrib import admin
from .models import Request

class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'place','title', 'requester', 'guardian', 'type', 'status', 'created_at', 'is_active')
    list_filter = ('id','place','type', 'status', 'created_at', 'is_active')
    search_fields = ('id','place','title', 'description', 'requester__username', 'guardian__username', 'is_active')
    fields = ('place', 'requester', 'guardian', 'title', 'description', 'type', 'status', 'is_active')
    list_per_page = 20
    verbose_name = "Requisição"
    verbose_name_plural = "Requisições"

admin.site.register(Request, RequestAdmin)