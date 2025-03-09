from django.utils.timezone import localtime
from rest_framework import serializers

from soft_components.serializers import softModelSerializer

from .models import Notification, UserNotification


class NotificationSerializer(softModelSerializer):
    confirmed_at = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id",
            "title",
            "description",
            "schedule",
            "url",
            "image",
            "confirmed_at",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"write_only": True, "required": False},
        }

    def get_confirmed_at(self, obj: Notification):
        user_notification = UserNotification.objects.filter(notification=obj).first()
        return (
            localtime(user_notification.confirmed_at).isoformat()
            if getattr(user_notification, "confirmed_at")
            else None
        )
