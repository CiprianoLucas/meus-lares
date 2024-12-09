from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ApartmentTenantView, AptoTenanListView, CondoTenanListView

router = DefaultRouter()
router.register(
    r"tenant/condominium/list", CondoTenanListView, "tenant-condominium-list"
)
router.register(r"tenant/apartment/list", AptoTenanListView, "tenant-apartment-list")
router.register(r"tenant/apartment", ApartmentTenantView, "tenant-apartment")

urlpatterns = [path("", include(router.urls))]
