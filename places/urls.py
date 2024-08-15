from django.urls import path
from .views import (
    PlaceCreateView,
    PlaceDetailView,
    PlaceListForResidentsView,
    PlaceListForUnionsAndRepresentativesView,
    ResidentPlaceView,
    UnionPlaceView,
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
    path("<uuid:pk>/resident/", ResidentPlaceView.as_view(), name="add-resident"),
    path("<uuid:pk>/union/", UnionPlaceView.as_view(), name="add-union"),
]
