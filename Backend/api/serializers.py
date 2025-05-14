from rest_framework import serializers
from .models import Categoria, Producto, Venta, DetalleVenta
from .models import Inventario, Hilo, Tela, Uniforme

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = DetalleVenta
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = '__all__'


class InventarioSerializer(serializers.ModelSerializer):
    descripcion = serializers.SerializerMethodField()
    
    class Meta:
        model = Inventario
        fields = ['id', 'tipo', 'objeto_id', 'cantidad', 'fecha_actualizacion', 'descripcion']
    
    def get_descripcion(self, obj):
        return str(obj.content_object)
