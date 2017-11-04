# -*- coding: utf-8 -*-
import warnings

from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.deprecation import RemovedInDjango110Warning
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

# =========================================================================


from django.views.generic import FormView, ListView
from .models import (Perfil, PerfilAttributeChar, PerfilAttributeInteger,
                     PerfilAttributeEmail, Notificacion)
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.contrib.auth import update_session_auth_hash

from .forms import (UserForm, ModifyPrivacity, ModifyProfile,
                    PasswordChangeForm2)


def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    notificaciones_all = Notificacion.objects.filter(link_id=request.user.id)
    notificaciones = []
    for noti in notificaciones_all:
        if noti.estado is False:
            notificaciones.append(noti)
    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'notificaciones': notificaciones
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, 'index/login.html', context)


@login_required
def ver_perfil(request):
    """
    Metodo que permite ver el perfil del usuario
    """
    perfil = Perfil.objects.get(usuario_id=request.user.id)

    # Calculo lo indices para obtener los atributos del perfil
    index, index2 = get_indexs(perfil.id)

    # Obtengo los objetos
    mail, edad, telefono, nombre, apellido, pais, ciudad, provincia,\
        direccion, estado_Civil, facebook =\
        obtener_atr_perfil(perfil.id, index, index2)

    # Diccionario con los objetos obtenidos
    data = crear_dict_de_datos(nombre, apellido, edad, ciudad,
                               provincia, pais, direccion, estado_Civil,
                               facebook, mail, telefono)

    return render_to_response('index/ver_perfil.html',
                              context_instance=RequestContext(request, data))


@login_required
def ver_notificacion(request, notificacion_id):
    '''
    Metodo para visualizar una notificaion
    '''
    notificacion = Notificacion.objects.get(id=notificacion_id)
    notificacion.estado = True
    notificacion.save()
    data = {
        'notificacion': notificacion,
    }
    return TemplateResponse(request, 'index/ver_notificacion.html',
                            context=data)


@login_required
def cambiar_password(request):
    """
    Metodo que muestra el formulario para que un usuario registrado
    pueda cambiar su password. En caso de exito, el usuario sera notificado.
    En caso de tener algun campo erroneo, se le pedira que lo reingrese.
    """
    form = PasswordChangeForm2(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm2(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return render(request, 'index/success_password.html',
                          {'form': form, })
        else:
            return render(request, 'index/cambiar_password.html',
                          {'form': form, })
    return render(request, 'index/cambiar_password.html', {'form': form, })


@login_required
def confirm_logout(request):
    """
    Metodo que muestra la confirmacion del deslogueo
    """
    return render_to_response('index/confirm_logout.html')


def success_register(request):
    """
    Metodo que muestra la confirmacion del registro
    """
    return render_to_response('index/success_register.html')


@login_required
def success_password(request):
    """
    Metodo que muestra la confirmacion del cambio de password
    """
    return render_to_response('index/success_password.html')


class Registrarse(FormView):
    """
    Clase que muestra al usario el formulario para que se registre
    """
    template_name = "index/registrar.html"
    form_class = UserForm
    success_url = reverse_lazy('success_register')

    def form_valid(self, form):
        """
        Metodo que guarda los datos ingresados por el usuario que se esta
        registrando.
        """
        user = form.save()
        perfil = Perfil()
        perfil.usuario = user
        perfil.is_admin = False
        perfil.nombre = PerfilAttributeChar()
        perfil.nombre.value = form.cleaned_data['nombre']
        perfil.nombre.privacity = "FALSE"
        perfil.nombre.save()
        perfil.apellido = PerfilAttributeChar()
        perfil.apellido.value = form.cleaned_data['apellido']
        perfil.apellido.privacity = "FALSE"
        perfil.apellido.save()
        perfil.edad = PerfilAttributeInteger()
        perfil.edad.value = form.cleaned_data['edad']
        perfil.edad.privacity = "TRUE"
        perfil.edad.save()
        perfil.telefono = PerfilAttributeInteger()
        perfil.telefono.value = form.cleaned_data['telefono']
        perfil.telefono.privacity = "TRUE"
        perfil.telefono.save()
        perfil.pais = PerfilAttributeChar()
        perfil.pais.value = form.cleaned_data['pais']
        perfil.pais.privacity = "TRUE"
        perfil.pais.save()
        perfil.ciudad = PerfilAttributeChar()
        perfil.ciudad.value = form.cleaned_data['ciudad']
        perfil.ciudad.privacity = "TRUE"
        perfil.ciudad.save()
        perfil.mail = PerfilAttributeEmail()
        perfil.mail.value = form.cleaned_data['mail']
        perfil.mail.privacity = "TRUE"
        perfil.mail.save()
        perfil.provincia = PerfilAttributeChar()
        perfil.provincia.value = form.cleaned_data['provincia']
        perfil.provincia.privacity = "TRUE"
        perfil.provincia.save()
        perfil.direccion = PerfilAttributeChar()
        perfil.direccion.value = form.cleaned_data['direccion']
        perfil.direccion.privacity = "TRUE"
        perfil.direccion.save()
        perfil.estado_Civil = PerfilAttributeChar()
        perfil.estado_Civil.value = form.cleaned_data['estado_Civil']
        perfil.estado_Civil.privacity = "TRUE"
        perfil.estado_Civil.save()
        perfil.facebook = PerfilAttributeChar()
        perfil.facebook.value = form.cleaned_data['facebook']
        perfil.facebook.privacity = "TRUE"
        perfil.facebook.save()
        perfil.save()
        return super(Registrarse, self).form_valid(form)


@login_required
def modificar_privacidad(request):
    """
    Metodo que le permite al usuario modificar la privacidad de los atributos
    de su perfil.
    """
    if request.method == 'POST':
        form = ModifyPrivacity(request.POST)
        if form.is_valid():
            perfil = Perfil.objects.get(usuario_id=request.user.id)

            # Indices para obtener los objetos del Perfil
            index, index2 = get_indexs(perfil.id)

            # Obtengo los objetos
            mail, edad, telefono, nombre, apellido, pais, ciudad, provincia,\
                direccion, estado_Civil, facebook =\
                obtener_atr_perfil(perfil.id, index, index2)

            nombre.privacity = form.cleaned_data['nombre']
            nombre.save()
            apellido.privacity = (form.cleaned_data['apellido'])
            apellido.save()
            edad.privacity = form.cleaned_data['edad']
            edad.save()
            telefono.privacity = (form.cleaned_data['telefono'])
            telefono.save()
            pais.privacity = form.cleaned_data['pais']
            pais.save()
            ciudad.privacity = form.cleaned_data['ciudad']
            ciudad.save()
            mail.privacity = form.cleaned_data['mail']
            mail.save()
            provincia.privacity = (form.cleaned_data['provincia'])
            provincia.save()
            direccion.privacity = (form.cleaned_data['direccion'])
            direccion.save()
            estado_Civil.privacity = (form.cleaned_data['estado_Civil'])
            estado_Civil.save()
            facebook.privacity = (form.cleaned_data['facebook'])
            facebook.save()
            perfil.save()
            request.user.save()
            return render_to_response('index/success_modify.html')
    else:
        form = ModifyPrivacity()
        return render_to_response('index/modificar_privacidad.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))


@login_required
def Editar_perfil(request):
    """
    Metodo que le permite al usuario modificar los datos de su perfil.
    """
    perfil = Perfil.objects.get(usuario_id=request.user.id)

    # Indices para obtener los objetos del Perfil
    index, index2 = get_indexs(perfil.id)

    # Obtengo los objetos
    mail, edad, telefono, nombre, apellido, pais, ciudad, provincia,\
        direccion, estado_Civil, facebook =\
        obtener_atr_perfil(perfil.id, index, index2)

    # Diccionario con los objetos obtenidos
    data = crear_dict_de_datos(nombre, apellido, edad, ciudad,
                               provincia, pais, direccion,
                               estado_Civil, facebook, mail, telefono)

    if request.method == 'POST':
        form = ModifyProfile(request.POST)
        if form.is_valid():
            nombre.value = form.cleaned_data['nombre']
            nombre.save()
            apellido.value = (form.cleaned_data['apellido'])
            apellido.save()
            edad.value = form.cleaned_data['edad']
            edad.save()
            telefono.value = (form.cleaned_data['telefono'])
            telefono.save()
            pais.value = form.cleaned_data['pais']
            pais.save()
            ciudad.value = form.cleaned_data['ciudad']
            ciudad.save()
            mail.value = form.cleaned_data['mail']
            mail.save()
            provincia.value = (form.cleaned_data['provincia'])
            provincia.save()
            direccion.value = (form.cleaned_data['direccion'])
            direccion.save()
            estado_Civil.value = (form.cleaned_data['estado_Civil'])
            estado_Civil.save()
            facebook.value = (form.cleaned_data['facebook'])
            facebook.save()
            perfil.save()
            request.user.save()
            return render_to_response('index/success_edit_perfil.html')
        else:
            context_instance = RequestContext(request, data)
            return render_to_response('index/editar_perfil.html',
                                      {'form': form},
                                      context_instance)
    else:
        form = ModifyProfile()
        context_instance = RequestContext(request, data)
        return render_to_response('index/editar_perfil.html',
                                  {'form': form},
                                  context_instance)


def get_indexs(id):
    '''
    Metodo que calcula los indices que se van a utilizar
    para obtener los atributos de un perfil.
    id = id del perfil del cual queremos obtener los atributos
    '''
    if (id != 1):
        index = (id - 1) * 8 + 1
        index2 = id * 2 - 1
    else:
        index = id
        index2 = id
    return index, index2


def crear_dict_de_datos(nombre, apellido, edad, ciudad, provincia, pais,
                        direccion, estado_Civil, facebook, mail, telefono):
    '''
    Metodo que crea un diccionario con los atributos de un perfil
    :return: el diccionario "data" con los atributos dentro
    '''
    data = {
        'nombre': nombre,
        'apellido': apellido,
        'edad': edad,
        'ciudad': ciudad,
        'provincia': provincia,
        'pais': pais,
        'direccion': direccion,
        'estado_Civil': estado_Civil,
        'facebook': facebook,
        'mail': mail,
        'telefono': telefono,
    }
    return data


def obtener_atr_perfil(id, index, index2):
    '''
    Metodo que obtiene de la BD todos los atributos referidos
    a un perfil
    :param id: index para obtener los PerfilAttributeEmail
    :param index: index para obtener los PerfilAttributeChar
    :param index2: index para obtener los PerfilAttributeInteger
    :return: todos los attibutos de un perfil
    '''
    mail = PerfilAttributeEmail.objects.get(id=id)
    edad = PerfilAttributeInteger.objects.get(id=index2)
    telefono = PerfilAttributeInteger.objects.get(id=index2 + 1)
    nombre = PerfilAttributeChar.objects.get(id=index)
    apellido = PerfilAttributeChar.objects.get(id=index + 1)
    pais = PerfilAttributeChar.objects.get(id=index + 2)
    ciudad = PerfilAttributeChar.objects.get(id=index + 3)
    provincia = PerfilAttributeChar.objects.get(id=index + 4)
    direccion = PerfilAttributeChar.objects.get(id=index + 5)
    estado_Civil = PerfilAttributeChar.objects.get(id=index + 6)
    facebook = PerfilAttributeChar.objects.get(id=index + 7)
    return mail, edad, telefono, nombre, apellido, pais, ciudad,\
        provincia, direccion, estado_Civil, facebook
