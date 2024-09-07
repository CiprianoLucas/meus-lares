from django.urls import path
from .views import (
    PlaceCreateView,
    PlaceDetailView,
    PlaceListForResidentsView,
    PlaceListForUnionsAndRepresentativesView,
    ResidentPlaceCreateView,
    ResidentPlaceRemoveView,
    UnionPlaceCreateView,
    UnionPlaceRemoveRemoveView,
)

urlpatterns = [
    path("", PlaceCreateView.as_view(), name="place-create"),
    path("<uuid:pk>/", PlaceDetailView.as_view(), name="place-detail"),
    path(
        "residents/", PlaceListForResidentsView.as_view(), name="place-list-residents"
    ),
    path(
        "unions/",
        PlaceListForUnionsAndRepresentativesView.as_view(),
        name="place-list-unions",
    ),
    path(
        "<uuid:pk_place>/residents/", ResidentPlaceCreateView.as_view(), name="resident"
    ),
    path(
        "<uuid:pk_place>/residents/<uuid:pk_user>",
        ResidentPlaceRemoveView.as_view(),
        name="resident",
    ),
    path("<uuid:pk>/unions/", UnionPlaceCreateView.as_view(), name="union"),
    path(
        "<uuid:pk_place>/unions/<uuid:pk_user>",
        UnionPlaceRemoveRemoveView.as_view(),
        name="union",
    ),
]
