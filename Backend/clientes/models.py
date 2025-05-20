from django.db import models

# Tabla de Empresas
class Empresa(models.Model):
    nombre = models.CharField(max_length=255)
    nit = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

# Tabla de Clientes
class Cliente(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=255)
    contacto = models.CharField(max_length=255, blank=True)
    nit = models.CharField(max_length=50, unique=True, blank=True)
    direccion = models.TextField(blank=True)
    direccion_entrega = models.TextField(blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    estado = models.BooleanField(default=True)  # True = Activo, False = Inactivo

    def __str__(self):
        return self.nombre

# Tabla de Pedidos (Ventas)
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    precio_total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre}"

# Detalle de Pedidos
class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    descripcion_producto = models.TextField()
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    def total(self):
        return self.cantidad * self.precio_unitario

# Tabla de Cuentas Pagadas
class CuentaPagada(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto_pagado = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Pago {self.id} - {self.cliente.nombre}"

# Tabla de Proveedores
class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    contacto = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    nit = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

# Tabla de Compras a Proveedores
class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Compra #{self.id} - {self.proveedor.nombre}"

# Detalle de Compras
class CompraDetalle(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    descripcion_producto = models.TextField()
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    def total(self):
        return self.cantidad * self.precio_unitario
