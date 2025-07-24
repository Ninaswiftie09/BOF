from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Operacion, Venta, DetalleVenta, Producto
from datetime import date

@receiver(post_save, sender=Operacion)
def crear_venta_desde_operacion(sender, instance, created, **kwargs):
    if created and instance.tipo == 'ingreso':
        
        producto, _ = Producto.objects.get_or_create(
            nombre='Venta desde Operación',
            defaults={
                'precio': instance.monto,
                'descripcion': 'Ingreso registrado automáticamente',
                'categoria_id': 1  
            }
        )

        venta = Venta.objects.create(
            fecha=date.today(),
            cliente_id=0,  
            metodo_pago='efectivo',
            total=instance.monto,
            estado='completada'
        )

        DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            cantidad=1,
            precio_unitario=instance.monto,
            subtotal=instance.monto
        )
