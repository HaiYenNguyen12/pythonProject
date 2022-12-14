
from django.contrib import admin
from django.urls import path, include
from base.views import home_view
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('room/', include('base.urls')),
    path('api/', include('base.api.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)