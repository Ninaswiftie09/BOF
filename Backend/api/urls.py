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
)

router = routers.DefaultRouter()
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')
router.register(r'compras', CompraViewSet, basename='compra')

urlpatterns = [
    path("ping/", ping), 
    path('register/', register_user),  
    path('login/', login_user),  

    # Ventas
    path('ventas/por-fecha/', VentasPorFechaAPIView.as_view(), name='ventas_por_fecha'),
    path('ventas/evolucion/', EvolucionVentasAPIView.as_view(), name='evolucion_ventas'),
    path('ventas/productos-mas-vendidos/', ProductosMasVendidosAPIView.as_view(), name='productos_mas_vendidos'),
    path('ventas/metodos-pago/', MetodosPagoUsadosAPIView.as_view(), name='metodos_pago_usados'),
    path('ventas/detalles/', DetalleVentasAPIView.as_view(), name='detalle_ventas'),

    # Inventario
    path('inventario/agregar-stock/hilo/<int:pk>/', AgregarStockHilo.as_view()),
    path('inventario/agregar-stock/tela/<int:pk>/', AgregarStockTela.as_view()),
    path('inventario/agregar-stock/uniforme/<int:pk>/', AgregarStockUniforme.as_view()),
    path('inventario/quitar-stock/hilo/<int:pk>/', QuitarStockHilo.as_view()),
    path('inventario/quitar-stock/tela/<int:pk>/', QuitarStockTela.as_view()),
    path('inventario/quitar-stock/uniforme/<int:pk>/', QuitarStockUniforme.as_view()),
    path('inventario/agregar-nuevo-hilo/', AgregarNuevoHilo.as_view()),
    path('inventario/agregar-nuevo-tela/', AgregarNuevaTela.as_view()),
    path('inventario/agregar-nuevo-uniforme/', AgregarNuevoUniforme.as_view()),

    # Rutas automáticas de Proveedores y Compras
    path('', include(router.urls)),
]
