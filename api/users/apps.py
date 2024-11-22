from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from datetime import datetime


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = "usuários"
    
    def ready(self):
        post_migrate.connect(create_super_user_if_not_exists, sender=self)

def create_super_user_if_not_exists(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@admin.com',
            password='admin',
            cpf='12345678900',
            phone_number='47987654321',
            full_name='Admin Manager',
            birth = datetime.now()
        )
        print('Create superuser. username: admin, password: admin')