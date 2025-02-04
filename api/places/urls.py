from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ApartmentByCondominiumView, ApartmentOwnerView,
                    BulkApartmentCreateView, BulkParkCreateView,
                    BulkSharedPlaceCreateView, CitiesView,
                    CondominiumOwnerView, FullAddressView, ParkingView,
                    SharedPlacesView)

router = DefaultRouter()
router.register(r"condominium", CondominiumOwnerView, "condominium")
router.register(r"apartment", ApartmentOwnerView, "apartment")
router.register(r"park", ParkingView, "parking")
router.register(r"shared", SharedPlacesView, "shared")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "apartments/bulk-create/",
        BulkApartmentCreateView.as_view(),
        name="bulk-apartment-create",
    ),
    path(
        "parks/bulk-create/", BulkParkCreateView.as_view(), name="bulk-apartment-create"
    ),
    path(
        "shareds/bulk-create/",
        BulkSharedPlaceCreateView.as_view(),
        name="bulk-apartment-create",
    ),
    path(
        "apartments-all/<uuid:condominium_id>",
        ApartmentByCondominiumView.as_view(),
        name="apartments-by-condominium",
    ),
    path("cities/<str:uf>", CitiesView.as_view(), name="cities"),
    path("cep/<str:cep>", FullAddressView.as_view(), name="full-address-by-cep"),
]
