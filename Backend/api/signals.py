from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Operacion, Venta

@receiver(post_save, sender=Operacion)
def crear_venta_desde_operacion(sender, instance, created, **kwargs):
    if created and instance.tipo == 'ingreso':
        # Crear la venta basada en la información disponible
        Venta.objects.create(
            producto='Venta desde Operación',
            cliente='Desconocido',
            cantidad=1,
            precio_unitario=instance.monto,
            total=instance.monto,
            metodo_pago='Efectivo', 
        )
