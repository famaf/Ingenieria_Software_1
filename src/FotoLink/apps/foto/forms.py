# -*- coding: utf-8 -*-

from django import forms
from datetime import date
from .models import Foto, search
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import ValidationError


class FotoForm(forms.ModelForm):
    """
    Formulario que se utiliza para subir una foto a la base de datos
    Extiende del objeto ModelForm
    """
    error_messages = {
        'invalid_date': _("la fecha es inexistente"),
    }

    class Meta:
        model = Foto
        fields = ['Ciudad', 'Pais', 'Lugar', 'Fecha', 'Momento', 'imagen']

    def clean_Ciudad(self):
        """
        Redefine el metodo clean, que viene por defecto
        """
        Ciudad = self.cleaned_data.get('Ciudad')
        return Ciudad

    def clean_Pais(self):
        """
        Redefine el metodo clean, que viene por defecto
        """

        Pais = self.cleaned_data.get('Pais')
        return Pais

    def clean_Lugar(self):
        """
        Redefine el metodo clean, que viene por defecto
        """
        Lugar = self.cleaned_data.get('Lugar')
        return Lugar

    def clean_Fecha(self):
        """
        Redefine el metodo clean del objeto, en este caso para que no se pueda
        ingresar una fecha posterior a la actual del servidor.
        En caso de ingresar una fecha posterior a la actual, este metodo se
        encarga de mostrar el error.
        """
        Fecha = self.cleaned_data.get('Fecha')
        if Fecha > date.today():
            raise forms.ValidationError('fecha invalida')
        return Fecha

        # self.error_messages['invalid_date'],
        # code='invalid_date',


class SearchForm(forms.ModelForm):
    """
    Formulario que permite realizar busqueda de imagenes
    """
    class Meta:
        model = search
        fields = ['Lugar', 'Momento', 'Fecha', 'Etiquetado']
