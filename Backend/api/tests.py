from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase
from rest_framework import status
from .models import (
    Tela, Hilo, Uniforme, 
    Venta, DetalleVenta, 
    Operacion, Proveedor, Compra
)
from .serializers import TelaSerializer

# Configuración inicial para pruebas
class BaseTest(APITestCase):
    def setUp(self):
        # Crear grupos y usuario de prueba para autenticación
        Group.objects.create(name='Administrador')
        self.user = User.objects.create_user(
            username='test@example.com',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)

        # Datos de prueba para inventario
        self.tela_data = {
            "nombre": "Tela de algodón",
            "codigo": "T001",
            "tipo": "Algodón",
            "composicion": "100% algodón",
            "stock": 10,
            "color": "Azul"
        }

# -------------------------------------------------------------------
# 1. Pruebas para Endpoints Básicos
# -------------------------------------------------------------------
class PingTest(TestCase):
    def test_ping_response(self):
        response = self.client.get(reverse('ping'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "pong"})

# -------------------------------------------------------------------
# 2. Pruebas de Autenticación
# -------------------------------------------------------------------
class AuthTests(BaseTest):
    def test_register_user(self):
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "new@example.com",
            "password": "password123",
            "role": "Administrador"
        }
        response = self.client.post(reverse('register'), data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        response = self.client.post(reverse('login'), {
            "email": "test@example.com",
            "password": "password123"
            }, format='json')
        self.assertEqual(response.status_code, 200)



# -------------------------------------------------------------------
# 3. Pruebas de Inventario (Telas, Hilos, Uniformes)
# -------------------------------------------------------------------
class InventarioTests(BaseTest):
    def test_crear_tela(self):
        response = self.client.post(
            reverse('agregar-nueva-tela'),
            self.tela_data,
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tela.objects.count(), 1)

    def test_agregar_stock_tela(self):
        tela = Tela.objects.create(**self.tela_data)
        response = self.client.patch(
            reverse('agregar-stock-tela', kwargs={'pk': tela.pk}),
            {"cantidad": 5},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tela.objects.get(pk=tela.pk).stock, 15)

# -------------------------------------------------------------------
# 4. Pruebas de Ventas
# -------------------------------------------------------------------
class VentasTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.venta_data = {
            "fecha": "2023-01-01",
            "cliente_id": 1,
            "metodo_pago": "efectivo",
            "total": 100.00,
            "estado": "completada"
        }

    def test_ventas_por_fecha(self):
        Venta.objects.create(**self.venta_data)
        response = self.client.get(
            reverse('ventas_por_fecha') + '?fecha_inicio=2023-01-01&fecha_fin=2023-01-31'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_ventas'], 100.00)

# -------------------------------------------------------------------
# 5. Pruebas de Operaciones Contables
# -------------------------------------------------------------------
class OperacionTests(BaseTest):
    def test_summary_operaciones(self):
        Operacion.objects.create(tipo='ingreso', monto=500.00, concepto="Venta")
        response = self.client.get(reverse('operaciones-summary'))
        self.assertEqual(response.json()['ingresos'], 500.00)

# -------------------------------------------------------------------
# 6. Pruebas de Proveedores
# -------------------------------------------------------------------
class ProveedorTests(BaseTest):
    def test_buscar_proveedor(self):
        Proveedor.objects.create(nombre="Proveedor ABC")
        response = self.client.get(reverse('proveedor-list') + '?search=ABC')
        self.assertContains(response, "Proveedor ABC")