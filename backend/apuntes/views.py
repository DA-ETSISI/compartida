from rest_framework.viewsets import ModelViewSet
from .models import Apunte
from .serializers import ApunteSerializer

class ApunteViewSet(ModelViewSet):
    """
    ViewSet for managing Apunte instances.

    Provides CRUD operations for Apunte model.
    """
    queryset = Apunte.objects.all()
    serializer_class = ApunteSerializer

    def perform_create(self, serializer):
        """
        Override to set the user when creating a new Apunte instance.
        """
        serializer.save(user=self.request.user)