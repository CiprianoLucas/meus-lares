from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('place/', include('places.urls')),
    path('request/', include('requests.urls')),
    path('ai/', include('ai.urls')),
]
