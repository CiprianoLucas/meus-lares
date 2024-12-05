from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("cpf", "phone_number", "full_name", "profile_photo")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
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

    def delete_queryset(self, request, queryset):
        return


admin.site.register(User, UserAdmin)
