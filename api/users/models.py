import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import UUIDField
from django.db.models.fields.files import FileField, ImageField
from django.db.models.fields.related import ForeignKey
from django.utils.timezone import now
from rest_framework import serializers

from meus_lares.storages import PrivateMediaStorage, PublicMediaStorage
from soft_components.managers import SoftUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError

username_validator = UnicodeUsernameValidator()
def unique_cpf(value, id):
    if User.objects.filter(cpf=value).exclude(id=id).exists():
        raise serializers.ValidationError("cpf is already in use")

def unique_username(value, id):
    if User.objects.filter(username=value).exclude(id=id).exists():
        raise serializers.ValidationError("username is already in use")

def unique_email(value, id):
    if User.objects.filter(email=value).exclude(id=id).exists():
        raise serializers.ValidationError("email is already in use")
    
def validate_all_params(user):
    unique_cpf(user.cpf, user.id)
    unique_username(user.username, user.id)
    unique_email(user.email, user.id)
        

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cpf = models.CharField(max_length=11)
    username = models.CharField(
        max_length=25,
        validators=[username_validator],
    )
    email = models.EmailField(blank=True)
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
        unique_cpf(self.cpf, self.id)
        unique_username(self.username, self.id)
        unique_email(self.email, self.id)

    def save(self, *args, user=None, query_delete=False, **kwargs):
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
                            "user": user.username if user else "system",
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
                            "user": user.username if user else "system",
                            "changes": {"is_deleted": {"new": False, "old": True}},
                        }
                    )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def delete(self, *args, user=None, **kwargs):
        self.is_deleted = True
        self.save(user=user)
