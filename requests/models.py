from django.db import models
import uuid
from users.models import User
from places.models import Places

class Request(models.Model):
    TYPE_CHOICES = [
        ('R', 'RECLAMAÇÃO'),
        ('M', 'MANUTENÇÃO'),
        ('O', 'OUTROS'),
    ]
    STATUS_CHOICES = [
        ('A', 'ANDAMENTO'),
        ('C', 'CONCLUIDO'),
        ('P', 'PENDENTE'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requester = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank = True ,related_name='request_requester')
    guardian = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank = True, related_name='request_guardian')
    place = models.ForeignKey(Places, on_delete=models.CASCADE, related_name='request_place')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=20)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='O')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Requisição"
        verbose_name_plural = "Requisições"
        
class Images(models.Model):
    
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='requests')
    
    def __str__(self):
        return f"Image for {self.request.title}"