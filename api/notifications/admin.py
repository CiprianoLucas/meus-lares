from django.contrib import admin
from soft_components import SoftAdmin
from django.utils.translation import gettext_lazy as _
from .models import Notification, UserNotification


class UserNotificationInline(admin.TabularInline):
    extra = 0
    can_delete = False
    model = UserNotification


class NotificationAdmin(SoftAdmin):
    list_display = ("id", "title", "schedule", "condominium")
    list_filter = ("schedule", "condominium")
    search_fields = ("id", "title", "condominium__name", "schedule")
    verbose_name = _("Notification")
    verbose_name_plural = _("Notifications")
    inlines = [UserNotificationInline]


admin.site.register(Notification, NotificationAdmin)
