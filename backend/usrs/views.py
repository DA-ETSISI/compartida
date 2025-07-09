from rest_framework.permissions import IsAuthenticated #type: ignore[import]
from rest_framework import viewsets #type: ignore[import]
from rest_framework.decorators import api_view, permission_classes #type: ignore[import]
from rest_framework.response import Response #type: ignore[import]
from .serializers import UsrDaSerializer

from usrs.models import UsrDa


@api_view(['GET'])
def current_user(request):
    user = request.user

    if not user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)

    data = {
        'id': user.id,
        'username': user.preferred_username,
        'email': user.email,
        'is_staff': user.is_staff,
        # otros campos que quieras exponer
    }
    return Response(data)
