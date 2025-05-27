import uuid

from django.db import models
from django.db.models.fields import UUIDField
from django.db.models.fields.files import FileField, ImageField
from django.db.models.fields.related import ForeignKey
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from enum import Enum

from .managers import SoftManager


class SoftChoices(str, Enum):

    @classmethod
    def choices(cls):
        choices = [(role.name.lower(), role.value) for role in list(cls)]
        return choices


class SoftModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_deleted = models.BooleanField(_("is deleted"), default=False, db_index=True)
    is_active = models.BooleanField(_("is active"), default=True, db_index=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    history = models.JSONField(_("history"), default=list, blank=True)
    tags = models.ManyToManyField("relations.Tag")
    objects = SoftManager()
    route: str = None

    class Meta:
        abstract = True

    @classmethod
    def filter_by_roles(cls, user, roles: list = ["owner"]):
        full_route = "condominium__condostaff__"
        if cls.route:
            full_route = cls.route + "__" + full_route

        user_route = full_route + "user"
        role_route = full_route + "role__in"

        filters = {user_route: user, role_route: roles}

        objects = cls.objects.filter(**filters)

        return objects

    def delete(self, *args, user=None, **kwargs):
        self.is_deleted = True
        self.is_active = False
        self.save(user=user)

    def save(self, *args, user=None, query_delete=False, **kwargs):
        if self.pk:
            old_instance = type(self).objects.filter(pk=self.pk).first()
            if old_instance:
                changes = {}
                for field in self._meta.fields:
                    field_name = field.name
                    old_value = getattr(old_instance, field_name)
                    new_value = getattr(self, field_name)

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
                super().save(*args, **kwargs)
                if type(self).objects.filter(pk=self.pk) and created_at is not None:
                    self.history.append(
                        {
                            "timestamp": now().isoformat(),
                            "user": str(user.id) if user else "system",
                            "changes": {"is_deleted": {"new": False, "old": True}},
                        }
                    )

        super().save(*args, **kwargs)
