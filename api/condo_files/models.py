from django.db import models
from meus_lares.mixin import SoftModel
from relations.models import Contract
from meus_lares.storages import PrivateMediaStorage, validate_file

class ContractFiles(SoftModel):
    constract = models.ForeignKey(Contract, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to='relations/contracts/', validators=[validate_file], storage=PrivateMediaStorage())
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Arquivo de contrato"
        verbose_name_plural = "Arquivos de contratos"