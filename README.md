# CompartiDA

Compartida repositorio de apuntes.
Por [@Pdrj09](https://github.com/Pdrj09) con ❤️ para [@DA-ETSISI](https://github.com/DA-ETSISI)

## Instalación

Usa el gestor de paquetes de python [pip](https://pip.pypa.io/en/stable/) para descargar los paquetes de django y mozilla django oidc.

```bash
pip install django, mozilla_django_oidc, decouple
```

Clona el repositorio.
```bash
git clone https://github.com/Pdrj09/compartida.git
cd compartida/
```

Es importante generar un archivo .env en la raíz del del proyecto:

```.env
DJANGO_SECRECT_KEY={Clave secreta de la app}
DEBUG={True/False no usar nunca True en producción}
ALLOWED_HOST={Host permitidas para el acceso a la web, localhost,127.0.0.1 si es en local}
KC_CLIENT_ID={ID del cliente del keycloak}
KC_CLIENT_SECRET={Secreto del cliente del keycloak}
KC_REALM={Realm usado por el keycloak}
KC_HOST={Host del keycloak}
KC_ALGO={algoritmo usado por keycloak}
```

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
