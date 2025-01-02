from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecurringFeeView, BreachPenaltyView, calculate_penality

router = DefaultRouter()
router.register(r"recurring", RecurringFeeView, "bills-recurring-fee")
router.register(r"penalty", BreachPenaltyView, "bills-penalty")

urlpatterns = [
    path("", include(router.urls)),
    path("calculate-penality", calculate_penality, name="calculate-penality"),
    ]
