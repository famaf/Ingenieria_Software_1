from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^', include('apps.index.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fotos/', include('apps.foto.urls', namespace='fotos')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
