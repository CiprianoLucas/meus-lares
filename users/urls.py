from django.urls import path
from .views import UserCreateView, LoginView, logout_view, get_info

urlpatterns = [
    path('info/', get_info, name='csrf'),
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', logout_view, name='logout'),
]
