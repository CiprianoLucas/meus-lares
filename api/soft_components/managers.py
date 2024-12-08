from django.db import models
from django.utils.timezone import now


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self, user=None):
        for obj in self:
            if hasattr(obj, "history") and isinstance(obj.history, list):
                obj.history.append(
                    {
                        "timestamp": now().isoformat(),
                        "user": user.username if user else "system",
                        "changes": {"is_deleted": {"old": False, "new": True}},
                    }
                )
                obj.save(update_fields=["history"], user=user, query_delete=True)

        return self.update(is_deleted=True)

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)


class SoftManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()

    def get_all_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).all()
