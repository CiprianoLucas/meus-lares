from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ApartmentView,
    CondominiumView,
    FullAddressView,
    CitiesView,
    # CondominiumListForResidentsView,
    # CondominiumListForUnionsAndRepresentativesView,
    # ResidentCondominiumCreateView,
    # ResidentCondominiumRemoveView,
    # UnionCondominiumCreateView,
    # UnionCondominiumRemoveRemoveView,
)

router = DefaultRouter()
router.register(r"condominium", CondominiumView)
router.register(r"apartment", ApartmentView)

urlpatterns = [
    path("owner/", include(router.urls)),
    # path("<uuid:pk>/", CondominiumDetailView.as_view(), name="condominium-detail"),
    # path(
    #     "residents/",
    #     CondominiumListForResidentsView.as_view(),
    #     name="condominium-list-residents",
    # ),
    # path(
    #     "unions/",
    #     CondominiumListForUnionsAndRepresentativesView.as_view(),
    #     name="condominium-list-unions",
    # ),
    # path(
    #     "<uuid:pk_condominium>/residents/",
    #     ResidentCondominiumCreateView.as_view(),
    #     name="resident",
    # ),
    # path(
    #     "<uuid:pk_condominium>/residents/<uuid:pk_user>",
    #     ResidentCondominiumRemoveView.as_view(),
    #     name="resident",
    # ),
    # path("<uuid:pk>/unions/", UnionCondominiumCreateView.as_view(), name="union"),
    # path(
    #     "<uuid:pk_condominium>/unions/<uuid:pk_user>",
    #     UnionCondominiumRemoveRemoveView.as_view(),
    #     name="union",
    # ),
    path("cities/<str:uf>", CitiesView.as_view(), name="cities"),
    path("cep/<str:cep>", FullAddressView.as_view(), name="full-address-by-cep"),
]
