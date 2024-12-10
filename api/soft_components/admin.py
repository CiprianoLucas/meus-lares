from django.contrib import admin

from .models import SoftModel


class SoftInline(admin.TabularInline):
    extra = 0
    exclude = ("is_deleted", "history", "created_at")
    can_delete = False


class SoftAdmin(admin.ModelAdmin):
    exclude = []
    readonly_fields = ("created_at", "history")

    def save_model(self, request, obj: SoftModel, _, __):
        obj.save(user=request.user)

    def delete_queryset(self, request, queryset):
        queryset.delete(user=request.user)

    def delete_model(self, request, obj: SoftModel):
        obj.delete(user=request.user)

    def its_deleted(self, obj: SoftModel):
        if obj.is_deleted:
            return "DELETED"
        return ""

    its_deleted.short_description = "is deleted"

    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        if request.user.is_superuser:
            list_display.append("its_deleted")
        return list_display

    def get_list_filter(self, request):
        filters = list(super().get_list_filter(request))
        if request.user.is_superuser:
            filters.append("is_deleted")
        return filters

    def get_exclude(self, request, _):

        if request.user.is_superuser:
            return []

        self.exclude = list(self.exclude)
        self.exclude.append("is_deleted")
        self.readonly_fields = [
            item for item in self.readonly_fields if item not in self.exclude
        ]

        return self.exclude

    def get_readonly_fields(self, request, obj: SoftModel):

        if obj and obj.is_deleted:
            readonly = [column.name for column in obj._meta._get_fields()]
            readonly.remove("is_deleted")
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
