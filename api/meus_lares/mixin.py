from django.db import models
from django.db.models.fields.related import ForeignKey
from django.core.exceptions import PermissionDenied
from django.db.models.fields.files import ImageField
from django.utils.timezone import now
import uuid
from django.contrib import admin


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self, user=None):
        for obj in self:
            if hasattr(obj, 'history') and isinstance(obj.history, list):
                obj.history.append({
                    "timestamp": now().isoformat(),
                    "user": user.username if user else "system",
                    "changes": {"is_deleted": {"old": False, "new": True}},
                })
                obj.save(update_fields=['history'])
                
        return self.update(is_deleted=True)

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)
    
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()
    
    def get_all_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).all()

class SoftModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    history = models.JSONField(default=list, blank=True)
    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = now()
        self.save()

    def save(self, *args, user=None, **kwargs):
        if self.pk:
            old_instance = type(self).objects.filter(pk=self.pk).first()
            if old_instance:
                changes = {}
                for field in self._meta.fields:
                    field_name = field.name
                    old_value = getattr(old_instance, field_name)
                    new_value = getattr(self, field_name)

                    if isinstance(field, ForeignKey):
                        old_value = old_value.pk if old_value else None
                        new_value = new_value.pk if new_value else None

                    if isinstance(field, ImageField):
                        old_value = old_value.url if old_value else None
                        new_value = new_value.url if new_value else None

            
                    if old_value != new_value:
                        changes[field_name] = {
                            "old": old_value,
                            "new": new_value,
                        }

                if changes:
                    if "history" in changes:
                        if user.is_superuser:
                            super().save(*args, **kwargs)
                        return

                    self.history.append({
                        "timestamp": now().isoformat(),
                        "user": user.username if user else "system",
                        "changes": changes,
                    })
            else:
                created_at = self.created_at
                super().save(*args, **kwargs)
                if type(self).objects.filter(pk=self.pk) and created_at is not None:
                    self.history.append({
                        "timestamp": now().isoformat(),
                        "user": user.username if user else "system",
                        "changes": {"is_deleted": {"new": False, "old": True}},
                    })

        super().save(*args, **kwargs)


    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


class SoftInline(admin.TabularInline):
    extra = 0
    exclude = ('is_deleted', 'history', 'created_at')
    can_delete = False

class SoftAdmin(admin.ModelAdmin):
    exclude = []
    readonly_fields = ('created_at','history')

    def save_model(self, request, obj, form, change):
        obj.save(user=request.user)

    def delete_queryset(self, request, queryset):
        queryset.delete(user=request.user)
    
    def its_deleted(self, obj):
        if obj.is_deleted:
            return "DELETED"
        return ""
    its_deleted.short_description = "is deleted"

    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        if request.user.is_superuser:
            list_display.append('its_deleted')
        return list_display
        
    def get_list_filter(self, request):
        filters = list(super().get_list_filter(request))
        if request.user.is_superuser:
            filters.append('is_deleted')
        return filters

    def get_exclude(self, request, _):

        if request.user.is_superuser:
            return []

        self.exclude = list(self.exclude)
        self.exclude.append('is_deleted')
        self.readonly_fields = [item for item in self.readonly_fields if item not in self.exclude]
        
        return self.exclude
    
    def get_readonly_fields(self, request, obj):

        if obj and obj.is_deleted:
            readonly = [column.name for column in obj._meta._get_fields()]
            readonly.remove('is_deleted')
            return readonly

        if request.user.is_superuser:
            return []
        return self.readonly_fields

    def get_queryset(self, request):
        qs = self.model._default_manager.get_all_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(is_deleted=False)