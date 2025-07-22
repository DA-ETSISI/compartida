from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions

from .serializers import *
from .models import Apunte

class LoadApunteViewSet(CreateModelMixin, GenericViewSet):
    """
    ViewSet for managing Apunte instances.

    Provides CRUD operations for Apunte model.
    """
    permission_classes = [permissions.IsAuthenticated]

    queryset = Apunte.objects.all()
    serializer_class = LoadApunteSerializer

    def perform_create(self, serializer):
        """
        Override to set the user when creating a new Apunte instance.
        """
        serializer.save(user=self.request.user)

class GetApunteViewSet(RetrieveModelMixin, GenericViewSet):
    """
    ViewSet for retrieving Apunte instances.

    Provides read-only access to Apunte model.
    """
    permission_classes = [permissions.IsAuthenticated]

    queryset = Apunte.objects.all()
    serializer_class = LoadApunteSerializer

    def get_serializer_class(self):
        """
        Use different serializer for retrieving Apunte instances.
        """
        return GetApunteSerializer