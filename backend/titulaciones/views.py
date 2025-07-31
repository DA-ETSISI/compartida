from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Asignatura, Titulacion
from .serializers import AsignaturaSerializer, TitulacionSerializer


class AsignaturaRetrieveViewSet(RetrieveModelMixin, GenericViewSet):

    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = AsignaturaSerializer


class AsignaturaListViewSet(ListModelMixin, GenericViewSet):

    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = AsignaturaSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["nombre", "curso", "optativa", "grados"]

    queryset = Asignatura.objects.all()


class TitulacionListViewSet(ListModelMixin, GenericViewSet):
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = TitulacionSerializer

    queryset = Titulacion.objects.all()
