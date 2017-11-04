# -*- coding: utf8 -*-
from django.test import TestCase, RequestFactory
from django.test import Client
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import (Perfil, PerfilAttributeChar,
                     PerfilAttributeEmail, PerfilAttributeInteger,
                     Notificacion)
from .views import (ver_perfil, modificar_privacidad, cambiar_password,
                    success_password, success_register, confirm_logout, login,
                    Registrarse, Editar_perfil, ver_notificacion)
from .forms import (PasswordChangeForm2, ModifyPrivacity, UserForm,
                    ModifyProfile)
from apps.foto.models import Foto


class UsersTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.user = User.objects.create_user(username='pepe',
                                             password='123456')
        self.nombre = PerfilAttributeChar.objects.create(
            value="Nahuel", privacity="FALSE")
        self.apellido = PerfilAttributeChar.objects.create(
            value="Palma", privacity="FALSE")
        self.pais = PerfilAttributeChar.objects.create(
            value="Argentina", privacity="TRUE")
        self.provincia = PerfilAttributeChar.objects.create(
            value="Cordoba", privacity="TRUE")
        self.ciudad = PerfilAttributeChar.objects.create(
            value="Alejandro", privacity="TRUE")
        self.direccion = PerfilAttributeChar.objects.create(
            value="Sarmiento 123",
            privacity="TRUE")
        self.estado_Civil = PerfilAttributeChar.objects.create(
            value="soltero",
            privacity="TRUE")
        self.facebook = PerfilAttributeChar.objects.create(
            value="nahuel.palma",
            privacity="TRUE")
        self.edad = PerfilAttributeInteger.objects.create(
            value=26,
            privacity="TRUE")
        self.telefono = PerfilAttributeInteger.objects.create(
            value=2323232323232,
            privacity="TRUE")
        self.mail = PerfilAttributeEmail.objects.create(value="n@gmail.com",
                                                        privacity="TRUE")
        self.perfil = Perfil.objects.create(usuario=self.user,
                                            is_admin=False)

        self.user1 = User.objects.create_user(
            username='nahue', password='111111')
        self.user2 = User.objects.create_user(
            username='juano', password='123456')

        self.nombre1 = PerfilAttributeChar.objects.create(
            value="Nahuel", privacity="FALSE")
        self.apellido1 = PerfilAttributeChar.objects.create(
            value="Palma", privacity="FALSE")
        self.pais1 = PerfilAttributeChar.objects.create(
            value="Argentina", privacity="TRUE")
        self.provincia1 = PerfilAttributeChar.objects.create(
            value="Cordoba", privacity="TRUE")
        self.ciudad1 = PerfilAttributeChar.objects.create(
            value="Alejandro", privacity="TRUE")
        self.direccion1 = PerfilAttributeChar.objects.create(
            value="Sarmiento 123", privacity="TRUE")
        self.estado_Civil1 = PerfilAttributeChar.objects.create(
            value="soltero", privacity="TRUE")
        self.facebook1 = PerfilAttributeChar.objects.create(
            value="nahuel.palma", privacity="TRUE")
        self.edad1 = PerfilAttributeInteger.objects.create(
            value=26, privacity="TRUE")
        self.telefono1 = PerfilAttributeInteger.objects.create(
            value=2323232323232, privacity="TRUE")
        self.mail1 = PerfilAttributeEmail.objects.create(
            value="n@gmail.com", privacity="TRUE")

        self.nombre2 = PerfilAttributeChar.objects.create(
            value="Juan Ignacio", privacity="FALSE")
        self.apellido2 = PerfilAttributeChar.objects.create(
            value="Farias", privacity="FALSE")
        self.pais2 = PerfilAttributeChar.objects.create(
            value="Argentina", privacity="TRUE")
        self.provincia2 = PerfilAttributeChar.objects.create(
            value="Cordoba", privacity="TRUE")
        self.ciudad2 = PerfilAttributeChar.objects.create(
            value="Jesus Maria", privacity="TRUE")
        self.direccion2 = PerfilAttributeChar.objects.create(
            value="Palermo s/n", privacity="TRUE")
        self.estado_Civil2 = PerfilAttributeChar.objects.create(
            value="soltero", privacity="TRUE")
        self.facebook2 = PerfilAttributeChar.objects.create(
            value="juano.farias", privacity="TRUE")
        self.edad2 = PerfilAttributeInteger.objects.create(
            value=26, privacity="TRUE")
        self.telefono2 = PerfilAttributeInteger.objects.create(
            value=2323232323232, privacity="TRUE")
        self.mail2 = PerfilAttributeEmail.objects.create(
            value="n@gmail.com", privacity="TRUE")

        self.perfil1 = Perfil.objects.create(usuario=self.user1,
                                             is_admin=False)
        self.perfil2 = Perfil.objects.create(usuario=self.user2,
                                             is_admin=False)

        self.foto = Foto.objects.create(Ciudad='Cordoba', Pais='Argentina',
                                        Lugar='Casa', Fecha='2015-01-01',
                                        Momento='TA')

        self.notificacion = Notificacion.objects.create(link=self.user1,
                                                        foto_id=self.foto.id,
                                                        mensaje="mensaje",
                                                        estado=False)


class VerPerfilTestCase(UsersTestCase):

    def test_ver_perfil_exitoso(self):
        """
        verifica la vista que permite ver el perfil
        """
        request = self.factory.get('ver_perfil')
        request.user = self.user1
        response = ver_perfil(request)
        with open("test_index_html/ver_perfil1.html", 'r') as expected:
            self.assertHTMLEqual(expected.read(), response.content)
        self.assertEqual(response.status_code, 200)

    def test_ver_perfil_fallido(self):
        """
        verifica que un usuario solo puede ver su perfil utilizando
        esta vista y que ningun otro puede
        """
        request = self.factory.get('ver_perfil')
        request.user = self.user2
        response = ver_perfil(request)
        with open("test_index_html/ver_perfil1.html", 'r') as expected:
            self.assertHTMLNotEqual(expected.read(), response.content)
        self.assertEqual(response.status_code, 200)


class ModifyPrivacityTestCase(UsersTestCase):

    def test_modificar_privacidad(self):
        """
        verifica la vista que permite modificar la privacidad
        """
        request = self.factory.post('modificar_privacidad')
        request.user = self.user1

        # Prueba formulario invalido
        data = {
            'nombre': "TRUE",
            'apellido': "TRUE",
        }
        form = ModifyPrivacity(data)
        self.assertFalse(form.is_valid())

        # Prueba formulario valido
        data = {
            'nombre': "TRUE",
            'apellido': "TRUE",
            'edad': "TRUE",
            'telefono': "TRUE",
            'pais': "TRUE",
            'ciudad': "TRUE",
            'mail': "TRUE",
            'provincia': "TRUE",
            'direccion': "TRUE",
            'estado_Civil': "TRUE",
            'facebook': "TRUE",
        }
        form = ModifyPrivacity(data)
        self.assertTrue(form.is_valid())

        request.POST = data
        response = modificar_privacidad(request)

        response = ver_perfil(request)
        with open("test_index_html/mod_privacidad.html", 'r') as expected:
            self.assertHTMLEqual(expected.read(), response.content)

        self.assertEqual(response.status_code, 200)


class EditarPerfilTestCase(UsersTestCase):

    def test_editar_perfil(self):
        """
        verifica la vista que permite editar el perfil
        """
        request = self.factory.get('editar_perfil')
        request.user = self.user1
        response = Editar_perfil(request)
        with open("test_index_html/editar.html", 'r') as expected:
            self.assertHTMLEqual(expected.read(), response.content)
        self.assertEqual(response.status_code, 200)

    def test_editar_perfil_nombre(self):
        """
        verifica que se puede ver el perfil y que luego se pueda
        cambiar el nombre validando el formulario al realizar esta
        accion
        """
        request = self.factory.get('ver_perfil')
        request.user = self.user1
        response = ver_perfil(request)
        with open("test_index_html/ver_nombre_nahuel.html", 'r') as expected:
            self.assertHTMLEqual(expected.read(), response.content)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('editar_perfil')
        request.user = self.user1
        data = {'nombre': 'Juan',
                'apellido': 'Palma',
                'edad': '26',
                'telefono': '2323232323232',
                'pais': 'Argentina',
                'provincia': 'Alejandro',
                'ciudad': 'Cordoba',
                'direccion': 'Sarmiento 123',
                'mail': 'n@gmail.com',
                'estado_Civil': 'soltero',
                'facebook': 'nahuel.palma'}
        request.POST = data
        form = ModifyProfile(data)
        self.assertTrue(form.is_valid())


class LogsTestCase(UsersTestCase):
    """
    Tests que chequean todo lo relacionado con el login/logout
    """

    def test_login(self):
        """
        Test que comprueba el login con
        username y password validos
        """
        data = {'username': 'pepe', 'password': '123456'}
        request = self.factory.get('login')
        request.user = self.user
        request.POST = data
        formulario = AuthenticationForm(request, request.POST)
        self.assertTrue(formulario.is_valid())
        response = login(request)
        self.assertEqual(response.status_code, 200)

    def test_login_fail_1(self):
        """
        Test que comprueba el login con
        username valido y password invalido
        """
        data = {'username': 'pepe', 'password': '123'}
        request = self.factory.get('login')
        request.user = self.user
        request.POST = data
        formulario = AuthenticationForm(request, request.POST)
        self.assertFalse(formulario.is_valid())
        response = login(request)
        self.assertEqual(response.status_code, 200)

    def test_login_fail_2(self):
        """
        Test que comprueba el login con
        username invalido y password valido
        """
        data = {'username': 'pepito', 'password': '123456'}
        request = self.factory.get('login')
        request.user = self.user
        request.POST = data
        formulario = AuthenticationForm(request, request.POST)
        self.assertFalse(formulario.is_valid())
        response = login(request)
        self.assertEqual(response.status_code, 200)

    def test_login_fail_3(self):
        """
        Test que comprueba el login con
        username y password vacios
        """
        data = {'username': '', 'password': ''}
        request = self.factory.get('login')
        request.user = self.user
        request.POST = data
        formulario = AuthenticationForm(request, request.POST)
        self.assertFalse(formulario.is_valid())
        response = login(request)
        self.assertEqual(response.status_code, 200)

    def test_login_fail_4(self):
        """
        Test que comprueba el login con
        username y password invalidos
        """
        data = {'username': 'pepito', 'password': '1234'}
        request = self.factory.get('login')
        request.user = self.user
        request.POST = data
        formulario = AuthenticationForm(request, request.POST)
        self.assertFalse(formulario.is_valid())
        response = login(request)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """
        Test que comprueba el logout
        """
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_confirm_logout(self):
        """
        Test que comprueba la vista del confirm_logout
        """
        request = self.factory.get('confirm_logout')
        request.user = self.user
        response = confirm_logout(request)
        with open('test_html/confirmar_logout.html', 'r') as expected:
            # expected.write(response.content)
            self.assertHTMLEqual(expected.read(), response.content)
        self.assertEqual(response.status_code, 200)

    def test_success_register(self):
        """
        Test que comprueba la vista del success_register
        """
        request = self.factory.get('success_register')
        request.user = self.user
        response = success_register(request)
        with open('test_html/success_registro.html', 'r') as expected:
            # expected.write(response.content)
            self.assertHTMLEqual(expected.read(), response.content)
        self.assertEqual(response.status_code, 200)

    def test_success_password(self):
        """
        Test que comprueba la vista del success_password
        """
        request = self.factory.get('success_password')
        request.user = self.user
        response = success_password(request)
        with open('test_html/cambiar_password.html', 'r') as expected:
            # expected.write(response.content)
            self.assertHTMLEqual(expected.read(), response.content)
        self.assertEqual(response.status_code, 200)

    def test_editar_perfil_varios(self):
        """verifica que se puede ver el perfil, luego cambiar varios datos
        del perfil y que de nuevo pueda ver el perfil notando los cambios
        realizados y siendo el formulario valido
        """
        request = self.factory.get('ver_perfil')
        request.user = self.user1
        response = ver_perfil(request)
        with open("test_index_html/ver_nombre_nahuel.html", 'r') as expected:
            self.assertHTMLEqual(expected.read(), response.content)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('editar_perfil')
        request.user = self.user1
        data = {'nombre': 'Juan',
                'apellido': 'Pardo',
                'edad': '30',
                'telefono': '4899999',
                'pais': 'Argentina',
                'provincia': 'Cordoba',
                'ciudad': 'Cordoba',
                'direccion': 'Sarmiento 666',
                'mail': 'note@hotmail.com',
                'estado_Civil': 'soltero',
                'facebook': 'JuanFB'}
        request.POST = data
        form = ModifyProfile(data)
        self.assertTrue(form.is_valid())

        response = Editar_perfil(request)

        response = ver_perfil(request)
        with open("test_index_html/ver_perfil_editado.html", 'r') as expected:
            self.assertHTMLEqual(expected.read(), response.content)
        self.assertEqual(response.status_code, 200)

    def test_editar_perfil_edad_error(self):
        """
        verifica que al modificar la edad en el perfil ingresando caracteres
        y no numeros, se genera un error
        """
        request = self.factory.post('editar_perfil')
        request.user = self.user1
        data = {'nombre': 'Juan',
                'apellido': 'Palma',
                'edad': 'AAA',
                'telefono': '2323232323232',
                'pais': 'Argentina',
                'provincia': 'Alejandro',
                'ciudad': 'Cordoba',
                'direccion': 'Sarmiento 123',
                'mail': 'n@gmail.com',
                'estado_Civil': 'soltero',
                'facebook': 'nahuel.palma'}
        request.POST = data
        form = ModifyProfile(data)
        self.assertFalse(form.is_valid())

    def test_editar_perfil_mail_error(self):
        """
        verifica que al editar el mail colocando un "mail" sin '@'
        lanza un error obligando a que coloque un '@'
        """
        request = self.factory.post('editar_perfil')
        request.user = self.user1
        data = {'nombre': 'Juan',
                'apellido': 'Palma',
                'edad': '26',
                'telefono': '2323232323232',
                'pais': 'Argentina',
                'provincia': 'Alejandro',
                'ciudad': 'Cordoba',
                'direccion': 'Sarmiento 123',
                'mail': 'ngmail.com',
                'estado_Civil': 'soltero',
                'facebook': 'nahuel.palma'}
        request.POST = data
        form = ModifyProfile(data)
        self.assertFalse(form.is_valid())

    def test_editar_perfil_form_incompleto(self):
        """
        verifica que al editar el perfil, si se dejan datos vacios
        se invalida el formulario y se lanza un error que obliga a ingresar
        datos completos
        """
        request = self.factory.post('editar_perfil')
        request.user = self.user1
        data = {'nombre': 'Juan',
                'apellido': 'Palma',
                'edad': '26',
                'telefono': '2323232323232'}
        request.POST = data
        form = ModifyProfile(data)
        self.assertFalse(form.is_valid())


class VerNotificacionTestCase(UsersTestCase):

    def test_ver_notificacion(self):
        """
        verifica que al ver la notificacion, su estado cambia
        """
        request = self.factory.get('ver_notificacion')
        request.user = self.user1
        response = ver_notificacion(request, self.notificacion.id)
        noti = Notificacion.objects.get(id=self.notificacion.id)
        self.assertEqual(noti.estado, True)
        self.assertEqual(response.status_code, 200)


class RegistrarTestCase(UsersTestCase):

    def test_registrar_form_invalido1(self):
        '''
        Test para un formulario con campos en blanco
        '''
        data = {
            'nombre': "Juan",
            'apellido': "Perez"
        }
        form = UserForm(data)
        self.assertFalse(form.is_valid())

    def test_registrar_form_invalido2(self):
        '''
        Test que verifica que las contraseñas no concuerdan
        '''
        data = {
            'username': "juani",
            'nombre': "Juan",
            'apellido': "Perez",
            'edad': 20,
            'telefono': 123122132131,
            'pais': "Argentina",
            'provincia': "Rio Negro",
            'ciudad': "Bariloche",
            'direccion': "Illia 535",
            'mail': "j@gmail.com",
            'estado_Civil': "casado",
            'facebook': "j.face",
            'password1': 111112,
            'password2': 111111,
        }
        form = UserForm(data)
        self.assertFalse(form.is_valid())


class PasswordTestCase(UsersTestCase):
    """
    Tests que comprueba todo sobre el el cambio de password
    """

    def test_change_password(self):
        """
        Test que comprueba el cambio de contraseña de forma correcta
        """
        data = {'old_password': '123456',
                'new_password1': '1234567',
                'new_password2': '1234567'}
        request = self.factory.get('cambiar_password')
        request.user = self.user
        request.POST = data
        formulario = PasswordChangeForm2(request.user, request.POST)
        self.assertTrue(formulario.is_valid())
        response = cambiar_password(request)
        self.assertEqual(response.status_code, 200)

    def test_change_password_fail_1(self):
        """
        Test que comprueba el cambio de contraseña
        con la vieja contraseña escrita mal
        """
        data = {'old_password': '777777',
                'new_password1': '1234567',
                'new_password2': '1234567'}
        request = self.factory.get('cambiar_password')
        request.user = self.user
        request.POST = data
        formulario = PasswordChangeForm2(request.user, request.POST)
        self.assertFalse(formulario.is_valid())
        response = cambiar_password(request)
        self.assertEqual(response.status_code, 200)

    def test_change_password_fail_2(self):
        """
        Test que comprueba el cambio de contraseña
        con la nueva contraseña escrita mal (menos de 6 caracteres)
        """
        data = {'old_password': '123456',
                'new_password1': '123',
                'new_password2': '123'}
        request = self.factory.get('cambiar_password')
        request.user = self.user
        request.POST = data
        formulario = PasswordChangeForm2(request.user, request.POST)
        self.assertFalse(formulario.is_valid())
        response = cambiar_password(request)
        self.assertEqual(response.status_code, 200)

    def test_change_password_fail_3(self):
        """
        Test que comprueba el cambio de contraseña
        con la nueva contraseña repetida escrita mal
        """
        data = {'old_password': '123456',
                'new_password1': '1234567',
                'new_password2': '1234576'}
        request = self.factory.get('cambiar_password')
        request.user = self.user
        request.POST = data
        formulario = PasswordChangeForm2(request.user, request.POST)
        self.assertFalse(formulario.is_valid())
        response = cambiar_password(request)

    def test_registrar_form_valido(self):
        '''
        Test que evalua un formulario valido
        '''
        data = {
            'username': "juani",
            'nombre': "Juan",
            'apellido': "Perez",
            'edad': 20,
            'telefono': 123122132131,
            'pais': "Argentina",
            'provincia': "Rio Negro",
            'ciudad': "Bariloche",
            'direccion': "Illia 535",
            'mail': "j@gmail.com",
            'estado_Civil': "casado",
            'facebook': "j.face",
            'password1': 111111,
            'password2': 111111,
        }
        form = UserForm(data)
        self.assertTrue(form.is_valid())

    def test_registrar_un_usuario(self):
        """
        verifica que se puede registrar un usuario y que luego al ver el
        perfil del mismo sera correcto respecto a los datos ingresados
        en la registracion
        """
        request = self.factory.post('registrarse')
        data = {
            'username': "juani",
            'nombre': "Juan",
            'apellido': "Perez",
            'edad': 20,
            'telefono': 123122132131,
            'pais': "Argentina",
            'provincia': "Rio Negro",
            'ciudad': "Bariloche",
            'direccion': "Illia 535",
            'mail': "j@gmail.com",
            'estado_Civil': "casado",
            'facebook': "j.face",
            'password1': 111111,
            'password2': 111111,
        }
        form = UserForm(data)

        request.POST = data
        response = Registrarse.as_view()(request, form)
        user = User.objects.get(username="juani")
        request.user = user
        response = ver_perfil(request)
        with open("test_index_html/perfil_registrado.html", 'r') as expected:
            self.assertHTMLEqual(expected.read(), response.content)
        self.assertEqual(response.status_code, 200)
