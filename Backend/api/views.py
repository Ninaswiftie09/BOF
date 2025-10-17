import json
import string
import random
from decimal import Decimal

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.utils import timezone
from django.core.cache import cache

from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsAdminOrEmpleado


from .utils.roles import get_role




from .models import (
    Empresa, Cliente, Pedido, PedidoDetalle, CuentaPagada,
    Categoria, Compra, DetalleVenta, Hilo, Operacion, Orden,
    Producto, Proveedor, Tela, Uniforme, Venta, CompraDetalle
)

from .serializers import (
    EmpresaSerializer, ClienteSerializer, PedidoSerializer, PedidoDetalleSerializer,
    CuentaPagadaSerializer, CategoriaSerializer, CompraSerializer, DetalleVentaSerializer,
    HiloSerializer, OperacionSerializer, OrdenSerializer, ProductoSerializer, ProveedorSerializer,
    TelaSerializer, UniformeSerializer, VentaSerializer, VentaDetalleSerializer, CompraDetalleSerializer
)

# =======================
# CLIENTES
# =======================

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('nombre')
    serializer_class = ClienteSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nombre', 'nit', 'email']



class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer


class PedidoDetalleViewSet(viewsets.ModelViewSet):
    queryset = PedidoDetalle.objects.all()
    serializer_class = PedidoDetalleSerializer


class CuentaPagadaViewSet(viewsets.ModelViewSet):
    queryset = CuentaPagada.objects.all()
    serializer_class = CuentaPagadaSerializer


# =======================
# INVENTARIO Y PROVEEDORES
# =======================

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all().order_by('nombre')
    serializer_class = ProveedorSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nombre', 'correo', 'telefono']


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all().order_by('-fecha')
    serializer_class = CompraSerializer


class CompraDetalleViewSet(viewsets.ModelViewSet):
    queryset = CompraDetalle.objects.all()
    serializer_class = CompraDetalleSerializer


# =======================
# INVENTARIO CRUD EXTRA
# =======================

class TelaListAPIView(ListAPIView):
    queryset = Tela.objects.all()
    serializer_class = TelaSerializer


class HiloListAPIView(ListAPIView):
    queryset = Hilo.objects.all()
    serializer_class = HiloSerializer


class UniformeListAPIView(ListAPIView):
    queryset = Uniforme.objects.all()
    serializer_class = UniformeSerializer


class EliminarTela(APIView):
    def delete(self, request, pk):
        tela = get_object_or_404(Tela, pk=pk)
        tela.delete()
        return Response({'mensaje': 'Tela eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)


class EliminarHilo(APIView):
    def delete(self, request, pk):
        hilo = get_object_or_404(Hilo, pk=pk)
        hilo.delete()
        return Response({'mensaje': 'Hilo eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)


class EliminarUniforme(APIView):
    def delete(self, request, pk):
        uniforme = get_object_or_404(Uniforme, pk=pk)
        uniforme.delete()
        return Response({'mensaje': 'Uniforme eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)


class EditarTela(APIView):
    def put(self, request, pk):
        tela = get_object_or_404(Tela, pk=pk)
        serializer = TelaSerializer(tela, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Tela actualizada correctamente', 'tela': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)


class EditarHilo(APIView):
    def put(self, request, pk):
        hilo = get_object_or_404(Hilo, pk=pk)
        serializer = HiloSerializer(hilo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Hilo actualizado correctamente', 'hilo': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)


class EditarUniforme(APIView):
    def put(self, request, pk):
        uniforme = get_object_or_404(Uniforme, pk=pk)
        serializer = UniformeSerializer(uniforme, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Uniforme actualizado correctamente', 'uniforme': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TelaViewSet(viewsets.ModelViewSet):
    queryset = Tela.objects.all().order_by('id')
    serializer_class = TelaSerializer

class HiloViewSet(viewsets.ModelViewSet):
    queryset = Hilo.objects.all().order_by('id')
    serializer_class = HiloSerializer

class UniformeViewSet(viewsets.ModelViewSet):
    queryset = Uniforme.objects.all().order_by('id')
    serializer_class = UniformeSerializer


# =======================
# AUTENTICACIÓN
# =======================

def ping(request):
    return JsonResponse({"message": "pong"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    u = request.user
    return Response({
        "id": u.id,
        "email": u.email,
        "first_name": getattr(u, "first_name", ""),
        "role": get_role(u),             # <-- "admin" | "empleado" | "ninguno"
        "group_ids": list(u.groups.values_list("id", flat=True)),  # por si quieres verlo
    })
    
    
@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            role = data.get('role')
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

            if not first_name or not last_name or not email or not role:
                return JsonResponse({'message': 'Faltan datos requeridos'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'El correo ya está registrado'}, status=400)

            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=email,
                email=email,
            )
            user.set_password(password)
            user.save()

            # Roles
            admin_group, _ = Group.objects.get_or_create(name='Administrador')
            employee_group, _ = Group.objects.get_or_create(name='Empleado')

            if role == 'Administrador':
                user.groups.add(admin_group)
            elif role == 'Empleado':
                user.groups.add(employee_group)
            else:
                return JsonResponse({'message': 'Rol no válido'}, status=400)

            # Email bienvenida
            subject = 'Bienvenido a Abril Uniformes y Bordados'
            html_message = render_to_string('emails/bienvenida.html', {
                'nombre': first_name,
                'correo': email,
                'contraseña': password
            })
            send_mail(subject, '', None, [email], html_message=html_message, fail_silently=False)

            return JsonResponse({'message': 'Usuario creado y correo enviado'}, status=201)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Método no permitido'}, status=405)


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'message': 'El correo y la contraseña son requeridos'}, status=400)

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Inicio de sesión exitoso'}, status=200)
            return JsonResponse({'message': 'Credenciales incorrectas'}, status=400)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Método no permitido'}, status=405)


@csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'message': 'Correo requerido'}, status=400)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'message': 'No existe un usuario con ese correo'}, status=404)

            new_password = get_random_string(length=8)
            user.set_password(new_password)
            user.save()

            subject = 'Restablecimiento de contraseña - Abril Uniformes'
            html_message = render_to_string('emails/restablecer.html', {
                'nombre': user.first_name,
                'correo': user.email,
                'contraseña': new_password
            })
            send_mail(subject, '', None, [user.email], html_message=html_message)

            return JsonResponse({'message': 'Correo enviado con la nueva contraseña'}, status=200)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Método no permitido'}, status=405)
    
@csrf_exempt
def send_verification_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'message': 'Correo requerido'}, status=400)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'message': 'No existe un usuario con ese correo'}, status=404)

            code = get_random_string(length=6, allowed_chars='0123456789')
            cache.set(f'verify_code_{email}', code, timeout=180)  # 3 minutos

            html_message = f"""
            <h2>Hola {user.first_name}</h2>
            <p>Este es tu código de verificación para restablecer tu contraseña:</p>
            <h3>{code}</h3>
            <p>El código es válido por 3 minutos.</p>
            """

            send_mail('Código de verificación', '', None, [email], html_message=html_message)

            return JsonResponse({'message': 'Código enviado'}, status=200)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Método no permitido'}, status=405)



# =======================
# CONTABILIDAD
# =======================

class OperacionViewSet(viewsets.ModelViewSet):
    queryset = Operacion.objects.all()
    serializer_class = OperacionSerializer


class OperacionSummaryAPIView(APIView):
    def get(self, request):
        ingresos = Operacion.objects.filter(tipo='ingreso').aggregate(total=Sum('monto'))['total'] or 0
        egresos = Operacion.objects.filter(tipo='egreso').aggregate(total=Sum('monto'))['total'] or 0
        total_ops = Operacion.objects.count()

        data = {
            'ingresos': float(ingresos),
            'egresos': float(egresos),
            'balance': float(ingresos - egresos),
            'total': total_ops
        }
        return Response(data, status=status.HTTP_200_OK)


# =======================
# ORDENES
# =======================

class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer


class HistorialPedidosAPIView(ListAPIView):
    queryset = Orden.objects.all().order_by('-fecha')
    serializer_class = OrdenSerializer


# =======================
# VENTAS
# =======================

class CrearVentaAPIView(APIView):
    @transaction.atomic
    def post(self, request):
        detalles_data = request.data.pop("detalles", [])

        venta_serializer = VentaSerializer(data=request.data)
        if not venta_serializer.is_valid():
            return Response(venta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        venta = venta_serializer.save(total=0)
        total = Decimal("0")

        for item in detalles_data:
            producto = get_object_or_404(Uniforme, pk=item["producto"])
            cantidad = int(item["cantidad"])
            precio_unitario = Decimal(item.get("precio_unitario", 0))
            subtotal = cantidad * precio_unitario

            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=subtotal,
            )
            total += subtotal

        venta.total = total
        venta.save()
        return Response(VentaSerializer(venta).data, status=status.HTTP_201_CREATED)


class EditarVentaAPIView(APIView):
    @transaction.atomic
    def put(self, request, pk):
        venta = get_object_or_404(Venta, pk=pk)
        detalles_data = request.data.pop("detalles", [])

        venta_serializer = VentaSerializer(venta, data=request.data, partial=True)
        if not venta_serializer.is_valid():
            return Response(venta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        venta = venta_serializer.save(total=Decimal("0"))
        venta.detalles.all().delete()
        total = Decimal("0")

        for item in detalles_data:
            producto = get_object_or_404(Uniforme, pk=item["producto"])
            cantidad = int(item["cantidad"])
            precio_unitario = Decimal(item.get("precio_unitario", 0))
            subtotal = cantidad * precio_unitario

            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=subtotal,
            )
            total += subtotal

        venta.total = total
        venta.save()
        return Response(VentaSerializer(venta).data, status=status.HTTP_200_OK)


class EliminarVentaAPIView(APIView):
    def delete(self, request, pk):
        venta = get_object_or_404(Venta, pk=pk)
        venta.delete()
        return Response({"mensaje": "Venta eliminada correctamente"}, status=status.HTTP_204_NO_CONTENT)


class VentaReciboAPIView(RetrieveAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaDetalleSerializer


# =======================
# REPORTES
# =======================

class VentasPorFechaAPIView(APIView):
    def get(self, request):
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        ventas = Venta.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        total_ventas = ventas.aggregate(total=Sum('total'))['total'] or 0
        numero_facturas = ventas.count()

        serializer = VentaSerializer(ventas, many=True)
        return Response({
            'total_ventas': total_ventas,
            'numero_facturas': numero_facturas,
            'ventas': serializer.data
        }, status=status.HTTP_200_OK)


class EvolucionVentasAPIView(APIView):
    def get(self, request):
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        ventas = Venta.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        ventas_por_dia = ventas.annotate(dia=TruncDate('fecha')).values('dia').annotate(total=Sum('total')).order_by('dia')
        return Response(list(ventas_por_dia), status=status.HTTP_200_OK)


class ProductosMasVendidosAPIView(APIView):
    def get(self, request):
        productos = DetalleVenta.objects.values('producto__nombre').annotate(total_vendido=Sum('cantidad')).order_by('-total_vendido')[:5]
        return Response(list(productos), status=status.HTTP_200_OK)


class MetodosPagoUsadosAPIView(APIView):
    def get(self, request):
        metodos = Venta.objects.values('metodo_pago').annotate(cantidad=Count('metodo_pago')).order_by('-cantidad')
        return Response(list(metodos), status=status.HTTP_200_OK)


class DetalleVentasAPIView(APIView):
    def get(self, request):
        cliente = request.query_params.get('cliente')
        fecha = request.query_params.get('fecha')
        nit = request.query_params.get('nit')

        ventas = Venta.objects.all()

        if cliente:
            ventas = ventas.filter(cliente__nombre__icontains=cliente)
        if fecha:
            ventas = ventas.filter(fecha=fecha)
        if nit:
            ventas = ventas.filter(cliente__nit__icontains=nit)

        serializer = VentaSerializer(ventas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# =======================
# CATEGORÍAS
# =======================

class CategoriaListAPIView(APIView):
    def get(self, request):
        categorias = Categoria.objects.all().order_by('nombre')
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AgregarNuevaCategoria(APIView):
    def post(self, request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            categoria = serializer.save()
            return Response(
                {"message": "Categoría creada", "categoria": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditarCategoria(APIView):
    def put(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        serializer = CategoriaSerializer(categoria, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Categoría actualizada", "categoria": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EliminarCategoria(APIView):
    def delete(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.delete()
        return Response({"mensaje": "Categoría eliminada correctamente"}, status=status.HTTP_204_NO_CONTENT)