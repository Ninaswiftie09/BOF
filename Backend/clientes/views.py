from rest_framework import viewsets
from .models import Empresa, Cliente, Pedido, PedidoDetalle, CuentaPagada, Proveedor, Compra, CompraDetalle
from .serializers import (
    EmpresaSerializer, ClienteSerializer, PedidoSerializer, PedidoDetalleSerializer,
    CuentaPagadaSerializer, ProveedorSerializer, CompraSerializer, CompraDetalleSerializer
)

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class PedidoDetalleViewSet(viewsets.ModelViewSet):
    queryset = PedidoDetalle.objects.all()
    serializer_class = PedidoDetalleSerializer

class CuentaPagadaViewSet(viewsets.ModelViewSet):
    queryset = CuentaPagada.objects.all()
    serializer_class = CuentaPagadaSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

class CompraDetalleViewSet(viewsets.ModelViewSet):
    queryset = CompraDetalle.objects.all()
    serializer_class = CompraDetalleSerializer
