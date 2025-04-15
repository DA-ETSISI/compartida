"""
Modelos de la app usrs.
"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class Asignatura(models.Model):
    """
    Modelo para almacenar asignaturas.

    atributos:
    - nombre: Nombre de la asignatura.
    - créditos: Número de créditos de la asignatura.

    """
    nombre = models.CharField(max_length=255)
    creditos = models.IntegerField()

class Titulacion(models.Model):
    """
    Modelo para almacenar titulación.

    atributos:
    - nombre: Nombre de la carrera.

    """
    nombre = models.CharField(max_length=255)

class UsrDaManager(BaseUserManager):
    """
    Clase para gestionar la creación de usuarios y superusuarios.
    """
    def create_user(self, preferred_username, email, es_profesor=False, **extra_fields):
        """
        Metodo para crear un usuario normal.
        """
        email = self.normalize_email(email)
        user = self.model(
            preferred_username=preferred_username,
            email=self.normalize_email(email),
            **extra_fields
        )
        if es_profesor:
            Profesor.objects.create(user=user, asignaturas=None)
        user.set_unusable_password()
        user.save()

        return user

    def create_superuser(self, preferred_username, email, **extra_fields):
        """
        Metodo para crear un superusuario.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(preferred_username, email, **extra_fields)        

class UsrDa(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado que hereda de AbstractUser => django.user + usrs.user.
    Se pueden añadir campos adicionales si es necesario.
    atributos:
    - Titulación (titulacion_id): Relación con el modelo titulación.
    - Recuento de subidas (int): Número de apuntes subidos por el usuario.
    - Recuento de descargas (int): Número de apuntes descargados por el usuario.
    - Es profesor (Bool): Booleano que indica si el usuario es profesor o no.
    """

    preferred_username = models.CharField(max_length=255, unique=True, default="")
    email = models.EmailField(unique=True, default="")
    given_name = models.CharField(max_length=255, default="")
    family_name = models.CharField(max_length=255, default="")
    UPMClassCode = models.CharField(max_length=255, default="")
    name = models.CharField(max_length=255, default="")
    titulacion = models.ForeignKey(Titulacion, on_delete=models.SET_NULL, null=True)
    recuento_subidas = models.IntegerField(default=0)
    recuento_descargas = models.IntegerField(default=0)
    es_profesor = models.BooleanField(default=False)

    password = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'preferred_username'

    objects = UsrDaManager()

class Profesor(models.Model):
    """
    Modelo para almacenar profesores.
    atributos:
    - user (user_id => int): Usuario que subió el apunte => enlace a la tabla user, Si se borra el
        usuario se borran los apuntes.
    - asignaturas (asignatura_id => int): Asignaturas impartidas por el profesor => enlace a la
        tabla asignatura, Si se borra la asignatura se pone a null.
    """
    user = models.OneToOneField(UsrDa, on_delete=models.CASCADE)
    asignaturas = models.ManyToManyField(Asignatura)
