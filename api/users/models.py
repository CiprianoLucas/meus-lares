import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import UUIDField
from django.db.models.fields.files import FileField, ImageField
from django.db.models.fields.related import ForeignKey
from django.utils.timezone import now
from rest_framework import serializers
from PIL import Image
from io import BytesIO
from django.core.files import File

from meus_lares.storages import PrivateMediaStorage, PublicMediaStorage
from soft_components.managers import SoftUserManager

def unique_email(value, id):
    if User.objects.filter(email=value).exclude(id=id).exists():
        raise serializers.ValidationError({"error": "email is already in use"})
    
def validate_all_params(user):
    unique_email(user.email, user.id)
        

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cpf = models.CharField(max_length=11)
    nick = models.CharField(
        max_length=25,
    )
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    full_name = models.CharField(max_length=255)
    birth = models.DateField()
    profile_photo = models.ImageField(
        upload_to="users/profile_photo/",
        blank=True,
        null=True,
        storage=PublicMediaStorage(),
    )
    identity_photo = models.ImageField(
        upload_to="users/identity_photo/",
        blank=True,
        null=True,
        storage=PrivateMediaStorage(),
    )
    document_photo = models.ImageField(
        upload_to="users/document_photo/",
        blank=True,
        null=True,
        storage=PrivateMediaStorage(),
    )
    is_deleted = models.BooleanField(default=False)
    history = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = SoftUserManager()
    
    def clean(self):
        unique_email(self.email, self.id)
        
    def save_history(self, *args, user=None, query_delete=False, **kwargs):
        if self.pk:
            old_instance = type(self).objects.filter(pk=self.pk).first()
            if old_instance:
                changes = {}
                for field in self._meta.fields:
                    field_name = field.name
                    if field_name in ['last_login', 'date_joined']:
                        continue
                    
                    old_value = getattr(old_instance, field_name)
                    new_value = getattr(self, field_name)
                    
                    if isinstance(field, models.DateField):
                        old_value = str(old_value) if old_value else None
                        new_value = str(new_value) if new_value else None

                    if isinstance(field, ForeignKey):
                        old_value = str(old_value.pk) if old_value else None
                        new_value = str(new_value.pk) if new_value else None

                    if isinstance(field, UUIDField):
                        old_value = str(old_value) if old_value else None
                        new_value = str(new_value) if new_value else None

                    if isinstance(field, (ImageField, FileField)):
                        old_value = old_value.url if old_value else None
                        new_value = new_value.url if new_value else None

                    if old_value != new_value:
                        changes[field_name] = {
                            "old": old_value,
                            "new": new_value,
                        }

                if changes:
                    if "history" in changes:
                        if user.is_superuser or query_delete:
                            super().save(*args, **kwargs)
                        return

                    self.history.append(
                        {
                            "timestamp": now().isoformat(),
                            "user": str(user.id) if user else "system",
                            "changes": changes,
                        }
                    )
            else:
                created_at = self.created_at
                validate_all_params(self)
                super().save(*args, **kwargs)
                if type(self).objects.filter(pk=self.pk) and created_at is not None:
                    self.history.append(
                        {
                            "timestamp": now().isoformat(),
                            "user": str(user.id) if user else "system",
                            "changes": {"is_deleted": {"new": False, "old": True}},
                        }
                    )
    
    def sizeImgs(self, *args, **kwargs):
        if self.profile_photo:
            img = Image.open(self.profile_photo)
            
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            max_size = 400
            width, height = img.size

            if width > height:
                new_width = max_size
                new_height = int((new_width / width) * height)
            else:
                new_height = max_size
                new_width = int((new_height / height) * width)

            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            image_io = BytesIO()
            img.save(image_io, format='JPEG')
            image_io.seek(0)
            
            self.profile_photo.save(self.profile_photo.name, File(image_io), save=False)

    def save(self, *args, user=None, query_delete=False, **kwargs):
        self.sizeImgs(self, *args, **kwargs)
        self.save_history(self, *args, user=user, query_delete=query_delete, **kwargs)
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def delete(self, *args, user=None, **kwargs):
        self.is_deleted = True
        self.save(user=user)
