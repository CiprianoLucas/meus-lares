from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CondoFilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "condo_files"
    verbose_name = _("Files")
