from django.db import models
from places.models import Apartment, Condominium
from users.models import User
import uuid

class CondoTenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    apartment = models.ForeignKey(Apartment, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_renter = models.BooleanField(default=False)
    is_responsible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    start_day = models.DateField(blank=True, null=True)
    end_day = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

class CondoManager(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    condominium = models.ForeignKey(Condominium, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    start_day = models.DateField(blank=True, null=True)
    end_day = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

class CondoOwner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    condominium = models.ForeignKey(Condominium, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=False)
    is_responsible = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    start_day = models.DateField(blank=True, null=True)
    end_day = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)