from django.urls import path
from .views import RequestCreateView, RequestDetailView, RequestListForResidentsView, RequestListForUnionsAndRepresentativesView

urlpatterns = [
    path('', RequestCreateView.as_view(), name='request-create'),
    path("<uuid:pk>/", RequestDetailView.as_view(), name="request-detail"),
    path(
        "residents/", RequestListForResidentsView.as_view(), name="request-list-residents"
    ),
    path(
        "guardians/",
        RequestListForUnionsAndRepresentativesView.as_view(),
        name="request-list-unions",
    ),
]
