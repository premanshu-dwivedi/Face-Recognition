from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # OWN APP URL
    path("", include("recapp.urls")),
    path("api/face-recognition/", include("recapi.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
