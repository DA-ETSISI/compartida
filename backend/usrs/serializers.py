from rest_framework import serializers

from usrs.models import UsrDa, Profesor, Asignatura, Titulacion

class GenericUserDASerializer(serializers.ModelSerializer):
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
        fields = [
                    'id',
                    'preferred_username',
                    'email',
                    'name',
                    'es_profesor',
                    'is_staff',
                    'is_active',
                    'titulacion'
                ]