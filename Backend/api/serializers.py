from rest_framework import serializers
from .models import Categoria, Producto, Venta, DetalleVenta
from .models import Categoria, Hilo, Tela, Uniforme
from .models import Proveedor, Compra, Operacion
from clientes.models import Compra as CompraCliente
from .models import Orden, DetalleOrden




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
        read_only_fields = ['total']
        
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
    material_nombre = serializers.SerializerMethodField(read_only=True)
    categoria_nombre = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Uniforme
        fields = [
            'id', 'tipo', 'talla', 'color', 'stock',
            'material', 'material_nombre',
            'categoria', 'categoria_nombre',
        ]
    def get_material_nombre(self, obj):
        return obj.material.nombre if obj.material else None

    def get_categoria_nombre(self, obj):
        return obj.categoria.nombre if obj.categoria else None

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


# Nueva Orden Clientes

class DetalleOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleOrden
        exclude = ['orden']
        extra_kwargs = {
            'orden': {'required': False}
        }

class OrdenSerializer(serializers.ModelSerializer):
    detalles = DetalleOrdenSerializer(many=True)

    class Meta:
        model = Orden
        fields = '__all__'

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        orden = Orden.objects.create(**validated_data)
        for item in detalles_data:
            DetalleOrden.objects.create(orden=orden, **item)
        return orden

    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles', [])

        # Actualiza campos simples
        instance.cliente = validated_data.get('cliente', instance.cliente)
        instance.fecha = validated_data.get('fecha', instance.fecha)
        instance.total = validated_data.get('total', instance.total)
        instance.save()

        # Elimina detalles existentes
        instance.detalles.all().delete()

        # Crea nuevos detalles
        for item in detalles_data:
            DetalleOrden.objects.create(orden=instance, **item)

        return instance