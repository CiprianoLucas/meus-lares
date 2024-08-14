from django.contrib import admin
from django.urls import path, include
from users.views import get_csrf_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('csrf/', get_csrf_token, name='csrf'),
    path('auth/', include('dj_rest_auth.urls')),
    path('user/', include('users.urls')),
    path('place/', include('places.urls')),
    path('request/', include('requests.urls')),
]
