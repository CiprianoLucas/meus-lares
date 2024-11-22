from django.db import models
from soft_components import SoftModel
from relations.models import Contract, CondoTenant
from meus_lares.storages import PrivateMediaStorage, validate_file

class ContractFiles(SoftModel):
    constract = models.ForeignKey(Contract, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to='relations/contracts/files', validators=[validate_file], storage=PrivateMediaStorage())
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Arquivo de contrato"
        verbose_name_plural = "Arquivos de contratos"
        
        
class AptInspectImages(SoftModel):
    ROLE_CHOICES = [
        ('in', 'In'),
        ('out', 'Out'),
        ('inspect', 'Inspect')
    ]
    
    tenant = models.ForeignKey(CondoTenant, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='relations/tenant/images', storage=PrivateMediaStorage())
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        verbose_name = "Imagem de Inspeção de Apartamento"
        verbose_name_plural = "Imagens de Inspeção de Apartamentos"