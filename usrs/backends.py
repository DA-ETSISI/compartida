"""
Atuh backend for Keycloak OIDC
"""
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth.models import User
from .models import UsrDa, Profesor

class keycloakOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    """
    Custom authentication backend for Keycloak OIDC.
    This backend handles the authentication process and user creation
    or update based on the claims received from Keycloak.
    """

    def create_user(self, claims):
        """
        Create a new user based on the claims received from Keycloak.
        """
        # Extract the necessary information from the claims
        username = claims.get('preferred_username')
        email = claims.get('email')
        first_name = claims.get('given_name')
        last_name = claims.get('family_name')

        if User.objects.filter(username=username).exists():
            return User.objects.get(username=username)

        # Create a new user
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        groups = claims.get('groups', [])
        profesor:bool = 'pdi' in groups

        UsrDa.objects.create(
            user=user,
            titulacion=None,  # Set to None or assign a default value
            recuento_subidas=0,
            recuento_descargas=0,
            es_profesor=profesor
        )

        if profesor:
            # Create a Profesor instance if the user is a professor
            Profesor.objects.create(user=user, asignaturas=None)

        # Return the created user
        return user

    def update_user(self, user, claims):
        """
        Update an existing user based on the claims received from Keycloak.
        """ 
        # Extract the necessary information from the claims
        username = claims.get('preferred_username')
        email = claims.get('email')
        first_name = claims.get('given_name')
        last_name = claims.get('family_name')

        # Update the user instance
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        # Save the updated user instance
        user.save()

        return user
