from rest_framework import serializers
from .models import Venta

class VentaSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = Venta
        fields = ['id', 'producto', 'cantidad', 'precio_unitario', 'total', 'fecha']

    def get_total(self, obj):
        return obj.total()
