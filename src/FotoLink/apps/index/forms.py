# -*- coding: utf-8 -*-

from collections import OrderedDict
from django import forms

from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import Perfil
from django.contrib.auth.forms import UserCreationForm

from django.forms.extras.widgets import *


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput, min_length=6)

    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput, min_length=6,
                                help_text=("Enter the same password "
                                           "as above, for verification."))

    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        """
        Metodo que muestra error en caso que de los password ingresados por
        el usuario no coincidan.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserForm(UserCreationForm):
    """
    Formulario que es utilizado para el registro de un usuario en la base de
    datos.
    """
    nombre = forms.CharField(max_length=250)
    apellido = forms.CharField(max_length=250)
    edad = forms.IntegerField()
    telefono = forms.IntegerField()
    pais = forms.CharField(max_length=250)
    provincia = forms.CharField(max_length=250)
    ciudad = forms.CharField(max_length=250)
    direccion = forms.CharField(max_length=250)
    mail = forms.EmailField(max_length=254)
    estado_Civil = forms.CharField(max_length=250)
    facebook = forms.CharField(max_length=250)


class ModifyPrivacity(forms.Form):
    """
    Un formulario que le permite al usuario modificar su la privacidad de
    los atributos de su perfil
    """

    BOOL_CHOICES = (('TRUE', 'Privado'), ('FALSE', 'Publico'))

    nombre = forms.ChoiceField(choices=BOOL_CHOICES)
    apellido = forms.ChoiceField(choices=BOOL_CHOICES)
    edad = forms.ChoiceField(choices=BOOL_CHOICES)
    telefono = forms.ChoiceField(choices=BOOL_CHOICES)
    pais = forms.ChoiceField(choices=BOOL_CHOICES)
    ciudad = forms.ChoiceField(choices=BOOL_CHOICES)
    mail = forms.ChoiceField(choices=BOOL_CHOICES)
    provincia = forms.ChoiceField(choices=BOOL_CHOICES)
    direccion = forms.ChoiceField(choices=BOOL_CHOICES)
    estado_Civil = forms.ChoiceField(choices=BOOL_CHOICES)
    facebook = forms.ChoiceField(choices=BOOL_CHOICES)


class ModifyProfile(forms.Form):
    """
    Un formulario que le permite al usuario modificar su perfil.
    """
    nombre = forms.CharField(max_length=250)
    apellido = forms.CharField(max_length=250)
    edad = forms.IntegerField()
    telefono = forms.IntegerField()
    pais = forms.CharField(max_length=250)
    provincia = forms.CharField(max_length=250)
    ciudad = forms.CharField(max_length=250)
    direccion = forms.CharField(max_length=250)
    mail = forms.EmailField(max_length=254)
    estado_Civil = forms.CharField(max_length=250)
    facebook = forms.CharField(max_length=250)


class SetPasswordForm2(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_("Nuevo Password"),
                                    widget=forms.PasswordInput, min_length=6)
    new_password2 = forms.CharField(label=_("Repetir Nuevo Password"),
                                    widget=forms.PasswordInput, min_length=6)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm2, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm2(SetPasswordForm2):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(SetPasswordForm2.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
    })
    old_password = forms.CharField(label=_("Password Viejo"),
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

PasswordChangeForm2.base_fields = OrderedDict(
    (k, PasswordChangeForm2.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)
