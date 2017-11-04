# -*- coding: utf8 -*-
from django.db.models import Q
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apps.index.models import (
    PerfilAttributeChar, PerfilAttributeInteger,
    PerfilAttributeEmail, Notificacion)
from apps.index.views import obtener_atr_perfil, get_indexs

from .forms import FotoForm, SearchForm
from .models import Foto, Perfil, Etiqueta


@login_required(login_url='')
def mostrar_perfil(request, username):
    '''
    Metodo que muestra el perfil de un usuario etiquetado en una foto
    '''
    user = User.objects.get(username=username)

    perfil = Perfil.objects.get(usuario_id=user.id)

    # Calculo los indices
    index, index2 = get_indexs(perfil.id)

    # Obtengo los objetos
    mail, edad, telefono, nombre, apellido, pais, ciudad, provincia,\
        direccion, estado_Civil, facebook =\
        obtener_atr_perfil(perfil.id, index, index2)

    # Creo una lista con los atributos publicos
    lista_atributos_publicos = []
    if nombre.privacity == 'FALSE':
        lista_atributos_publicos.append("Nombre: " + str(nombre.value))
    if apellido.privacity == 'FALSE':
        lista_atributos_publicos.append("Apellido: " + str(apellido.value))
    if edad.privacity == 'FALSE':
        lista_atributos_publicos.append("Edad: " + str(edad.value))
    if telefono.privacity == 'FALSE':
        lista_atributos_publicos.append("Telefono: " + str(telefono.value))
    if pais.privacity == 'FALSE':
        lista_atributos_publicos.append("Pais: " + str(pais.value))
    if provincia.privacity == 'FALSE':
        lista_atributos_publicos.append("Provincia: " + str(provincia.value))
    if ciudad.privacity == 'FALSE':
        lista_atributos_publicos.append("Ciudad: " + str(ciudad.value))
    if direccion.privacity == 'FALSE':
        lista_atributos_publicos.append("Direccion: " + str(direccion.value))
    if mail.privacity == 'FALSE':
        lista_atributos_publicos.append("Mail: " + str(mail.value))
    if estado_Civil.privacity == 'FALSE':
        lista_atributos_publicos.append(
            "Estado Civil: " + str(estado_Civil.value))
    if facebook.privacity == 'FALSE':
        lista_atributos_publicos.append("Facebook: " + str(facebook.value))

    data = {
        'lista_atributos_publicos': lista_atributos_publicos,
        'username': username,
    }
    return render_to_response('foto/mostrar_perfil.html',
                              context_instance=RequestContext(request, data))


@login_required(login_url='')
def success_tag(request, id_foto):
    """
    Metodo que muestra la confirmacion de etiqueta
    """
    foto = Foto.objects.get(id=id_foto)
    data = {
        'foto': foto
    }
    return TemplateResponse(request, 'foto/ver_foto.html', context=data)


@login_required(login_url='')
def success_fail_tag(request, id_foto):
    """
    Metodo que le informa al usuario que ya se encuentra etiquetado
    """
    foto = Foto.objects.get(id=id_foto)
    data = {
        'foto': foto
    }
    return TemplateResponse(request, 'foto/ver_foto.html', context=data)


@login_required(login_url='')
def ver_foto(request, id_foto):
    '''
    Metodo que muestra una foto con sus respectivas etiquetas
    '''
    foto = Foto.objects.get(id=id_foto)
    etiquetas = Etiqueta.objects.filter(link_id=id_foto)
    data = {
        'foto': foto,
        'etiquetas': etiquetas,
    }
    return TemplateResponse(request, 'foto/ver_foto.html',
                            context=data)


@login_required(login_url='')
def etiquetar_foto(request, id_foto):
    '''
    Metodo para etiquetar un usuario a una foto
    '''
    # Flag para verificar si el usuario ya se encuentra etiquetado
    flag = False
    foto = Foto.objects.get(id=id_foto)
    data = {
        'foto': foto,
    }

    et = Etiqueta.objects.filter(link_id=id_foto)
    # Recorro las etiquetas para ver si el usuario ya se encuentra etiquetado
    for e in et:
        if (str(e.nombre) == str(request.user)):
            flag = True
            break

    if flag:  # Si ya esta etiquetado
        return TemplateResponse(request, 'foto/success_fail_tag.html',
                                context=data)
    else:
        # Creo notificaiones para los ya etiquetados
        for e in et:
            user = User.objects.get(username=e.nombre)
            notificacion = Notificacion()
            notificacion.link = user
            notificacion.foto_id = id_foto
            notificacion.estado = False
            notificacion.mensaje = "El usuario " + \
                str(request.user) + \
                " se ha etiquetado en una foto en la que apareces etiquetado"
            notificacion.save()
        # Creo la etiqueta
        etiqueta = Etiqueta()
        etiqueta.link = foto
        etiqueta.nombre = request.user
        etiqueta.save()
        return TemplateResponse(request, 'foto/success_tag.html', context=data)


@login_required(login_url='')
def upload_image(request):
    """
    Esta vista permite que el usuario suba sus fotos la base de datos
    mediante el llenado de un formulario.
    """
    form = FotoForm()
    title = "Sube tu foto"
    title2 = "Foto Subida con exito"
    context = {
        "title": title,
        "form": form
    }

    if request.method == 'POST':
        formu = FotoForm(request.POST, request.FILES)
        if formu.is_valid():
            save_it = formu.save(commit=False)
            save_it.save()
            return render(request,
                          "foto/success_subir.html", {"title2": title})
        else:
            formulario = FotoForm()
            advertencia = "Formulario con error, reingreselo porfavor"
            context = {"advertencia": advertencia, "form": formulario}
            return render(request, "foto/subir_foto.html", context)

    return render_to_response(
        'foto/subir_foto.html',
        context,
        context_instance=RequestContext(request))


@login_required(login_url='')
def search_image(request):
    """
    Vista realiza la busqueda de fotos dentro de la base de datos.
    Filtrara los resultados segun Lugar, Fecha, Momento y si Esta
    etiquetado o no.
    """
    form = SearchForm()
    title = "Buscar Foto"
    results = []
    if request.method == 'POST':
        formu = SearchForm(request.POST)
        if formu.is_valid():
            perfil = Perfil.objects.get(usuario_id=request.user.id)

            lugar = formu.cleaned_data['Lugar']
            fecha = formu.cleaned_data['Fecha']
            momento = formu.cleaned_data['Momento']
            etiquetado = formu.cleaned_data['Etiquetado']

            # Instancio los Q Objects fuera de las queries
            # para no violar las condiciones de Pep8
            momento_q = Q(Momento=momento)
            etiqueta_q = Q(Etiquetado=etiquetado)
            fecha_q = Q(Fecha=fecha)
            lugar_q = Q(Lugar=lugar)

            result = []
            if (len(lugar) == 0):
                if(fecha is None):
                    if(len(momento) == 0):
                        if not etiquetado:  # Busqueda vacia
                            result = Foto.objects.all()
                        else:               # Busqueda(etiqueta)
                            mis_etiquetas =\
                                Etiqueta.objects.filter(nombre=request.user)
                            for et in mis_etiquetas:
                                foto = Foto.objects.get(id=et.link_id)
                                result.append(foto)
                    else:
                        if not etiquetado:  # Busqueda(momento)
                            result = Foto.objects.filter(momento_q)
                        else:               # Busqueda(momento, etiqueta)
                            list_foto = Foto.objects.filter(momento_q)
                            mis_etiquetas =\
                                Etiqueta.objects.filter(nombre=request.user)
                            for fot in list_foto:
                                for et in mis_etiquetas:
                                    if et.link_id == fot.id:
                                        result.append(fot)
                else:
                    if(len(momento) == 0):
                        if not etiquetado:  # Busqueda(fecha)
                            result = Foto.objects.filter(fecha_q)
                        else:               # Busqueda(fecha,etiqueta)
                            list_foto = Foto.objects.filter(fecha_q)
                            mis_etiquetas =\
                                Etiqueta.objects.filter(nombre=request.user)
                            for fot in list_foto:
                                for et in mis_etiquetas:
                                    if et.link_id == fot.id:
                                        result.append(fot)
                    else:
                        if not etiquetado:  # Busqueda(momento, fecha)
                            result = Foto.objects.filter(
                                momento_q).filter(fecha_q)
                        else:              # Busqueda(momento, fecha, etiqueta)
                            list_foto =\
                                Foto.objects.filter(momento_q).filter(fecha_q)
                            mis_etiquetas =\
                                Etiqueta.objects.filter(nombre=request.user)
                            for fot in list_foto:
                                for et in mis_etiquetas:
                                    if et.link_id == fot.id:
                                        result.append(fot)
            else:
                if(fecha is None):
                    if(len(momento) == 0):
                        if not etiquetado:  # Busqueda(lugar)
                            result = Foto.objects.filter(lugar_q)
                        else:               # Busqueda(lugar, etiqueta)
                            list_foto = Foto.objects.filter(lugar_q)
                            mis_etiquetas =\
                                Etiqueta.objects.filter(nombre=request.user)
                            for fot in list_foto:
                                for et in mis_etiquetas:
                                    if et.link_id == fot.id:
                                        result.append(fot)
                    else:
                        if not etiquetado:  # Busqueda(momento, lugar)
                            result = Foto.objects.filter(
                                momento_q).filter(lugar_q)
                        else:              # Busqueda(momento, lugar, etiqueta)
                            list_foto =\
                                Foto.objects.filter(momento_q).filter(lugar_q)
                            mis_etiquetas =\
                                Etiqueta.objects.filter(nombre=request.user)
                            for fot in list_foto:
                                for et in mis_etiquetas:
                                    if et.link_id == fot.id:
                                        result.append(fot)
                else:
                    if(len(momento) == 0):
                        if not etiquetado:  # Busqueda(fecha, lugar)
                            result = Foto.objects.filter(
                                fecha_q).filter(lugar_q)
                        else:               # Busqueda(fecha, lugar, etiqueta)
                            list_foto =\
                                Foto.objects.filter(fecha_q).filter(lugar_q)
                            mis_etiquetas =\
                                Etiqueta.objects.filter(nombre=request.user)
                            for fot in list_foto:
                                for et in mis_etiquetas:
                                    if et.link_id == fot.id:
                                        result.append(fot)
                    else:
                        if not etiquetado:  # Busqueda(momento, fecha, lugar)
                            result = Foto.objects.filter(
                                momento_q).filter(fecha_q).filter(lugar_q)
                        else:       # Busqueda(momento, fecha, lugar, etiqueta)
                            list_foto = Foto.objects.filter(momento_q).\
                                filter(fecha_q).filter(lugar_q)
                            mis_etiquetas =\
                                Etiqueta.objects.filter(nombre=request.user)
                            for fot in list_foto:
                                for et in mis_etiquetas:
                                    if et.link_id == fot.id:
                                        result.append(fot)

            return render(request, "foto/mostrar_busqueda.html",
                          {"result": result, "perfil": perfil})

        else:
            pass
    dictio = {"form": form, "title": title, "results": results}
    return render_to_response(
        "foto/buscar_foto.html",
        dictio,
        context_instance=RequestContext(request))


@login_required(login_url='')
def remove_photo(request, id_remove):
    """
    Vista que permite eliminar una foto de acuerdo al id_remove
    que recibe. Ese ide refiere a una instancia de Foto dentro de
    la base de datos.
    """
    Foto.objects.filter(id=id_remove).delete()
    return render_to_response('foto/foto_borrada.html')
