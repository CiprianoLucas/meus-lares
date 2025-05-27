from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from .models import SoftModel


class SoftModelsPermission(BasePermission):
    def has_object_permission(self, request: Request, view, obj: SoftModel):
        return obj.tags.filter(
            condominium__name="Soares"
        ).exists()
