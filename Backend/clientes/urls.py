from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmpresaViewSet, ClienteViewSet, PedidoViewSet, PedidoDetalleViewSet,
    CuentaPagadaViewSet, ProveedorViewSet, CompraViewSet, CompraDetalleViewSet
)

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'pedidos-detalle', PedidoDetalleViewSet)
router.register(r'pagos', CuentaPagadaViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'compras', CompraViewSet)
router.register(r'compras-detalle', CompraDetalleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
