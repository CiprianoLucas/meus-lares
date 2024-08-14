from django.contrib import admin
from .models import Users

class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'cpf', 'phone_number', 'full_name')
    list_filter = ('user__is_active', 'user__is_staff')
    search_fields = ('user__username', 'cpf', 'full_name', 'user__email')
    fields = ('user', 'cpf', 'phone_number', 'full_name')
    list_per_page = 20
    verbose_name = "Usuário"
    verbose_name_plural = "Usuários"

admin.site.register(Users, UserAdmin)