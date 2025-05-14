from rest_framework import serializers
from .models import Categoria, Producto, Venta, DetalleVenta
from .models import Hilo, Tela, Uniforme

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

#inventario

class HiloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hilo
        fields = ['id', 'material', 'codigo_color', 'stock', 'nombre', 'codigo', 'descripcion']

    def update(self, instance, validated_data):
        if 'stock' in validated_data:
            instance.stock = validated_data['stock']
        instance.save()
        return instance


class TelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tela
        fields = ['id', 'tipo', 'composicion', 'color', 'stock', 'nombre', 'codigo', 'descripcion']

    def update(self, instance, validated_data):
        if 'stock' in validated_data:
            instance.stock = validated_data['stock']
        instance.save()
        return instance

class UniformeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uniforme
        fields = ['id', 'tipo', 'talla', 'color', 'material']

    def update(self, instance, validated_data):
        if 'stock' in validated_data:
            instance.stock = validated_data['stock']
        instance.save()
        return instance


