from django.db import models
from soft_components import SoftModel
from users.models import User
from meus_lares.storages import PublicMediaStorage
from places.models import Condominium

class Notification(SoftModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    schedule = models.DateTimeField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    condominium = models.ForeignKey(Condominium, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    image = models.ImageField(
        upload_to="notifications/images/", blank=True, storage=PublicMediaStorage()
    )

    def __str__(self):
        return self.title

    def temporary_url(self):
        return self.image.url if self.image else None

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        
class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    notification = models.ForeignKey(Notification, on_delete=models.DO_NOTHING)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Notificação do usuário"
        verbose_name_plural = "Notificações dos usuários"