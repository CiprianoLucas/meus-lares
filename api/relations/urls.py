from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AptoListView, CondoListView, CondoStaffView, CondoTenantView

router = DefaultRouter()
router.register(r"condominium/list", CondoListView, "tenant-condominium-list")
router.register(r"apartment/list", AptoListView, "tenant-apartment-list")
router.register(r"tenant", CondoTenantView, "tenant")
router.register(r"staff", CondoStaffView, "staff")

urlpatterns = [path("", include(router.urls))]
