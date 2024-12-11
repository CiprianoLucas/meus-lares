from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AptoListView,
    CondoListView,
    CondoStaffView,
    CondoTenantView,
    ContractStaffView,
    ContractTenantView,
)

router = DefaultRouter()
router.register(r"condominium/list", CondoListView, "tenant-condominium-list")
router.register(r"apartment/list", AptoListView, "tenant-apartment-list")
router.register(r"tenant", CondoTenantView, "tenant")
router.register(r"staff", CondoStaffView, "staff")
router.register(r"contract/tenant", ContractTenantView, "contract-tenant")
router.register(r"contract/staff", ContractStaffView, "contract-staff")

urlpatterns = [path("", include(router.urls))]
