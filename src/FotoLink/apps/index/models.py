# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

BOOL_CHOICES = (('TRUE', 'Privado'), ('FALSE', 'Publico'))


class PerfilAttributeChar(models.Model):
    """
    Esta clase modela la tupla (Atributo, Privacidad), cuando atributo es de
    tipo String, y privacidad de tipo Boolean.
    """
    value = models.CharField(max_length=250, blank=True)
    privacity = models.CharField(max_length=250, blank=False,
                                 choices=BOOL_CHOICES)

    def __unicode__(self):
        return self.value


class PerfilAttributeInteger(models.Model):
    """
    Esta clase modela la tupla (Atributo, Privacidad), cuando atributo es de
    tipo Int, y privacidad de tipo Boolean.
    """
    value = models.IntegerField(default=0)
    privacity = models.CharField(max_length=250, blank=False,
                                 choices=BOOL_CHOICES)

    def __unicode__(self):
        return self.value


class PerfilAttributeEmail(models.Model):
    """
    Esta clase modela la tupla (Atributo, Privacidad), para poder almacenar el
    email, se podria haber utilizado PerfilAtrributeChar, pero perderiamos el
    metodo que incorpora EmailField (clean_email), para asegurarnos que es un
    email "valido".
    """
    value = models.EmailField(max_length=254, blank=True)
    privacity = models.CharField(max_length=250, blank=False,
                                 choices=BOOL_CHOICES)

    def __unicode__(self):
        return self.value


class Perfil(models.Model):
    """
    Modelo que permite almacenar el perfil del usuario en la base de datos.
    """
    usuario = models.OneToOneField(User)
    is_admin = models.BooleanField(default=False)
    nombre = PerfilAttributeChar()
    apellido = PerfilAttributeChar()
    edad = PerfilAttributeInteger()
    telefono = PerfilAttributeInteger()
    pais = PerfilAttributeChar()
    provincia = PerfilAttributeChar()
    ciudad = PerfilAttributeChar()
    direccion = PerfilAttributeChar()
    mail = PerfilAttributeEmail()
    estado_Civil = PerfilAttributeChar()
    facebook = PerfilAttributeChar()

    def __unicode__(self):
        return self.usuario.username

# VISTA_CHOICES = (('TRUE', 'vista'), ('FALSE', 'no_vista'))


class Notificacion(models.Model):
    link = models.ForeignKey(User)
    foto_id = models.IntegerField()
    mensaje = models.TextField()
    estado = models.BooleanField(default=False)
