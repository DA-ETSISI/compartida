# CompartiDA

Compartida repositorio de apuntes.
Por [@Pdrj09](https://github.com/Pdrj09) con ❤️ para [@DA-ETSISI](https://github.com/DA-ETSISI)

## Instalación

Usa el gestor de paquetes de python [pip](https://pip.pypa.io/en/stable/) para descargar los paquetes de django y mozilla django oidc.

```bash
pip install django, mozilla_django_oidc
```

Clona el repositorio.
```bash
git clone https://github.com/Pdrj09/compartida.git
cd compartida/
```

Es importante generar el `setings.py` del proyecto y configurar [mozilla django oidc](https://mozilla-django-oidc.readthedocs.io/en/stable/index.html)

Make the migrations of the db.
```bash
python3 manage.py migrate
```

Run server.
```bash
python3 manage.py runserver
```

## Ayudanos

Todas las colaboraciones son bienvenidas, si quieres hacer una colaboración pequeña haz un pull request, si quieres hacer una modificación grande por favor pon una issue.

Por favor respeta las pylint a la hora de colaborar.
