from rest_framework.permissions import BasePermission

class IsRepresentative(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.place.representative == request.user
