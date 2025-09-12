from rest_framework import routers
from django.urls import path, include

from .views import (
    # --- AUTH ---
    ping, register_user, login_user, forgot_password,

    # --- CLIENTES ---
    EmpresaViewSet, ClienteViewSet, PedidoViewSet, PedidoDetalleViewSet, CuentaPagadaViewSet,

    # --- INVENTARIO Y PROVEEDORES ---
    ProveedorViewSet, CompraViewSet, CompraDetalleViewSet,
    TelaListAPIView, HiloListAPIView, UniformeListAPIView,
    EliminarTela, EliminarHilo, EliminarUniforme,
    EditarTela, EditarHilo, EditarUniforme,

    # --- CATEGORÍAS ---
    CategoriaListAPIView, AgregarNuevaCategoria, EditarCategoria, EliminarCategoria,

    # --- CONTABILIDAD ---
    OperacionViewSet, OperacionSummaryAPIView,

    # --- ORDENES ---
    OrdenViewSet, HistorialPedidosAPIView,

    # --- VENTAS ---
    CrearVentaAPIView, EditarVentaAPIView, EliminarVentaAPIView, VentaReciboAPIView,

    # --- REPORTES ---
    VentasPorFechaAPIView, EvolucionVentasAPIView, ProductosMasVendidosAPIView, MetodosPagoUsadosAPIView, DetalleVentasAPIView,
)

router = routers.DefaultRouter()

# --- CLIENTES ---
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'pedidos', PedidoViewSet, basename='pedido')
router.register(r'pedidos-detalle', PedidoDetalleViewSet, basename='pedido-detalle')
router.register(r'pagos', CuentaPagadaViewSet, basename='cuenta-pagada')

# --- INVENTARIO Y PROVEEDORES ---
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')
router.register(r'compras', CompraViewSet, basename='compra')
router.register(r'compras-detalle', CompraDetalleViewSet, basename='compra-detalle')

# --- CONTABILIDAD ---
router.register(r'operaciones', OperacionViewSet, basename='operacion')

# --- ORDENES ---
router.register(r'ordenes', OrdenViewSet, basename='orden')


urlpatterns = [
    # --- AUTH ---
    path("ping/", ping, name='ping'),
    path("register/", register_user, name='register'),
    path("login/", login_user, name='login'),
    path("forgot-password/", forgot_password, name='forgot-password'),

    # --- VENTAS ---
    path("ventas/crear/", CrearVentaAPIView.as_view(), name="crear-venta"),
    path("ventas/editar/<int:pk>/", EditarVentaAPIView.as_view(), name="editar-venta"),
    path("ventas/eliminar/<int:pk>/", EliminarVentaAPIView.as_view(), name="eliminar-venta"),
    path("ventas/<int:pk>/recibo/", VentaReciboAPIView.as_view(), name="venta-recibo"),

    # --- REPORTES ---
    path("ventas/por-fecha/", VentasPorFechaAPIView.as_view(), name="ventas-por-fecha"),
    path("ventas/evolucion/", EvolucionVentasAPIView.as_view(), name="evolucion-ventas"),
    path("ventas/productos-mas-vendidos/", ProductosMasVendidosAPIView.as_view(), name="productos-mas-vendidos"),
    path("ventas/metodos-pago/", MetodosPagoUsadosAPIView.as_view(), name="metodos-pago"),
    path("ventas/detalles/", DetalleVentasAPIView.as_view(), name="detalle-ventas"),

    # --- INVENTARIO ---
    path("telas/", TelaListAPIView.as_view(), name="listar-telas"),
    path("hilos/", HiloListAPIView.as_view(), name="listar-hilos"),
    path("uniformes/", UniformeListAPIView.as_view(), name="listar-uniformes"),

    path("inventario/eliminar-tela/<int:pk>/", EliminarTela.as_view(), name="eliminar-tela"),
    path("inventario/eliminar-hilo/<int:pk>/", EliminarHilo.as_view(), name="eliminar-hilo"),
    path("inventario/eliminar-uniforme/<int:pk>/", EliminarUniforme.as_view(), name="eliminar-uniforme"),

    path("inventario/editar-tela/<int:pk>/", EditarTela.as_view(), name="editar-tela"),
    path("inventario/editar-hilo/<int:pk>/", EditarHilo.as_view(), name="editar-hilo"),
    path("inventario/editar-uniforme/<int:pk>/", EditarUniforme.as_view(), name="editar-uniforme"),

    # --- CATEGORÍAS ---
    path("categorias/", CategoriaListAPIView.as_view(), name="listar-categorias"),
    path("inventario/agregar-nueva-categoria/", AgregarNuevaCategoria.as_view(), name="agregar-nueva-categoria"),
    path("inventario/editar-categoria/<int:pk>/", EditarCategoria.as_view(), name="editar-categoria"),
    path("inventario/eliminar-categoria/<int:pk>/", EliminarCategoria.as_view(), name="eliminar-categoria"),

    # --- CONTABILIDAD ---
    path("operaciones/summary/", OperacionSummaryAPIView.as_view(), name="operaciones-summary"),

    # --- ORDENES ---
    path("ordenes/historial/", HistorialPedidosAPIView.as_view(), name="historial-pedidos"),

    # --- RUTAS AUTOMÁTICAS ---
    path("", include(router.urls)),
]
