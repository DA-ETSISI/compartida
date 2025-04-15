"""
This module contains the keycloakOIDCAuthenticationBackend class, which is a custom authentication
backend for integrating with Keycloak's OpenID Connect (OIDC) protocol. It extends the
OIDCAuthenticationBackend from the mozilla_django_oidc library to provide additional 
functionality for creating and updating user instances

Models:
    KeycloakOIDCAuthenticationBackend:
        create_user(claims): Creates a new user based on the claims received from Keycloak.
        update_user(user, claims): Updates the attributes of an existing user instance based 
            on the provided claims.
"""
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.core.exceptions import PermissionDenied
from decouple import config

from .models import UsrDa
class keycloakOIDCAuthenticationBackend(OIDCAuthenticationBackend):

    """
    keycloakOIDCAuthenticationBackend is a custom authentication backend that integrates with 
    Keycloak's OpenID Connect (OIDC) protocol. It extends the OIDCAuthenticationBackend to 
    provide additional functionality for creating and updating user instances based on claims 
    received from Keycloak.

    Methods:
        create_user(claims):
            Creates a new user based on the claims received from Keycloak. If a user with the given 
            username already exists, the existing user is returned. Additional user-related data is 
            stored in the `UsrDa` model, and if the user belongs to the 'pdi' group, a `Profesor` 
            instance is also created.



        update_user(user, claims):
            Updates the attributes of an existing user instance based on the provided claims.
    """

    def create_user(self, claims):
        """
        Create a new user based on the claims received from Keycloak.
        This method is called when a new user logs in for the first time.
        Args:
            claims (dict): A dictionary containing user information retrieved from Keycloak.
                Expected keys include:
                - 'preferred_username': The username of the user.
                - 'email': The email address of the user.
                - 'given_name': The first name of the user.
                - 'family_name': The last name of the user.
                - 'groups' (optional): A list of group names the user belongs to.

        Returns:
            User: The created or retrieved User instance.

        Behavior:
            If a user with the given username already exists, the existing user is returned.
            Otherwise, a new user is created with the provided claims.
            Additional user-related data is stored in the `UsrDa` model.
            If the user are PDI create a Profesor instance.
        """
        # Extract the necessary information from the claims
        preferred_username = claims.get('preferred_username')
        email = claims.get('email')
        given_name = claims.get('given_name')
        family_name = claims.get('family_name')
        name = claims.get('name')
        UPMClassCode = claims.get('UPMClassCodes')

        if not config('CODIGO_DE_ESCUELA') in UPMClassCode:
            print("entro aqui")
            raise PermissionDenied("el usuario es de otra escuela")

        if UsrDa.objects.filter(preferred_username=preferred_username).exists():
            return UsrDa.objects.get(preferred_username=preferred_username)

        if  claims.get('UPMClassCodes')[-1] in "DMUPRB":
            es_profesor = True
        else:
            es_profesor = False

        user = UsrDa.objects.create_user(
            preferred_username=preferred_username,
            email=email,
            name=name,
            given_name=given_name,
            family_name=family_name,
            UPMClassCode=UPMClassCode,
            es_profesor=es_profesor,
        )

        # Return the created user
        return user

    def update_user(self, user, claims):
        """
        Updates the attributes of a user instance based on the provided claims.

        Args:
            user (User): The user instance to be updated.
            claims (dict): A dictionary containing user information, typically 
                           extracted from an authentication token. Expected keys 
                           include:
                           - 'preferred_username': The username of the user.
                           - 'email': The email address of the user.
                           - 'given_name': The first name of the user.
                           - 'family_name': The last name of the user.

        Returns:
            User: The updated user instance after saving the changes.
        """

        # Extract the necessary information from the claims
        preferred_username = claims.get('preferred_username')
        email = claims.get('email')
        given_name = claims.get('given_name')
        family_name = claims.get('family_name')
        name = claims.get('name')
        UPMClassCode = claims.get('UPMClassCodes')

        # Update the user instance
        user.preferred_username = preferred_username
        user.email = email
        user.given_name = given_name
        user.family_name = family_name
        user.name = name
        user.UPMClassCode = UPMClassCode

        # Save the updated user instance
        user.save()

        return user
