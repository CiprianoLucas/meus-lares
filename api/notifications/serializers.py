from rest_framework import serializers
from soft_components.serializers import softModelSerializer

from .models import Notification, UserNotification
from users.models import User
from places.models import Condominium
from datetime import datetime

class NotificationSerializer(softModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Notification
        fields = [
            "id",
            "title",
            "description",
            "schedule",
            "url",
            "condominium",
            "image",
            "user"
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"write_only": True, "required": False},
        }
        
    def create(self, data):
        user = data.pop("user", None)
        notification: Notification = super().create(data)

        if user:
            user_notification = UserNotification(user=user, notification=notification)
            user_notification.save()
        elif notification.condominium:
            users = Condominium.objects.filter(apartment__condotenant__user=notification.condominium)
            notifications_obj = [UserNotification(user=u, notification=notification) for u in users]
            UserNotification.objects.bulk_create(notifications_obj)

        return notification

class UserNotificationSerializer(softModelSerializer):
    
    class Meta:
        model = UserNotification
        fields = [
            "user",
            "notification",
            "confirmed_at"
        ]
        extra_kwargs = {
            "user": {"read_only": True},
            "notification": {"read_only": True},
            "confirmed_at": {"read_only": True},
        }
        
    def update(self, instance: UserNotification, validated_data):
        user = self.context["request"].user

        if user != instance.user:
            raise serializers.ValidationError({"notification": "Notificação não pertence ao usuário."})

        instance.confirmed_at = datetime.now()
        instance.save()
        return instance
