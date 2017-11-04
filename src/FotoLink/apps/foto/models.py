# -*- coding: utf-8 -*-

from django.db import models
from apps.index.models import Perfil


class Foto(models.Model):
    """
    Modelo Foto, como en el diagrama de clases, este Objeto Modelo permite
    almacenar efectivamente la imagen en la base de datos junto a sus
    atributos, Ciudad, Pais, Lugar, Fecha, Momento.
    """

    # como el proyecto esta en ingles no me toma la enie
    MANIANA = 'Ma'
    TARDE = 'Ta'
    NOCHE = 'No'

    MOMENTOS = (
        (MANIANA, 'Mañana'),
        (TARDE, 'Tarde'),
        (NOCHE, 'Noche'),
        )
    Ciudad = models.CharField(max_length=50, blank=True)
    Pais = models.CharField(max_length=50, blank=True)
    Lugar = models.CharField(max_length=50, blank=True)
    Fecha = models.DateField(null=True)
    Momento = models.CharField(max_length=2, choices=MOMENTOS, default=TARDE)
    imagen = models.ImageField(upload_to='foto_db')

    def __unicode__(self):
        return str(self.id)


class search(models.Model):
    MANIANA = 'Ma'
    TARDE = 'Ta'
    NOCHE = 'No'

    MOMENTOS = (
        (MANIANA, 'Mañana'),
        (TARDE, 'Tarde'),
        (NOCHE, 'Noche'),
        )

    Lugar = models.CharField(max_length=50, blank=True)
    Momento = models.CharField(max_length=2, choices=MOMENTOS, default=None,
                               blank=True)
    Fecha = models.DateField(blank=True)
    Etiquetado = models.BooleanField(blank=True)


class Etiqueta(models.Model):
    link = models.ForeignKey(Foto)
    nombre = models.CharField(max_length=50)
