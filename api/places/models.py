from django.db import models
from users.models import User
from meus_lares.storages import PrivateMediaStorage, PublicMediaStorage
import uuid

class State(models.Model):
    acronym = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f'{self.name} ({self.acronym})'
    
class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE, to_field='acronym')
    
    def __str__(self):
        return self.name

class Condominium(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    cep = models.CharField(max_length=8)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, related_name='place_city')
    neighborhood = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=20, null=True)
    complement = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='places/profile-photo/', blank=True, storage=PublicMediaStorage())

    def __str__(self):
        return self.name
    
    def temporary_url(self):
        return self.profile_photo.url if self.profile_photo else None

    class Meta:
        verbose_name = "Condomínio"
        verbose_name_plural = "Condomínios"
    
    def delete(self, *args, **kwargs):
        if self.profile_photo:
            self.profile_photo.delete(save=False)

        super().delete(*args, **kwargs)
        

class Apartment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    condominium = models.ForeignKey(Condominium, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_photo = models.ImageField(upload_to='places/profile-photo/', blank=True, storage=PublicMediaStorage())
    complement = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = "Apartamento"
        verbose_name_plural = "Apartamentos"