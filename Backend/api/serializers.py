from rest_framework import serializers
from .models import Categoria, Producto, Venta, DetalleVenta
from .models import Hilo, Tela, Uniforme
from .models import Proveedor, Compra, Operacion
from clientes.models import Compra as CompraCliente


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
        
#para proveedores
        
class CompraSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Compra
        fields = ['id', 'proveedor', 'fecha', 'descripcion', 'monto_total']
        read_only_fields = ['id', 'fecha']



class ProveedorSerializer(serializers.ModelSerializer):
    compras = CompraSerializer(many=True, read_only=True)

    class Meta:
        model = Proveedor
        fields = ['id', 'nombre', 'correo', 'telefono', 'direccion', 'compras']
        read_only_fields = ['id']

#inventario

class HiloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hilo
        fields = ['id', 'material', 'codigo_color','color', 'stock', 'nombre', 'codigo', 'descripcion']

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
        fields = ['id', 'tipo', 'talla', 'color','stock', 'material']

    def update(self, instance, validated_data):
        if 'stock' in validated_data:
            instance.stock = validated_data['stock']
        instance.save()
        return instance

class OperacionSerializer(serializers.ModelSerializer):
    fecha = serializers.DateTimeField(
        format="%d/%m/%Y %H:%M",  
        read_only=True
    )
    tipo_display = serializers.CharField(
        source='get_tipo_display',
        read_only=True
    )

    class Meta:
        model = Operacion
        fields = ['id', 'tipo', 'tipo_display', 'monto', 'concepto', 'fecha']
        read_only_fields = ['fecha']

    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a cero.")
        return value




