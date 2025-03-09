from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class BillsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bills"
    verbose_name = _("Installments and Fines")
