from django.contrib import admin
from .models import Categoria, Venta, DetalleVenta
from .models import (
    Cliente,
    Proveedor,
    Tela,
    Hilo,
    Uniforme,
    Operacion
)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_cliente', 'nit', 'telefono', 'email', 'estado')
    search_fields = ('nombre', 'codigo_cliente', 'nit')
    list_filter = ('estado',)
    ordering = ('nombre',)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'nit')
    search_fields = ('nombre', 'nit')
    ordering = ('nombre',)

@admin.register(Uniforme)
class UniformeAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'talla', 'color', 'stock', 'precio', 'categoria')
    search_fields = ('tipo', 'color', 'talla')
    list_filter = ('categoria', 'talla')
    list_editable = ('stock', 'precio')
    ordering = ('id',)

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0
    autocomplete_fields = ['producto']

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'no_recibo', 'cliente', 'fecha', 'total', 'estado')
    search_fields = ('no_recibo', 'cliente__nombre')
    list_filter = ('estado', 'fecha', 'metodo_pago')
    inlines = [DetalleVentaInline]
    ordering = ('-fecha',)
    autocomplete_fields = ['cliente']

admin.site.register(Categoria)
admin.site.register(Tela)
admin.site.register(Hilo)
admin.site.register(Operacion)