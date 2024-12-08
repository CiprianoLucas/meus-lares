from rest_framework.permissions import BasePermission

from .models import Apartment, Condominium


class CondominiumOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Condominium):
            return obj.condostaff_set.filter(user=request.user, role="owner").exists()
        elif isinstance(obj, Apartment):
            return obj.condominium.condostaff_set.filter(
                user=request.user, role="owner"
            ).exists()

        return False

    def has_permission(self, request, view):

        if view.basename == "condominium":
            return True

        elif view.basename == "apartment":

            if view.action in ["list"]:
                return True
            elif view.action in ["create"] and not request.data:
                return True
            elif view.action in ["create"] and request.data:
                condominium_id = request.data["condominium"]
                condominium = Condominium.objects.get(id=condominium_id)
                if condominium.condostaff_set.filter(
                    user=request.user, role="owner"
                ).exists():
                    return True

        return False
