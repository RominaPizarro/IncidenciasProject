from rest_framework import serializers
from .models import Requerimiento


class RequerimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requerimiento
        fields = ('id', 'codigo', 'fecha_registro', 'descripcion', 'observaciones',
                  'usuario_reporta', 'area', 'usuario_asignado', 'estado')
