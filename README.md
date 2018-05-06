# Welcome to Potatoe ![alt text](https://en.gravatar.com/userimage/97652074/bb1065c2d4711c097727f2920112fae7.jpg "Potatoe")

FotoLink
========
Fotolink consiste en un sistema capaz de conectar a personas que estuvieron presentes en un lugar en un determinado momento.
El usuario se registra ingresando algunos datos personales, luego con su usuario y password, se logueara en el sistema.
A partir de ese momento podra subir sus fotografias, etiquetarse en otras fotos, ver perfil de los usuarios etiquetados en las fotos.


## ¿Cómo arranco / instalo el proyecto en mi máquina?


#### Provisionamiento:

#### Instalar las siguientes dependencias, en un sistema basado en Debian (como Ubuntu), se puede hacer:

    $ sudo apt-get install git libxml2-dev libxslt1-dev python-pip python-dev virtualenv

#### Crear y activar un nuevo [virtualenv](https://virtualenv.pypa.io/en/stable/). Recomiendo usar [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/). Se puede instalar así:

    $ sudo pip install virtualenvwrapper

Y luego agregando la siguiente línea al final del archivo `.bashrc`:

    export WORKON_HOME=$HOME/.virtualenvs
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python
    export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
    [[ -s "/usr/local/bin/virtualenvwrapper.sh" ]] && source "/usr/local/bin/virtualenvwrapper.sh"

Para crear y activar nuestro virtualenv:

    $ mkvirtualenv fotolink

#### Clonar el repositorio:

    $ git clone https://github.com/marioferreyra/Potatoe.git

#### Instalarlo:

    $ cd Potatoe/src/FotoLink/env_install
    $ pip install -r requirements.txt

#### Activar el entorno virtual:

    $ workon fotolink

#### Generar y llenar la base de datos:

    $ python manage.py migrate


#### Activar el server local:

    $ python manage.py runserver

#### Luego en el navegador podras acceder a FotoLink:

    http://127.0.0.1:8000/
    ó
    http://localhost:8000/

#### Desactivar el entorno virtual

    $ deactivate

## Test, Test and more Test
Para correr los test de Fotolink

    $ cd Potatoe/src/FotoLink/
    $ python manage.py test

## Contribuyendo con Potatoe

Existen varias maneras de contribuir Potatoe y FotoLink, reportando bugs, codeando 
algunas nuevas apps para mejorar las funcionalidades de FotoLink. Para ello deberas
hacer pull request para que nuestros revisores lo aprueben, debera pasar el standard
pep8, docstring, y tener sus test correspondientes.

Una vez tu pull request sea aprobado tu código pasará a la inmortalidad de
Potatoe :)

## Proximas Tareas
* Historias relacionadas a la amistad entre usuarios.
* Deploy del proyecto en un server real ?
