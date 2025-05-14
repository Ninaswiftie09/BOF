from django.urls import path
from .views import (
    ping,
    register_user,
    login_user,
    VentasPorFechaAPIView,
    EvolucionVentasAPIView,
    ProductosMasVendidosAPIView,
    MetodosPagoUsadosAPIView,
    DetalleVentasAPIView
)
urlpatterns = [
    path("ping/", ping), 
    path('register/', register_user),  
    path('login/', login_user),
    
    path('ventas/por-fecha/', VentasPorFechaAPIView.as_view(), name='ventas_por_fecha'),
    path('ventas/evolucion/', EvolucionVentasAPIView.as_view(), name='evolucion_ventas'),
    path('ventas/productos-mas-vendidos/', ProductosMasVendidosAPIView.as_view(), name='productos_mas_vendidos'),
    path('ventas/metodos-pago/', MetodosPagoUsadosAPIView.as_view(), name='metodos_pago_usados'),
    path('ventas/detalles/', DetalleVentasAPIView.as_view(), name='detalle_ventas'),
]
