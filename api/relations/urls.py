from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CondoTenantContractView,
    CondoTenantView,
    PlaceReservationViewSet,
)

router = DefaultRouter()
router.register(r"tenant", CondoTenantView, "tenant")
router.register(r"contract/tenant", CondoTenantContractView, "contract-tenant")
router.register(r"reservate", PlaceReservationViewSet, "reservate")

urlpatterns = [path("", include(router.urls))]
