from django.urls import path
from .views import PlaceCreateView, PlaceDetailView, PlaceListForResidentsView, PlaceListForUnionsAndRepresentativesView

urlpatterns = [
    path('', PlaceCreateView.as_view(), name='place-create'),
    path('<int:pk>/', PlaceDetailView.as_view(), name='place-detail'),
    path('residents/', PlaceListForResidentsView.as_view(), name='place-list-residents'),
    path('unions/', PlaceListForUnionsAndRepresentativesView.as_view(), name='place-list-unions'),
]
