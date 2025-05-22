from rest_framework import serializers
from .models import Empresa, Cliente, Pedido, PedidoDetalle, CuentaPagada, Proveedor, Compra, CompraDetalle

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

class PedidoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoDetalle
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(),
        source='cliente'
    )
    detalles = PedidoDetalleSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = [
            'id', 'cliente_id', 'fecha', 'precio_total', 'detalles'
        ]

class CuentaPagadaSerializer(serializers.ModelSerializer):
    cuenta_pagar_id = serializers.PrimaryKeyRelatedField(
        queryset=Pedido.objects.all(),
        source='cuenta_pagar'
    )

    class Meta:
        model = CuentaPagada
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

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
        fields = [
            'id', 'proveedor_id', 'fecha', 'monto_total', 'detalles'
        ]
