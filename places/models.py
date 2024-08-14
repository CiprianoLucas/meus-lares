from django.db import models
from users.models import Users

class Places(models.Model):
    
    representative = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='place_representative')
    residents = models.ManyToManyField(Users, related_name='place_residents')
    unions = models.ManyToManyField(Users, related_name='place_unions')
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locais"