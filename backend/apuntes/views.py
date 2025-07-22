from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import *
from .models import Apunte

class ApunteCreateViewSet(CreateModelMixin, GenericViewSet):
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

@extend_schema(
    description="Read-only access to Apuntes. Staff see all. Others see only visible ones"
)
class ApunteRetrieveViewSet(RetrieveModelMixin, GenericViewSet):
    """
    A viewset for retrieving Apunte instances.
    This viewset provides read-only access to Apunte objects. Access is restricted to authenticated users.
    Staff users can retrieve all Apunte instances, while non-staff users can only retrieve those marked as visible.
    Attributes:
        permission_classes (list): Permissions required to access this viewset.
        serializer_class (Serializer): Serializer used for Apunte instances.
        lookup_field (str): Field used to look up Apunte instances.
    Methods:
        get_queryset(): Returns a queryset of Apunte objects based on the user's permissions.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    serializer_class = GetApunteSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Apunte.objects.all()
        return Apunte.objects.filter(visible=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.visualizaciones += 1
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(
    operation_id="List Apuntes",
    description="Retrieve apuntes filtered by visible, user, fecha, etc.",
    parameters=[
        OpenApiParameter("titulo", str, description="Filter by title of the Apunte"),
        OpenApiParameter("asignatura", int, description="Filter by asignatura ID"),
        OpenApiParameter("user", int, description="Filter by userDA ID"),
    ]
)
class ApunteListViewSet(ListModelMixin, GenericViewSet):
    """
    A viewset for listing Apunte instances.
    This viewset provides a list of Apunte objects, allowing users to see available study notes.
    Attributes:
        permission_classes (list): Permissions required to access this viewset.
        serializer_class (Serializer): Serializer used for Apunte instances.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    serializer_class = ListApunteSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['titulo', 'asignatura', 'user']

    def get_queryset(self):
        return Apunte.objects.filter(visible=True).order_by('-visualizaciones', '-fecha_creacion')

