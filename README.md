# CompartiDA

Compartida repositorio de apuntes.
Por [@Pdrj09](https://github.com/Pdrj09) con ❤️ para [@DA-ETSISI](https://github.com/DA-ETSISI).

## Instalación

Usa el gestor de paquetes de Python [pip](https://pip.pypa.io/en/stable/) para descargar los paquetes de Django y Mozilla Django OIDC.

```bash
pip install django mozilla_django_oidc decouple
```

Clona el repositorio.
```bash
git clone https://github.com/Pdrj09/compartida.git
cd compartida/
```

Es importante generar un archivo .env en la raíz del proyecto:

```.env
DJANGO_SECRET_KEY={Clave secreta de la app}
DEBUG={True/False no usar nunca True en producción}
ALLOWED_HOST={Hosts permitidos para el acceso a la web; localhost,127.0.0.1 si es en local}
KC_CLIENT_ID={ID del cliente de Keycloak}
KC_CLIENT_SECRET={Secreto del cliente de Keycloak}
KC_REALM={Realm usado por Keycloak}
KC_HOST={Host de Keycloak}
KC_ALGO={Algoritmo usado por Keycloak}
CODIGO_DE_ESCUELA={Código de tu escuela, 61 en caso de la ETSISI}
```

Aplica las migraciones de la base de datos.
```bash
python3 manage.py migrate
```

Inicia el servidor.
```bash
python3 manage.py runserver
```

## Ayúdanos 

Todas las colaboraciones son bienvenidas. Si quieres hacer una colaboración pequeña, haz un pull request. Si quieres hacer una modificación grande, por favor, pon una issue.

Por favor, respeta las reglas de Pylint a la hora de colaborar.
