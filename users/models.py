from django.db import models
from django.contrib.auth.models import User as UserDjango

class Users(models.Model):
    user = models.OneToOneField(UserDjango, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    full_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"