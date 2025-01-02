from django.contrib import admin
from soft_components import SoftAdmin
from .models import UserNotification, Notification

class UserNotificationInline(admin.TabularInline):
    extra = 0
    can_delete = False
    model = UserNotification

class NotificationAdmin(SoftAdmin):
    list_display = ("id", "title", "schedule", "condominium")
    list_filter = ("schedule", "condominium")
    search_fields = ("id", "title", "condominium__name", "schedule")
    verbose_name = "Notificação"
    verbose_name_plural = "Notificações"
    inlines = [UserNotificationInline]
    
admin.site.register(Notification, NotificationAdmin)