from rest_framework.permissions import IsAuthenticated
from soft_components.views import SoftModelsViewSet
from django.db.models import Q
from .models import CondoRequest
from .serializers import CondoRequestSerializer


class NotificationView(SoftModelsViewSet):
    serializer_class = CondoRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        requests = CondoRequest.objects.filter(
            Q(condominium__condostaff__user=user, condominium__condostaff__role_in=["owner"]) |
            Q(apartment__condotenant__user=user) |
            Q(requester=user) |
            Q(guardian=user)
        ).distinct()

        return requests