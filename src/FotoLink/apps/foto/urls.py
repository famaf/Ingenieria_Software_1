# -*- coding: utf-8 -*-

from django.conf.urls import url
from apps.foto import views

urlpatterns = [
    url(r'^subir_foto/$', views.upload_image, name='subir_foto'),
    url(r'^buscar_foto/$', views.search_image, name='buscar_foto'),
    url(r'^remove_photo/(?P<id_remove>\d+)/$', views.remove_photo,
        name='remove_photo'),
    url(r'^etiquetar_foto/(?P<id_foto>\d+)/$',
        views.etiquetar_foto, name='etiquetar_foto'),
    url(r'^ver_foto/(?P<id_foto>\d+)/$', views.ver_foto, name='ver_foto'),
    url(r'^success_tag/(?P<id_foto>\d+)/$',
        views.success_tag, name='success_tag'),
    url(r'^success_fail_tag/(?P<id_foto>\d+)/$',
        views.success_fail_tag, name='success_fail_tag'),
    url(r'^mostrar_perfil/(?P<username>\w+)/$',
        views.mostrar_perfil, name='mostrar_perfil'),
]
