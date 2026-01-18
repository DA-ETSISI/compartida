from django.db import models


# Create your models here.
class Titulacion(models.Model):
    """
    Represents an academic degree or program.

    Attributes:
        nombre (CharFiled): The name of the degree.
        codigo (CharField): A unique code for the degree, limited to 10 characters.
    """

    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=10, default="", unique=True)
    tipo = models.CharField(max_length=10, default="GRA", blank=True)


class Asignatura(models.Model):
    """
    Model representing an academic subject.

    Attributes:
        nombre (CharField): The name of the subject, with a maximum length of 255
            characters.
        creditos (IntegerField): The number of credits assigned to the subject.
        curso (IntegerField): The course number in which the subject is taught.
        optativa (BooleanField): Indicates whether the subject is optional (True) or
            mandatory (False). Defaults to False.
        grados (ManyToManyField): A many-to-many relationship with the Titulacion model,
            representing the degrees associated with the subject. This field is
            required.
    """

    codigo = models.CharField(max_length=20, primary_key=True, unique=True, default="")

    nombre = models.CharField(max_length=255)
    creditos = models.IntegerField(default=6)
    curso = models.IntegerField(default=0)
    optativa = models.BooleanField(default=False)

    grados = models.ManyToManyField(Titulacion, symmetrical=False, blank=False)
