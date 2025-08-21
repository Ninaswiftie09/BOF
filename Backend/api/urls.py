from rest_framework import routers
from django.urls import path, include
from .views import (
    ping,
    register_user,
    login_user,
    VentasPorFechaAPIView,
    EvolucionVentasAPIView,
    ProductosMasVendidosAPIView,
    MetodosPagoUsadosAPIView,
    DetalleVentasAPIView,
    AgregarStockHilo,
    AgregarStockTela,
    AgregarStockUniforme,
    QuitarStockHilo,
    QuitarStockTela,
    QuitarStockUniforme,
    AgregarNuevoHilo,
    AgregarNuevaTela,
    AgregarNuevoUniforme,
    ProveedorViewSet,
    CompraViewSet,
    OperacionViewSet,
    OperacionSummaryAPIView,
    TelaListAPIView,
    HiloListAPIView,
    UniformeListAPIView,
    EliminarTela,
    EliminarHilo,
    EliminarUniforme,
    EditarTela,
    EditarHilo,
    EditarUniforme,
    OrdenViewSet,
	HistorialPedidosAPIView,
    OrdenViewSet,
	HistorialPedidosAPIView,
    CrearVentaAPIView,
    EditarVentaAPIView,
    EliminarVentaAPIView,
    CategoriaListAPIView,
    AgregarNuevaCategoria,
    EditarCategoria,
    EliminarCategoria,

)


from clientes.views import ClienteViewSet


router = routers.DefaultRouter()
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')
router.register(r'compras', CompraViewSet, basename='compra')
router.register(r'operaciones', OperacionViewSet, basename='operacion')
router.register(r'ordenes', OrdenViewSet, basename='orden')
router.register(r'clientes', ClienteViewSet, basename='cliente')

urlpatterns = [
    path("ping/", ping, name='ping'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),

    # Ventas
    path('ventas/por-fecha/', VentasPorFechaAPIView.as_view(), name='ventas_por_fecha'),
    path('ventas/evolucion/', EvolucionVentasAPIView.as_view(), name='evolucion_ventas'),
    path('ventas/productos-mas-vendidos/', ProductosMasVendidosAPIView.as_view(), name='productos_mas_vendidos'),
    path('ventas/metodos-pago/', MetodosPagoUsadosAPIView.as_view(), name='metodos_pago_usados'),
    path('ventas/detalles/', DetalleVentasAPIView.as_view(), name='detalle_ventas'),

    # Inventario
    path('inventario/agregar-stock/hilo/<int:pk>/', AgregarStockHilo.as_view(), name='agregar-stock-hilo'),
    path('inventario/agregar-stock/tela/<int:pk>/', AgregarStockTela.as_view(), name='agregar-stock-tela'),
    path('inventario/agregar-stock/uniforme/<int:pk>/', AgregarStockUniforme.as_view(), name='agregar-stock-uniforme'),
    path('inventario/quitar-stock/hilo/<int:pk>/', QuitarStockHilo.as_view(), name='quitar-stock-hilo'),
    path('inventario/quitar-stock/tela/<int:pk>/', QuitarStockTela.as_view(), name='quitar-stock-tela'),
    path('inventario/quitar-stock/uniforme/<int:pk>/', QuitarStockUniforme.as_view(), name='quitar-stock-uniforme'),
    path('inventario/agregar-nuevo-hilo/', AgregarNuevoHilo.as_view(), name='agregar-nuevo-hilo'),
    path('inventario/agregar-nueva-tela/', AgregarNuevaTela.as_view(), name='agregar-nueva-tela'),
    path('inventario/agregar-nuevo-uniforme/', AgregarNuevoUniforme.as_view(), name='agregar-nuevo-uniforme'),

    path('telas/', TelaListAPIView.as_view(), name='listar_telas'),
    path('hilos/', HiloListAPIView.as_view(), name='listar_hilos'),
    path('uniformes/', UniformeListAPIView.as_view(), name='listar_uniformes'),

    path('inventario/eliminar-tela/<int:pk>/', EliminarTela.as_view(), name='eliminar-tela'),
    path('inventario/eliminar-hilo/<int:pk>/', EliminarHilo.as_view(), name='eliminar-hilo'),
    path('inventario/eliminar-uniforme/<int:pk>/', EliminarUniforme.as_view(), name='eliminar-uniforme'),

    path('inventario/editar-tela/<int:pk>/', EditarTela.as_view(), name='editar-tela'),
    path('inventario/editar-hilo/<int:pk>/', EditarHilo.as_view(), name='editar-hilo'),
    path('inventario/editar-uniforme/<int:pk>/', EditarUniforme.as_view(), name='editar-uniforme'),

    # Categorías
    path('categorias/', CategoriaListAPIView.as_view(), name='listar_categorias'),
    path('inventario/agregar-nueva-categoria/', AgregarNuevaCategoria.as_view(), name='agregar-nueva-categoria'),
    path('inventario/editar-categoria/<int:pk>/', EditarCategoria.as_view(), name='editar-categoria'),
    path('inventario/eliminar-categoria/<int:pk>/', EliminarCategoria.as_view(), name='eliminar-categoria'),

    # Operaciones resumen
    path('operaciones/summary/', OperacionSummaryAPIView.as_view(), name='operaciones-summary'),

    # Clientes
    path('ordenes/historial/', HistorialPedidosAPIView.as_view(), name='historial-pedidos'),

    #Ventas
    path("ventas/crear/", CrearVentaAPIView.as_view(), name="crear-venta"),
    path("ventas/editar/<int:pk>/", EditarVentaAPIView.as_view(), name="editar-venta"),
    path("ventas/eliminar/<int:pk>/", EliminarVentaAPIView.as_view(), name="eliminar-venta"),

    # Rutas automáticas
    path('', include(router.urls)),
]
