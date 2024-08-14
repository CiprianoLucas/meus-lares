from rest_framework.permissions import BasePermission

class IsGuardian(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.guardian == request.user

class IsRequester(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.requester == request.user
