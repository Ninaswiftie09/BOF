from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)

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
    cliente_id = models.IntegerField()  # Esto lo podemos mejorar después si tienes una tabla de clientes
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS_VENTA)

    def __str__(self):
        return f"Venta {self.id} - {self.fecha}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.id} de Venta {self.venta.id}"

# tabals para el inventario

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
