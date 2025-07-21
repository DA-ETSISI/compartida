from rest_framework import serializers
from .models import Apunte

class ApunteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apunte
        exclude = ['apoyo_docente', 'visualizaciones', 'visible']
