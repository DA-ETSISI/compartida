from rest_framework import serializers

from usrs.models import UsrDa, Profesor, Asignatura, Titulacion

class TitulacionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Titulacion model, which represents a degree in the system.

    Attributes:
        nombre (CharField): The name of the degree.
        codigo (CharField): The unique code of the degree.
    """
    
    class Meta:
        model = Titulacion
        fields = '__all__'  # Include all fields from Titulacion model

class AsignaturaSerializer(serializers.ModelSerializer):
    """
    Serializer for the Asignatura model, which represents a subject in the system.
    
    Attributes:
        nombre (CharField): The name of the subject.
        codigo (CharField): The unique code of the subject.
        titulacion (ForeignKey): Foreign key to the Titulacion model, representing the degree associated with the subject.
    """
    
    class Meta:
        model = Asignatura
        fields = '__all__'  # Include all fields from Asignatura model

class ProfesorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profesor model, which represents a professor in the system.
    
    Attributes:
        user (UsrDa): The user associated with the professor.
        asignaturas (ManyToManyField): List of subjects assigned to the professor.
    """
    
    class Meta:
        model = Profesor
        fields = '__all__'  # Include all fields from Profesor model

class UsrDaSerializer(serializers.ModelSerializer):
    """
    Serializer for the UsrDa model, which represents a user in the system.
    
    Attributes:
        preferred_username (CharField): The unique username of the user.
        email (EmailField): The email address of the user.
        name (CharField): The full name of the user.
        given_name (CharField): The first name of the user.
        codigos_escuela (JSONField): List of school codes associated with the user.
        tipo_usuario (JSONField): List of user types associated with the user.
        titulacion (ForeignKey): Foreign key to the Titulacion model, representing the user's degree.
        recuento_subidas (IntegerField): Count of uploads made by the user.
        recuento_visualizaciones (IntegerField): Count of views made by the user.
        es_profesor (BooleanField): Indicates if the user is a professor.
        is_staff (BooleanField): Indicates if the user is a staff member.
        is_active (BooleanField): Indicates if the user account is active.
        password (CharField): The password for the user. Can be blank or null.
    """
    
    class Meta:
        model = UsrDa
        fields = '__all__'  # Include all fields from UsrDa model