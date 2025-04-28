from django.contrib import admin
from .models import Categoria, Producto, Venta, DetalleVenta

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
