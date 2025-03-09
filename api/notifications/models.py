from django.db import models
from django.utils.translation import gettext_lazy as _

from meus_lares.storages import PublicMediaStorage
from places.models import Condominium
from soft_components import SoftModel
from users.models import User


class Notification(SoftModel):
    title = models.CharField(_("title"), max_length=100)
    description = models.TextField(_("description"), null=True, blank=True)
    schedule = models.DateTimeField(_("schedule"), null=True, blank=True)
    url = models.URLField(_("url"), null=True, blank=True)
    condominium = models.ForeignKey(
        Condominium,
        verbose_name=_("condominium"),
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    image = models.ImageField(
        _("image"),
        upload_to="notifications/images/",
        blank=True,
        storage=PublicMediaStorage(),
    )

    def __str__(self):
        return self.title

    def temporary_url(self):
        return self.image.url if self.image else None

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")


class UserNotification(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.DO_NOTHING)
    notification = models.ForeignKey(
        Notification, verbose_name=_("notification"), on_delete=models.DO_NOTHING
    )
    confirmed_at = models.DateTimeField(_("confirmed at"), null=True, blank=True)

    class Meta:
        verbose_name = _("User notification")
        verbose_name_plural = _("User notifications")
        unique_together = ("user", "notification")
