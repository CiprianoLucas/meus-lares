from django.db import models
from users.models import User
from places.models import Place
import uuid
        
class RelationInvoice(models.Model):
    STATUS_CHOICES = {'CELESC': 'CELESC'}
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resident = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relation_invoices')
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    company = models.CharField(max_length=50, choices=STATUS_CHOICES)
    unit_number = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Relação de fatura"
        verbose_name_plural = "Relações de faturas"
    
class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    relation = models.ForeignKey(RelationInvoice, on_delete=models.CASCADE)
    value = models.FloatField()
    ticket_number = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fatura"
        verbose_name_plural = "Faturas"