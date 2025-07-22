from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions, status

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
        user = self.request.user

        user.recuento_subidas += 1
        user.save()

        serializer.save(user=self.request.user)

class ApunteRetrieveViewSet(RetrieveModelMixin, GenericViewSet):
    """
    A viewset for retrieving Apunte instances.
    This viewset provides read-only access to Apunte objects. Access is restricted to authenticated users.
    Staff users can retrieve all Apunte instances, while non-staff users can only retrieve those marked as visible.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetApunteSerializer
    visibility_serializer_class = VisibilitySerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Apunte.objects.all()
        return Apunte.objects.filter(visible=True)

    def get_serializer_class(self):
        if self.action == 'set_visibility':
            return self.visibility_serializer_class
        return super().get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user

        user.recuento_visualizaciones += 1
        instance.visualizaciones += 1
        
        user.save()
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], url_path="visibility")
    @extend_schema(
        request=VisibilitySerializer,
        responses={200: VisibilitySerializer},
        description="Cambiar la visibilidad de un apunte"
    )
    def set_visibility(self, request, id=None):
        if not request.user.is_staff:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        apunte = self.get_object()
        serializer = self.get_serializer(apunte, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

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
