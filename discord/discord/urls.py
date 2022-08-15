
from django.contrib import admin
from django.urls import path, include
from base.views import home_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('room/', include('base.urls')),
    path('api/', include('base.api.urls')),
]
