from django.contrib import admin
from .models import Categoria, Venta, DetalleVenta

admin.site.register(Categoria)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
