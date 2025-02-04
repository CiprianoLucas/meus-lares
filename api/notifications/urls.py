from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import NotificationView, UserNotificationView

router = DefaultRouter()
router.register(r"main", NotificationView, "notifications")

urlpatterns = [
    path("confirm/", UserNotificationView.as_view(), name="confirm-notification"),
    path("", include(router.urls)),
]
