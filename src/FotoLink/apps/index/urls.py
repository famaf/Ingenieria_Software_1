# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import Registrarse


urlpatterns = [
    url(r'^registrar/$', Registrarse.as_view(), name='registrarse'),
    url(r'^$', 'apps.index.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',
        name='logout'),
    url(r'^success_register/$', 'apps.index.views.success_register',
        name='success_register'),
    url(r'^confirm_logout/$', 'apps.index.views.confirm_logout',
        name='confirm_logout'),
    url(r'^cambiar_password/$', 'apps.index.views.cambiar_password',
        name='cambiar_password'),
    url(r'^success_password/$', 'apps.index.views.success_password',
        name='success_password'),
    url(r'^modificar_privacidad/$', 'apps.index.views.modificar_privacidad',
        name='modificar_privacidad'),
    url(r'^ver_perfil/$', 'apps.index.views.ver_perfil', name='ver_perfil'),
    url(r'^editar_perfil/$', 'apps.index.views.Editar_perfil',
        name='editar_perfil'),
    url(r'^ver_notificacion/(?P<notificacion_id>\d+)/$',
        'apps.index.views.ver_notificacion', name='ver_notificacion'),
]
