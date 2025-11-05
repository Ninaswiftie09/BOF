# api/management/commands/populate_db.py

import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Cliente, Uniforme, Venta, DetalleVenta, Tela, Hilo, Categoria # Importa todos los modelos necesarios

class Command(BaseCommand):
    help = 'Populates the database with a large volume of test data.'

    # @transaction.atomic asegura que si algo falla, toda la operación se revierta.
    @transaction.atomic
    def handle(self, *args, **kwargs):
        fake = Faker('es_ES') # Usamos el generador en español
        self.stdout.write(self.style.SUCCESS('--- Starting database population ---'))

        # Limpia datos existentes para evitar duplicados si se corre de nuevo
        self.stdout.write('Deleting old data...')
        DetalleVenta.objects.all().delete()
        Venta.objects.all().delete()
        Cliente.objects.all().delete()
        Uniforme.objects.all().delete()
        Tela.objects.all().delete()
        Categoria.objects.all().delete()
        self.stdout.write('Old data deleted.')

        # --- Generar Categorías ---
        num_categorias = 5
        categorias_creadas = []
        for _ in range(num_categorias):
            cat = Categoria.objects.create(nombre=fake.word().capitalize())
            categorias_creadas.append(cat)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_categorias} categories.'))

        # --- Generar Telas (necesarias para los Uniformes) ---
        num_telas = 20
        telas_creadas = []
        for _ in range(num_telas):
            tela = Tela.objects.create(
                nombre=f"Tela {fake.word()}",
                tipo=random.choice(['Algodón', 'Poliéster', 'Mezcla', 'Lino']),
                composicion=f"{random.randint(50, 100)}% Algodón",
                color=fake.color_name(),
                codigo=fake.unique.ean(length=8),
                stock=random.randint(100, 1000)
            )
            telas_creadas.append(tela)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_telas} telas.'))

        # --- Generar Uniformes ---
        num_uniformes = 200
        uniformes_creados = []
        for _ in range(num_uniformes):
            uniforme = Uniforme.objects.create(
                tipo=random.choice(['Filipina', 'Pantalón Quirúrgico', 'Bata de Laboratorio', 'Pijama Médica']),
                talla=random.choice(['XS', 'S', 'M', 'L', 'XL']),
                color=fake.color_name(),
                material=random.choice(telas_creadas),
                stock=random.randint(10, 100),
                categoria=random.choice(categorias_creadas)
            )
            uniformes_creados.append(uniforme)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_uniformes} uniform products.'))

        # --- Generar Clientes ---
        num_clientes = 1000
        clientes_a_crear = []
        for _ in range(num_clientes):
            clientes_a_crear.append(Cliente(
                nombre=fake.name(),
                nit=fake.unique.ssn(),
                direccion=fake.address(),
                telefono=fake.phone_number(),
                email=fake.email(),
            ))
        Cliente.objects.bulk_create(clientes_a_crear)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_clientes} clients.'))

        # --- Generar Ventas y Detalles ---
        self.stdout.write('Generating sales and details (this may take a moment)...')
        cliente_ids = list(Cliente.objects.values_list('id', flat=True))
        
        num_ventas = 5000
        for i in range(num_ventas):
            venta_total = 0
            # Crea la cabecera de la venta
            venta = Venta.objects.create(
                cliente_id=random.choice(cliente_ids),
                fecha=fake.date_between(start_date='-2y', end_date='today'),
                metodo_pago=random.choice(['efectivo', 'tarjeta', 'transferencia']),
                estado='completada',
                total=0 # Se actualizará después
            )
            
            detalles_a_crear_para_esta_venta = []
            num_detalles_por_venta = random.randint(1, 4)
            for _ in range(num_detalles_por_venta):
                uniforme_elegido = random.choice(uniformes_creados)
                cantidad = random.randint(1, 5)
                # Precio aleatorio ya que no está en el modelo Uniforme
                precio_unitario = round(random.uniform(75.0, 450.0), 2)
                subtotal = cantidad * precio_unitario
                venta_total += subtotal
                
                detalles_a_crear_para_esta_venta.append(DetalleVenta(
                    venta=venta,
                    producto=uniforme_elegido,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=subtotal
                ))
            
            # Crea los detalles para esta venta
            DetalleVenta.objects.bulk_create(detalles_a_crear_para_esta_venta)
            
            # Actualiza el total de la venta
            venta.total = round(venta_total, 2)
            venta.save()
            
            # Imprime un progreso para saber que no se ha colgado
            if (i + 1) % 500 == 0:
                self.stdout.write(f'  ... {i + 1} / {num_ventas} sales created.')

        self.stdout.write(self.style.SUCCESS(f'Successfully created sales and details.'))
        self.stdout.write(self.style.SUCCESS('--- Database population complete! ---'))