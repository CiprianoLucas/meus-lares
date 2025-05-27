from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView
from django.db.models import Prefetch
from soft_components.views import SoftModelsViewSet

from .models import Notification, UserNotification
from .serializers import NotificationSerializer


class NotificationView(SoftModelsViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get_queryset(self):
        user = self.request.user
        now = timezone.now()
        user_notification = UserNotification.objects.filter(user=user)

        notifications = Notification.objects.filter(
            Q(schedule__lt=now)
            & (
                (
                    Q(usernotification__only_confirm=False)
                    & Q(usernotification__user=user)
                )
                | (
                    Q(usernotification__isnull=True)
                    & Q(condominium__apartment__condotenant__user=user)
                )
            )
        ).prefetch_related(
            Prefetch(
                "usernotification_set",
                queryset=user_notification,
                to_attr="user_notification",
            )
        )

        return notifications


class UserNotificationView(APIView):

    def post(self, request: Request, *args, **kwargs):

        user = request.user
        notification = Notification.objects.get(id=request.data["id"])
        now = datetime.now()

        user_notification = UserNotification.objects.filter(
            user=user, notification=notification
        ).first()

        if not user_notification:
            user_notification = UserNotification(user=user, notification=notification)

        user_notification.confirmed_at = now
        user_notification.save()

        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
