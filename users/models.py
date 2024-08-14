from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"