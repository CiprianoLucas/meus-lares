from django.db import models
from users.models import User
import uuid
class Places(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    representative = models.ForeignKey(User, on_delete=models.CASCADE, related_name='place_representative')
    residents = models.ManyToManyField(User, related_name='place_residents', blank=True)
    unions = models.ManyToManyField(User, related_name='place_unions', blank=True)
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=20, null=True)
    street = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locais"