from django.db import models

# =======================
# MODELOS DE CLIENTES
# =======================

class Empresa(models.Model):
    nombre = models.CharField(max_length=255)
    nit = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "clientes_empresa"

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    codigo_cliente = models.CharField(max_length=50, unique=True, editable=False, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=255)
    nit = models.CharField(max_length=50, unique=True, blank=True)
    direccion = models.TextField(blank=True)
    direccion_entrega = models.TextField(blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = "clientes_cliente"

    def save(self, *args, **kwargs):
        if not self.codigo_cliente:
            last_id = Cliente.objects.order_by('-id').first()
            next_id = 1 if not last_id else last_id.id + 1
            self.codigo_cliente = f'CLI{next_id:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    precio_total = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "clientes_pedido"

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre}"


class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    descripcion_producto = models.TextField()
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "clientes_pedidodetalle"

    def total(self):
        return self.cantidad * self.precio_unitario


class CuentaPagada(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto_pagado = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "clientes_cuentapagada"

    def __str__(self):
        return f"Pago {self.id} - {self.cliente.nombre}"


# =======================
# INVENTARIO Y PROVEEDORES
# =======================

class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200, unique=True)
    correo = models.EmailField(max_length=254, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    nit = models.CharField(max_length=50, unique=True, null=True, blank=True)  # 👈 unificado de clientes

    class Meta:
        db_table = "clientes_proveedor"

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    id = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, related_name='compras', on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "clientes_compra"

    def __str__(self):
        return f'Compra {self.id} a {self.proveedor.nombre}'


class CompraDetalle(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    descripcion_producto = models.TextField()
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "clientes_compradetalle"

    def total(self):
        return self.cantidad * self.precio_unitario


# =======================
# INVENTARIO
# =======================

class Material(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class Hilo(Material):
    material = models.CharField(max_length=50)
    codigo_color = models.CharField(max_length=20)
    stock = models.PositiveIntegerField(default=0)


class Tela(Material):
    tipo = models.CharField(max_length=50)
    composicion = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)


class Uniforme(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100)
    talla = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
    material = models.ForeignKey(Tela, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    categoria = models.ForeignKey(
        'Categoria',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uniformes'
    )

    def __str__(self):
        return f"{self.tipo} - {self.talla} - {self.color}"


# =======================
# VENTAS
# =======================

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre



class Venta(models.Model):
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
        ('otro', 'Otro'),
    ]

    ESTADOS_VENTA = [
        ('completada', 'Completada'),
        ('anulada', 'Anulada'),
        ('pendiente', 'Pendiente'),
    ]

    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas')
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS_VENTA)

    no_recibo = models.PositiveIntegerField(unique=True, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.no_recibo:
            last = Venta.objects.exclude(no_recibo__isnull=True).order_by('-no_recibo').first()
            self.no_recibo = 1 if not last else last.no_recibo + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venta {self.id} - {self.fecha}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Uniforme, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.id} de Venta {self.venta.id}"
# =======================
# CONTABILIDAD
# =======================

class Operacion(models.Model):
    TIPO_OPERACION = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_OPERACION)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    concepto = models.TextField(max_length=250)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - Q{self.monto} - {self.fecha.strftime('%d/%m/%Y')}"

    @property
    def tipo_display(self):
        return self.get_tipo_display()

    class Meta:
        ordering = ['-fecha']


# =======================
# ORDENES
# =======================

class Orden(models.Model):
    cliente = models.CharField(max_length=100)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)


class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, related_name='detalles', on_delete=models.CASCADE)
    producto = models.CharField(max_length=100)
    talla = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    tela = models.CharField(max_length=50)
    bordado = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
