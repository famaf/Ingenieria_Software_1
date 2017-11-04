# -*- ::coding: utf-8 -*-
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from django.test import Client
from apps.index.models import (PerfilAttributeChar, PerfilAttributeInteger,
                               PerfilAttributeEmail)
from .models import Foto, search, Etiqueta
from .models import Perfil
from .forms import FotoForm, SearchForm
from django.contrib.auth.models import User
from .views import search_image, upload_image, etiquetar_foto, mostrar_perfil


class FotoTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='pepe',
                                             password='123456')
        self.factory = RequestFactory()
        self.Foto1 = Foto.objects.create(
            Ciudad='Cordoba', Pais='Argentina', Lugar='Casa',
            Fecha='2015-01-01', Momento='TA')
        self.etiqueta = Etiqueta.objects.create(
            link=self.Foto1, nombre='pepe')
        self.search = search.objects.create(Lugar='jesus maria',
                                            Momento='Tarde',
                                            Fecha='2015-03-18',
                                            Etiquetado=True)
        self.user2 = User.objects.create_user(username='juano',
                                              password='123456')

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

        self.perfil2 = Perfil.objects.create(usuario=self.user2,
                                             is_admin=False)

    def test_subir_foto(self):
        """
        verifica la vista de upload_image(subir una foto)
        """
        request = self.factory.get('upload_image')
        request.user = self.user
        response = upload_image(request)
        with open("test_html/upload.html", 'r') as expected:
            self.assertEqual(expected.read(), response.content)
        self.assertEqual(response.status_code, 200)

    def test_subir_foto_view(self):
        """
        verifica que se puede ingresar a subir foto
        y que utiliza el template correspondiente
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/fotos/subir_foto/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foto/subir_foto.html')

    def test_not_upload_foto_view(self):
        """
        verifica que no se puede subir una foto con solo el
        argumento Ciudad, lanzando esto un mensaje de error
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/fotos/subir_foto/',
                                    {'Ciudad': 'Cordoba'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foto/subir_foto.html')
        self.assertContains(
            response, "Formulario con error, reingreselo porfavor")

    def test_upload_succes_view(self):
        """
        verifica que subir foto con datos completos y requeridos
        es exitoso
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        f = open("testdata/image.jpg", "r")
        data = ({'Ciudad': "cordoba", 'Pais': "Argentina", 'Lugar': "casa",
                 'Fecha': "11/02/2010", 'Momento': "Ta",
                 'imagen': SimpleUploadedFile(f.name, f.read())})
        response = self.client.post('/fotos/subir_foto/', data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'foto/success_subir.html')
        self.assertContains(response, "Foto subida con éxito")

    def test_FotoForm_empty(self):
        """
        verifica que el formulario vacio para subir foto no es valido
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        data = {}
        foto = FotoForm(data)
        self.assertEquals(False, foto.is_valid())

    def test_FotoForm_onlyoneitem(self):
        """
        verifica que el formulario solo con el dato 'Ciudad' no es valido
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        data = {'Ciudad': "cordoba"}
        foto = FotoForm(data)
        self.assertEquals(False, foto.is_valid())

    def test_FotoForm_ciudad_pais(self):
        """
        verifica que el formulario solo con los datos de 'Ciudad' y 'Pais'
        no es valido
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        data = {'Ciudad': "cordoba", 'Pais': "Argentina"}
        foto = FotoForm(data)
        self.assertEquals(False, foto.is_valid())

    def test_FotoForm_ciudad_pais_fecha_ok(self):
        """
        verifica que el formulario con 'Ciudad', Pais y Fecha
        no es valido
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        data = {'Ciudad': "cordoba", 'Pais': "Argentina",
                'Fecha': "11/02/2015"}
        foto = FotoForm(data)
        self.assertEquals(False, foto.is_valid())

    def test_FotoForm_ciudad_pais_fecha_not_ok(self):
        """
        verifica que el formulario esta completo pero que la fecha
        no es valida
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        data = {'Ciudad': "cordoba", 'Pais': "Argentina",
                'Lugar': "casa", 'Fecha': "11/02/2010", 'Momento': "Ta"}
        foto = FotoForm(data)
        self.assertEquals(False, foto.is_valid())

    def test_FotoForm_less_args(self):
        """
        verifica que el formulario con Pais, Lugar, Fecha y Momento
        no es valido
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        data = ({'Pais': "Argentina", 'Lugar': "casa",
                 'Fecha': "11/02/2010", 'Momento': "Ta", })
        foto = FotoForm(data)
        self.assertEquals(False, foto.is_valid())

    def test_FotoForm_date_invalid(self):
        """
        verifica que la fecha es invalida con el formulario completo
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        f = open("testdata/image.jpg", "r")
        data = ({'Ciudad': "cordoba", 'Pais': "Argentina",
                 'Lugar': "casa", 'Fecha': "11/02/2020", 'Imagen': f, })
        foto = FotoForm(data)
        f.close()
        self.assertEqual(False, foto.is_valid())

    def test_FotoForm_invalid_moment(self):
        """
        verifica que el momento no es valido (Mañana, Tarde o Noche)
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        f = open("testdata/image.jpg", "r")
        data = ({'Ciudad': "cordoba", 'Pais': "Argentina", 'Lugar': "casa",
                 'Fecha': "11/02/2010", 'Momento': "dummy", })
        image = {'imagen': SimpleUploadedFile(f.name, f.read())}
        foto = FotoForm(data, image)
        f.close()
        self.assertEquals(False, foto.is_valid())

    def test_FotoForm_full_success(self):
        """
        verifica que el formulario se ingreso correctamente
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        f = open("testdata/image.jpg", "r")
        data = ({'Ciudad': "cordoba", 'Pais': "Argentina", 'Lugar': "casa",
                 'Fecha': "11/02/2010", 'Momento': "Ta", })
        image = {'imagen': SimpleUploadedFile(f.name, f.read())}
        foto = FotoForm(data, image)
        f.close()
        self.assertEquals(True, foto.is_valid())

    def test_Image_upload_Success(self):
        """
        verifica que la foto se subio con exito
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        f = open("testdata/image.jpg", "r")
        data = ({'Ciudad': "cordoba", 'Pais': "Argentina", 'Lugar': "casa",
                 'Fecha': "11/02/2010", 'Momento': "Ta", })
        response = self.client.post('/fotos/subir_foto/', data)
        f.close()
        self.assertEqual(response.status_code, 200)

# Tests de Buscar Foto
# ====================

    def test_search_image(self):
        """
        verifica la vista de search_image(buscar una foto)
        """
        request = self.factory.get('search_image')
        request.user = self.user
        response = search_image(request)
        with open("test_html/search.html", 'r') as expected:
            self.assertEqual(expected.read(), response.content)
        self.assertEqual(response.status_code, 200)

    def test_buscar_foto_view(self):
        """
        verifica que se puede ingresar a buscar una foto y que
        se utiliza el template correspondiente
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('fotos/buscar_foto')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed('fotos/buscar_foto.html')

    def test_buscar_foto_sin_args_view(self):
        """
        verifica la busqueda de fotos sin argumentos
        """
        response = self.client.post('/fotos/buscar_foto/', {})
        self.assertEqual(response.status_code, 302)

    def test_buscar_foto_con_lugar(self):
        """
        verifica la busqueda solo con el Lugar
        """
        response = self.client.post(
            '/fotos/buscar_foto/', {'Lugar': 'jesus maria'})
        self.assertEqual(response.status_code, 302)

    def test_buscar_foto_con_momento(self):
        """
        verifica la busqueda solo con el Momento
        """
        response = self.client.post('/fotos/buscar_foto/',
                                    {'Momento': 'Tarde'})
        self.assertEqual(response.status_code, 302)

    def test_buscar_foto_con_fecha(self):
        """
        verifica la busqueda solo con el Fecha
        """
        response = self.client.post(
            '/fotos/buscar_foto/', {'Fecha': '2015-03-18'})
        self.assertEqual(response.status_code, 302)

    def test_buscar_foto_con_lugar_y_momento(self):
        """
        verifica la busqueda solo con el Lugar y Momento
        """
        response = self.client.post('/fotos/buscar_foto/',
                                    {'Lugar': 'jesus maria',
                                     'Momento': 'Tarde'})
        self.assertEqual(response.status_code, 302)

    def test_buscar_foto_con_lugar_y_fecha(self):
        """
        verifica la busqueda solo con el Lugar y Fecha
        """
        response = self.client.post('/fotos/buscar_foto/',
                                    {'Lugar': 'jesus maria',
                                     'Fecha': '2015-03-18'})
        self.assertEqual(response.status_code, 302)

    def test_buscar_foto_con_momento_y_fecha(self):
        """
        verifica la busqueda solo con el Momento y Fecha
        """
        response = self.client.post('/fotos/buscar_foto/',
                                    {'Momento': 'Tarde',
                                     'Fecha': '2015-03-18'})
        self.assertEqual(response.status_code, 302)

    def test_buscar_foto_con_fecha_invalida(self):
        """
        verifica que la busqueda con Fecha no valida no se puede
        realizar
        """
        response = self.client.post(
            '/fotos/buscar_foto/', {'Fecha': '2016-03-18'})
        self.assertEqual(response.status_code, 302)

    def test_SearchForm_valid_empty(self):
        """
        verifica que un formulario de busqueda sin datos es valido
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        data = {}
        search = SearchForm(data)
        self.assertEquals(True, search.is_valid())

    def test_SearchForm_valid_lugar(self):
        """
        verifica que un formulario de busqueda solo con Lugar si es valido
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        data = {'Lugar': 'jesus maria'}
        search = SearchForm(data)
        self.assertEquals(True, search.is_valid())

    def test_SearchForm_valid_Fecha(self):
        """
        verifica que el formulario de busqueda solo con Fecha valida es valido
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        data = {'Fecha': '2015-03-18'}
        search = SearchForm(data)
        self.assertEquals(True, search.is_valid())

    def test_SearchForm_valid_Etiquetado(self):
        """
        verifica que el formulario de busqueda con Etiquetado es valido
        """
        response = self.client.post(
            '/', {'username': 'pepe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        data = {'Etiquetado': True}
        search = SearchForm(data)
        self.assertEquals(True, search.is_valid())

# Tests etiquetar foto
# ====================

    def test_etiquetarse(self):
        """
        verifica la vista de etiquetarse
        """
        request = self.factory.get('etiquetar_foto')
        request.user = self.user
        response = upload_image(request)
        with open("test_html/etiquetar.html", 'r') as expected:
            self.assertEqual(expected.read(), response.content)
        self.assertEqual(response.status_code, 200)

    def test_etiquetarse_view(self):
        """
        verifica que se puede ingresar a etiqutarse en una foto
        mostrando su template correspondiente
        """
        response = self.client.post('/', {'username': 'pepe',
                                          'password': '123456'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('fotos/etiquetar_foto')
        self.assertEqual(response.status_code, 404)

    def test_etiqueta_nombre(self):
        """
        verifica que se puede etiquetar con el nombre de usuario
        """
        response = self.client.post('/', {'username': 'pepe',
                                          'password': '123456'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('fotos/etiquetar_foto',
                                   {'nombre': 'pepe'})
        self.assertEqual(response.status_code, 404)

    def test_nombre_corresponde_a_etiqueta(self):
        """
        verifica que el nombre del usuario corresponde con el nombre
        de la etiqueta
        """
        request = self.factory.get('etiquetar_foto')
        request.user = self.user
        response = etiquetar_foto(request, self.Foto1.id)
        etiqueta = Etiqueta.objects.get(id=self.Foto1.id)
        self.assertEqual(etiqueta.nombre, 'pepe')
        self.assertEqual(response.status_code, 200)

# Tests Mostrar_Perfil
# ====================

    def test_mostrar_perfil(self):
        """
        verifica la vista de mostrar perfil
        """
        request = self.factory.post('mostrar_perfil')
        request.user = self.user
        response = mostrar_perfil(request, self.perfil2.usuario)
        with open("test_html/mostrar_perfil.html", 'r') as expected:
            self.assertEqual(expected.read(), response.content)
        self.assertEqual(response.status_code, 200)
