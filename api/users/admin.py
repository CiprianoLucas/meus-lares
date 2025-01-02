from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UD

from soft_components.admin import SoftAdmin

from .models import User


class UserAdmin(UD, SoftAdmin):
    fieldsets = UD.fieldsets + (
        (
            None,
            {
                "fields": (
                    "cpf",
                    "phone_number",
                    "full_name",
                    "profile_photo",
                    "history",
                )
            },
        ),
    )
    backup_fieldsets = UD.fieldsets + (
        (
            None,
            {
                "fields": (
                    "cpf",
                    "phone_number",
                    "full_name",
                    "profile_photo",
                    "history",
                    "is_deleted",
                )
            },
        ),
    )
    readonly_fields = ("history",)
    add_fieldsets = UD.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "email",
                    "cpf",
                    "phone_number",
                    "full_name",
                    "profile_photo",
                    "birth",
                )
            },
        ),
    )
    list_display = (
        "id",
        "username",
        "email",
        "cpf",
        "full_name",
        "phone_number",
        "is_staff",
    )
    search_fields = ("username", "email", "cpf", "full_name", "phone_number")

    def delete_model(self, request, obj):
        return SoftAdmin.delete_model(self, request, obj)

    def get_list_display(self, request):
        return SoftAdmin.get_list_display(self, request)

    def get_list_filter(self, request):
        return SoftAdmin.get_list_filter(self, request)

    def get_fieldsets(self, request, _):
        if request.user.is_superuser:
            return self.backup_fieldsets
        return self.fieldsets

    def get_readonly_fields(self, request, obj):
        return SoftAdmin.get_readonly_fields(self, request, obj)

    def save_model(self, request, obj, _, __):
        return SoftAdmin.save_model(self, request, obj, _, __)

    def delete_queryset(self, _, __):
        return SoftAdmin.delete_queryset(self, _, __)


admin.site.register(User, UserAdmin)
