from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ApartmentOwnerView,
    CitiesView,
    CondominiumOwnerView,
    FullAddressView,
)

router = DefaultRouter()
router.register(r"condominium", CondominiumOwnerView, "condominium")
router.register(r"apartment", ApartmentOwnerView, "apartment")

urlpatterns = [
    path("", include(router.urls)),
    path("cities/<str:uf>", CitiesView.as_view(), name="cities"),
    path("cep/<str:cep>", FullAddressView.as_view(), name="full-address-by-cep"),
]
