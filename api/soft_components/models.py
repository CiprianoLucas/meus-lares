import uuid

from django.db import models
from django.db.models.fields import UUIDField
from django.db.models.fields.files import FileField, ImageField
from django.db.models.fields.related import ForeignKey
from django.utils.timezone import now

from users.models import User

from .managers import SoftManager


class SoftModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    history = models.JSONField(default=list, blank=True)
    objects = SoftManager()

    class Meta:
        abstract = True

    def delete(self, *args, user=None, **kwargs):
        self.is_deleted = True
        self.save(user=user)

    def save(self, *args, user: User = None, query_delete=False, **kwargs):
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
                            "user": user.username if user else "system",
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
                            "user": user.username if user else "system",
                            "changes": {"is_deleted": {"new": False, "old": True}},
                        }
                    )

        super().save(*args, **kwargs)
