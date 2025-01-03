from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from soft_components.views import SoftModelsViewSet
from django.db.models import Q
from .models import Notification, UserNotification
from .serializers import NotificationSerializer, UserNotificationSerializer


class NotificationView(SoftModelsViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        notifications = Notification.objects.filter(
            Q(condominium__condostaff__user=user, condominium__condostaff__role="owner")
            | Q(usernotification__user=user)
        ).distinct()

        return notifications
    
class UserNotificationView(viewsets.ModelViewSet):
    serializer_class = UserNotificationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put"]

    def get_queryset(self):
        user = self.request.user
        notifications = UserNotification.objects.filter(Q(
            notification__condominium__condostaff__user=user, 
            notification__condominium__condostaff__role="owner")|
            Q(user=user)
        ).distinct()

        return notifications