from django.db import models
from users.models import User
from meus_lares.storages import PrivateMediaStorage, PublicMediaStorage
import uuid

class State(models.Model):
    name = models.CharField(max_length=50, unique=True)
    acronym = models.CharField(max_length=2, unique=True)
    
    def __str__(self):
        return f'{self.name} ({self.acronym})'
    
class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Place(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    representative = models.ForeignKey(User, on_delete=models.CASCADE, related_name='place_representative')
    residents = models.ManyToManyField(User, related_name='place_residents', blank=True)
    unions = models.ManyToManyField(User, related_name='place_unions', blank=True)
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=20, null=True)
    street = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_photo = models.ImageField(upload_to='places/profile-photo/', blank=True, storage=PrivateMediaStorage())

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locais"
    
    def delete(self, *args, **kwargs):
        if self.profile_photo:
            self.profile_photo.delete(save=False)

        super().delete(*args, **kwargs)
        
