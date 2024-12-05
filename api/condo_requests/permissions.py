from rest_framework.permissions import BasePermission


class IsRequester(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.requester == request.user


class IsPendent(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user in obj.place.unions.all()
            or request.user == obj.place.representative
        )
