"""
This module defines the models for a Django application that manages academic subjects, 
degrees, users, and professors. It includes the following models:

Models:
    Titulacion: Represents an academic degree or program with associated subjects and credits.
    Asignatura: Represents an academic subject with attributes for name, credits, and semester.
    UsrDa: Represents a user in the system with extended attributes and permissions.
    Profesor: Represents a professor with assigned subjects.

Models Managers:
    UsrDaManager: Custom manager for creating users and superusers with additional logic.

Each model includes detailed attributes and relationships to represent the academic structure 
and user roles within the system.
"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from titulaciones.models import Titulacion, Asignatura

class UsrDaManager(BaseUserManager):
    """
    Clase para gestionar la creación de usuarios y superusuarios.
    """
    def create_user(self, preferred_username, email, es_profesor=False, **extra_fields):
        """
        Creates and returns a new user with the specified username, email, and additional fields.

        Args:
            preferred_username (str): SIU username for the new user.
            email (str): The email address for the new user.
            es_profesor (bool, optional): Indicates whether the user is a professor. 
                Defaults to False.
            **extra_fields: Additional fields to include when creating the user.

        Returns:
            user: The created user instance.

        Notes:
            If `es_profesor` is True, a `Profesor` instance is created and associated 
                with the user.
            The user's password is set to an unusable state.
            The user instance is saved to the database.
        """

        email = self.normalize_email(email)
        user = self.model(
            preferred_username=preferred_username,
            email=self.normalize_email(email),
            es_profesor=es_profesor,
            **extra_fields
        )
        user.set_unusable_password()
        user.save()
        if es_profesor:
            profesor = Profesor.objects.create(user=user)
            profesor.save()

        return user

    def create_superuser(self, preferred_username, email, **extra_fields):
        """
        Creates and returns a superuser with the given preferred username, email, 
        and additional fields.

        This method ensures that the created user has the 'is_staff' and 
        'is_superuser' flags set to True.

        Args:
            preferred_username (str): The preferred username for the superuser.
            email (str): The email address for the superuser.
            **extra_fields: Additional fields to set on the superuser.

        Returns:
            User: The created superuser instance.
        """


        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(preferred_username, email, **extra_fields)

class UsrDa(AbstractBaseUser, PermissionsMixin):
    """
    UsrDa Model

    This model represents a user in the system with extended attributes and permissions.

    Attributes:
        preferred_username (CharField): The preferred username of the user. Must be unique.
        email (CharField): The email address of the user. Must be unique.
        name (CharField): The full name of the user.
        given_name (CharField): The given name (first name) of the user.
        family_name (CharField): The family name (last name) of the user.
        UPMClassCode (CharField): A code provided by Keycloak (siu) for the user.
        titulacion (ForeignKey): A foreign key to the `Titulacion` model, 
            representing the user's degree program.
        recuento_subidas (int): The count of uploads made by the user. Defaults to 0.
        recuento_visualizaciones (int): The count of views made by the user. Defaults to 0.
        es_profesor (bool): A flag indicating whether the user is a professor. Defaults to False.
        is_staff (bool): A flag indicating whether the user has staff privileges. Defaults to False.
        is_active (bool): A flag indicating whether the user account is active. Defaults to True.
        password (CharField): The password for the user. Can be blank or null.

    Notes:
        Meta:
            USERNAME_FIELD: 
                Specifies the field used as the unique identifier for authentication, 
                set to `preferred_username`.
            
            REQUIRED_FIELDS: 
                A list of fields that are required when creating a user,
                including `email`, `UPMClassCode`, `name`, 
                `given_name`, and `family_name`.

        Manager:
            objects: Custom manager for the `UsrDa` model, provided by `UsrDaManager`.
    """

    preferred_username = models.CharField(max_length=255, unique=True, default="")
    email = models.EmailField(unique=True, default="")
    name = models.CharField(max_length=255, default="")
    given_name = models.CharField(max_length=255, default="")

    # Códigos upm dado por keycloak (siu)
    codigos_escuela = models.JSONField(default=list)
    tipo_usuario = models.JSONField(default=list)

    titulacion = models.ForeignKey(Titulacion, on_delete=models.SET_NULL, blank= True, null=True)
    recuento_subidas = models.IntegerField(default=0)
    recuento_visualizaciones = models.IntegerField(default=0)
    es_profesor = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    password = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = "preferred_username"
    REQUIRED_FIELDS = [
                        "email",
                        "UPMClassCode",
                        "name",
                        "given_name",
                        "family_name",
                        ]

    objects = UsrDaManager()

class Profesor(models.Model):
    """
    Represents a Profesor model that associates a user with their assigned subjects.

    Attributes:
        user (OneToOneField): A one-to-one relationship linking the Profesor to a UsrDa instance.
        asignaturas (ManyToManyField): A many-to-many relationship linking the Profesor 
            to multiple Asignatura instances.
    """

    user = models.OneToOneField(UsrDa, on_delete=models.CASCADE)
    asignaturas = models.ManyToManyField(Asignatura, blank=True)
