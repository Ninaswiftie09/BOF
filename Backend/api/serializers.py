from rest_framework import serializers
from .models import (
    Empresa, Cliente, Pedido, PedidoDetalle, CuentaPagada,
    Categoria, Hilo, Tela, Uniforme, Producto, Venta, DetalleVenta,
    Proveedor, Compra, CompraDetalle, Operacion, Orden, DetalleOrden
)

# =======================
# CLIENTES
# =======================

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    empresa_id = serializers.PrimaryKeyRelatedField(
        queryset=Empresa.objects.all(),
        source='empresa',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Cliente
        fields = [
            'id',
            'codigo_cliente',
            'empresa_id',
            'nombre',
            'contacto',
            'nit',
            'direccion',
            'direccion_entrega',
            'telefono',
            'email',
            'estado'
        ]
        read_only_fields = ['codigo_cliente']


class PedidoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoDetalle
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(),
        source='cliente'
    )
    detalles = PedidoDetalleSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'cliente_id', 'cliente_nombre', 'fecha', 'precio_total', 'detalles']


class CuentaPagadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaPagada
        fields = '__all__'


# =======================
# VENTAS
# =======================

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'categoria', 'categoria_nombre', 'precio', 'descripcion']


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


class VentaDetalleSerializer(serializers.ModelSerializer):
    cliente = serializers.SerializerMethodField()
    detalles = DetalleVentaSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = ['id', 'fecha', 'cliente', 'metodo_pago', 'total', 'estado', 'detalles', 'no_recibo']

    def get_cliente(self, obj):
        if obj.cliente:
            return ClienteSerializer(obj.cliente).data
        return None


# =======================
# PROVEEDORES Y COMPRAS
# =======================

class CompraDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompraDetalle
        fields = '__all__'


class CompraSerializer(serializers.ModelSerializer):
    proveedor_id = serializers.PrimaryKeyRelatedField(
        queryset=Proveedor.objects.all(),
        source='proveedor'
    )
    detalles = CompraDetalleSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ['id', 'proveedor_id', 'fecha', 'descripcion', 'monto', 'detalles']
        read_only_fields = ['id', 'fecha']


class ProveedorSerializer(serializers.ModelSerializer):
    compras = CompraSerializer(many=True, read_only=True)

    class Meta:
        model = Proveedor
        fields = ['id', 'nombre', 'correo', 'telefono', 'direccion', 'nit', 'compras']
        read_only_fields = ['id']


# =======================
# INVENTARIO
# =======================

class HiloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hilo
        fields = ['id', 'material', 'codigo_color', 'color', 'stock', 'nombre', 'codigo', 'descripcion']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class TelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tela
        fields = ['id', 'tipo', 'composicion', 'color', 'stock', 'nombre', 'codigo', 'descripcion']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
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
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# =======================
# CONTABILIDAD
# =======================

class OperacionSerializer(serializers.ModelSerializer):
    fecha = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = Operacion
        fields = ['id', 'tipo', 'tipo_display', 'monto', 'concepto', 'fecha']
        read_only_fields = ['fecha']

    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a cero.")
        return value


# =======================
# ORDENES
# =======================

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

        instance.cliente = validated_data.get('cliente', instance.cliente)
        instance.fecha = validated_data.get('fecha', instance.fecha)
        instance.total = validated_data.get('total', instance.total)
        instance.save()

        instance.detalles.all().delete()

        for item in detalles_data:
            DetalleOrden.objects.create(orden=instance, **item)

        return instance
