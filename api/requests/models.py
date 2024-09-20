from django.db import models
import uuid
from users.models import User
from places.models import Place

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
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='request_place')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=3000)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='O')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Requisição"
        verbose_name_plural = "Requisições"
        
class RequestFiles:
    file = models.FileField(upload_to='requests/files/')
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Arquivo da requisição"
        verbose_name_plural = "Arquivos das requisições"
        
    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super().delete(*args, **kwargs)