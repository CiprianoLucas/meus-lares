from rest_framework.permissions import BasePermission

from relations.models import CondoTenant

from .models import Apartment, Condominium


class CondominiumOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Condominium):
            return obj.condostaff_set.filter(user=request.user, role="owner").exists()
        elif isinstance(obj, Apartment):
            return obj.condominium.condostaff_set.filter(
                user=request.user, role="owner"
            ).exists()
        elif isinstance(obj, CondoTenant):
            return obj.apartment.condominium.condostaff_set.filter(
                user=request.user, role="owner"
            ).exists()

        return False

    def has_permission(self, request, view):

        if view.basename == "condominium":
            return True

        elif view.basename == "apartment":

            if view.action in ["list", "retrieve"]:
                return True
            elif view.action in ["create", "update"] and not request.data:
                return True
            elif view.action in ["create", "update"] and request.data:
                condominium_id = request.data["condominium"]
                condominium = Condominium.objects.get(id=condominium_id)
                if condominium.condostaff_set.filter(
                    user=request.user, role="owner"
                ).exists():
                    return True

        elif view.basename == "tenant-apartment":
            if view.action in ["list", "retrieve"]:
                return True
            elif view.action in ["create", "update"] and not request.data:
                return True
            elif view.action in ["create", "update"] and request.data:
                apartment_id = request.data["apartment"]
                apartment = Apartment.objects.get(id=apartment_id)
                if apartment.condominium.condostaff_set.filter(
                    user=request.user, role="owner"
                ).exists():
                    return True

        return False
