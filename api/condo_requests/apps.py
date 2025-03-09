from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CondoRequestsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "condo_requests"
    verbose_name = _("Requests")
