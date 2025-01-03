from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    NotificationView,
    UserNotificationView
)

router = DefaultRouter()
router.register(r"main", NotificationView, "notifications")
router.register(r"user", UserNotificationView, "notifications-user")

urlpatterns = [
    path("", include(router.urls))
]
