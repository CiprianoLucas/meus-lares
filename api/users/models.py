from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    profile_photo = models.ImageField(upload_to='users/profile_photo/', blank=True)
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        
    def delete(self, *args, **kwargs):
        if self.profile_photo:
            self.profile_photo.delete(save=False)

        super().delete(*args, **kwargs)