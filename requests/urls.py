from django.urls import path
from .views import RequestCreateView, RequestDetailView, RequestListForRequesterView, RequestListForGuardianView

urlpatterns = [
    path('', RequestCreateView.as_view(), name='request-create'),
    path('<int:pk>/', RequestDetailView.as_view(), name='request-detail'),
    path('requester/', RequestListForRequesterView.as_view(), name='request-list-requester'),
    path('guardian/', RequestListForGuardianView.as_view(), name='request-list-guardian'),
]
