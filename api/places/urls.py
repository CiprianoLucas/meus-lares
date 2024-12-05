from django.urls import path

from .views import (
    CitiesView,
    CondominiumCreateView,
    CondominiumDetailView,
    CondominiumListForResidentsView,
    CondominiumListForUnionsAndRepresentativesView,
    FullAddressView,
    ResidentCondominiumCreateView,
    ResidentCondominiumRemoveView,
    UnionCondominiumCreateView,
    UnionCondominiumRemoveRemoveView,
)

urlpatterns = [
    path("", CondominiumCreateView.as_view(), name="condominium-create"),
    path("<uuid:pk>/", CondominiumDetailView.as_view(), name="condominium-detail"),
    path(
        "residents/",
        CondominiumListForResidentsView.as_view(),
        name="condominium-list-residents",
    ),
    path(
        "unions/",
        CondominiumListForUnionsAndRepresentativesView.as_view(),
        name="condominium-list-unions",
    ),
    path(
        "<uuid:pk_condominium>/residents/",
        ResidentCondominiumCreateView.as_view(),
        name="resident",
    ),
    path(
        "<uuid:pk_condominium>/residents/<uuid:pk_user>",
        ResidentCondominiumRemoveView.as_view(),
        name="resident",
    ),
    path("<uuid:pk>/unions/", UnionCondominiumCreateView.as_view(), name="union"),
    path(
        "<uuid:pk_condominium>/unions/<uuid:pk_user>",
        UnionCondominiumRemoveRemoveView.as_view(),
        name="union",
    ),
    path("cities/<str:uf>", CitiesView.as_view(), name="cities"),
    path("cep/<str:cep>", FullAddressView.as_view(), name="full-address-by-cep"),
]
