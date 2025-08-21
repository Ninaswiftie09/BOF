# Estándar de Python
import json

# Django
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.db import transaction
from decimal import Decimal

# DRF
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# App local
from .models import Proveedor, Compra
from .serializers import ProveedorSerializer, CompraSerializer

from .models import Categoria, Venta, DetalleVenta, Hilo, Tela, Uniforme, Operacion, Producto, Orden
from .serializers import (
    CategoriaSerializer,
    VentaSerializer,
    HiloSerializer,
    TelaSerializer,
    UniformeSerializer,
    OperacionSerializer,
    OrdenSerializer,
)

from django.utils.decorators import method_decorator


from rest_framework.generics import ListAPIView
from .models import Tela
from .serializers import TelaSerializer
from clientes.models import Compra

#categorias
from .models import Categoria
from .serializers import CategoriaSerializer

# Nueva Orden
from .models import Orden
from .serializers import OrdenSerializer
from rest_framework.generics import ListAPIView
from clientes.views import ClienteViewSet



class TelaListAPIView(ListAPIView):
    queryset = Tela.objects.all()
    serializer_class = TelaSerializer

def ping(request):
    return JsonResponse({"message": "pong"})

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password')
            role = data.get('role') 

            if not first_name or not last_name or not email or not password or not role:
                return JsonResponse({'message': 'Faltan datos requeridos'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'El correo ya está registrado'}, status=400)

            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=email,
                password=make_password(password),
                email=email,
            )
            user.save()

            # Crear o obtener los grupos
            admin_group, created = Group.objects.get_or_create(name='Administrador')
            employee_group, created = Group.objects.get_or_create(name='Empleado')

            if role == 'Administrador':
                user.groups.add(admin_group)
            elif role == 'Empleado':
                user.groups.add(employee_group)
            else:
                return JsonResponse({'message': 'Rol no válido'}, status=400)

            return JsonResponse({'message': 'Usuario creado exitosamente'}, status=201)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
    else:
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

            else:
                return JsonResponse({'message': 'Credenciales incorrectas'}, status=400)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

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
        serializer = TelaSerializer(tela, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Tela actualizada correctamente', 'tela': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditarHilo(APIView):
    def put(self, request, pk):
        hilo = get_object_or_404(Hilo, pk=pk)
        serializer = HiloSerializer(hilo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Hilo actualizado correctamente', 'hilo': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditarUniforme(APIView):
    def put(self, request, pk):
        uniforme = get_object_or_404(Uniforme, pk=pk)
        serializer = UniformeSerializer(uniforme, data=request.data, partial=True)  # 👈 partial=True
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Uniforme actualizado correctamente', 'uniforme': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TelaListAPIView(APIView):
    def get(self, request):
        telas = Tela.objects.all()
        serializer = TelaSerializer(telas, many=True)
        return Response(serializer.data)

class HiloListAPIView(APIView):
    def get(self, request):
        hilos = Hilo.objects.all()
        serializer = HiloSerializer(hilos, many=True)
        return Response(serializer.data)

class UniformeListAPIView(APIView):
    def get(self, request):
        uniformes = Uniforme.objects.all()
        serializer = UniformeSerializer(uniformes, many=True)
        return Response(serializer.data)


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
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Categoría actualizada", "categoria": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EliminarCategoria(APIView):
    def delete(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.delete()
        return Response({"mensaje": "Categoría eliminada correctamente"}, status=status.HTTP_204_NO_CONTENT)

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
        ventas = Venta.objects.all()
        serializer = VentaSerializer(ventas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

#logica para agregar, quitar stock y agregar nuevo producto al inventario

# Funciones para agregar stock
class AgregarStockHilo(APIView):
    def patch(self, request, pk):
        cantidad = request.data.get('cantidad')
        if not cantidad:
            return Response({'error': 'Cantidad requerida'}, status=status.HTTP_400_BAD_REQUEST)

        hilo = get_object_or_404(Hilo, pk=pk)
        hilo.stock += int(cantidad)
        hilo.save()

        serializer = HiloSerializer(hilo)
        return Response({'message': 'Stock de hilo actualizado', 'hilo': serializer.data}, status=status.HTTP_200_OK)

class AgregarStockTela(APIView):
    def patch(self, request, pk):
        cantidad = request.data.get('cantidad')
        if not cantidad:
            return Response({'error': 'Cantidad requerida'}, status=status.HTTP_400_BAD_REQUEST)

        tela = get_object_or_404(Tela, pk=pk)
        tela.stock += int(cantidad)
        tela.save()

        serializer = TelaSerializer(tela)
        return Response({'message': 'Stock de tela actualizado', 'tela': serializer.data}, status=status.HTTP_200_OK)

class AgregarStockUniforme(APIView):
    def patch(self, request, pk):
        cantidad = request.data.get('cantidad')
        if not cantidad:
            return Response({'error': 'Cantidad requerida'}, status=status.HTTP_400_BAD_REQUEST)

        uniforme = get_object_or_404(Uniforme, pk=pk)
        uniforme.stock += int(cantidad)
        uniforme.save()

        serializer = UniformeSerializer(uniforme)
        return Response({'message': 'Stock de uniforme actualizado', 'uniforme': serializer.data}, status=status.HTTP_200_OK)


# Funciones para quitar stock
class QuitarStockHilo(APIView):
    def patch(self, request, pk):
        cantidad = request.data.get('cantidad')
        if not cantidad:
            return Response({'error': 'Cantidad requerida'}, status=status.HTTP_400_BAD_REQUEST)

        hilo = get_object_or_404(Hilo, pk=pk)
        cantidad = int(cantidad)  
        
        if hilo.stock < cantidad:
            return Response({'error': 'Stock insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

        hilo.stock -= cantidad
        hilo.save()

        serializer = HiloSerializer(hilo)
        return Response({'message': 'Stock de hilo reducido', 'hilo': serializer.data}, status=status.HTTP_200_OK)

class QuitarStockTela(APIView):
    def patch(self, request, pk):
        cantidad = request.data.get('cantidad')
        if not cantidad:
            return Response({'error': 'Cantidad requerida'}, status=status.HTTP_400_BAD_REQUEST)

        tela = get_object_or_404(Tela, pk=pk)
        cantidad = int(cantidad)  
        
        if tela.stock < cantidad:
            return Response({'error': 'Stock insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

        tela.stock -= cantidad
        tela.save()

        serializer = TelaSerializer(tela)
        return Response({'message': 'Stock de tela reducido', 'tela': serializer.data}, status=status.HTTP_200_OK)

class QuitarStockUniforme(APIView):
    def patch(self, request, pk):
        cantidad = request.data.get('cantidad')
        if not cantidad:
            return Response({'error': 'Cantidad requerida'}, status=status.HTTP_400_BAD_REQUEST)

        uniforme = get_object_or_404(Uniforme, pk=pk)
        cantidad = int(cantidad)  
        
        if uniforme.stock < cantidad:
            return Response({'error': 'Stock insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

        uniforme.stock -= cantidad
        uniforme.save()

        serializer = UniformeSerializer(uniforme)
        return Response({'message': 'Stock de uniforme reducido', 'uniforme': serializer.data}, status=status.HTTP_200_OK)
    
# Funciones para agregar nuevos productos
class AgregarNuevoHilo(APIView):
    def post(self, request):
        serializer = HiloSerializer(data=request.data)
        if serializer.is_valid():
            if Hilo.objects.filter(codigo=serializer.validated_data['codigo']).exists():
                return Response({'error': 'Ya existe un hilo con ese código'}, status=status.HTTP_400_BAD_REQUEST)

            hilo = serializer.save()
            return Response({'message': 'Hilo agregado exitosamente', 'hilo': hilo.nombre}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgregarNuevaTela(APIView):
    def post(self, request):
        serializer = TelaSerializer(data=request.data)
        if serializer.is_valid():
            if Tela.objects.filter(codigo=serializer.validated_data['codigo']).exists():
                return Response({'error': 'Ya existe una tela con ese código'}, status=status.HTTP_400_BAD_REQUEST)

            tela = serializer.save()
            return Response({'message': 'Tela agregada exitosamente', 'tela': tela.nombre}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgregarNuevoUniforme(APIView):
    def post(self, request):
        material_id = request.data.get('material')
        categoria_id = request.data.get('categoria')

        material = None
        if material_id:
            try:
                material = Tela.objects.get(id=material_id)
            except Tela.DoesNotExist:
                return Response({'error': 'Material no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

        categoria = None
        if categoria_id:
            try:
                categoria = Categoria.objects.get(id=categoria_id)
            except Categoria.DoesNotExist:
                return Response({'error': 'Categoría no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UniformeSerializer(data=request.data)
        if serializer.is_valid():
            # Evitar duplicados por combinación
            if Uniforme.objects.filter(
                tipo=serializer.validated_data['tipo'],
                talla=serializer.validated_data['talla'],
                color=serializer.validated_data['color']
            ).exists():
                return Response({'error': 'Ya existe un uniforme con esas características'}, status=status.HTTP_400_BAD_REQUEST)

            uniforme = serializer.save(material=material, categoria=categoria)
            return Response({'message': 'Uniforme agregado exitosamente', 'uniforme': uniforme.tipo}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all().order_by('nombre')
    serializer_class = ProveedorSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nombre', 'correo', 'telefono']


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all().order_by('-fecha')
    serializer_class = CompraSerializer


# Metodos para el área de contabiidad 

class OperacionViewSet(viewsets.ModelViewSet):
    queryset = Operacion.objects.all()
    serializer_class = OperacionSerializer


class OperacionSummaryAPIView(APIView):
    def get(self, request):
        ingresos = Operacion.objects.filter(tipo='ingreso').aggregate(
            total=Sum('monto')
        )['total'] or 0
        
        egresos = Operacion.objects.filter(tipo='egreso').aggregate(
            total=Sum('monto')
        )['total'] or 0
        
        total_ops = Operacion.objects.count()
        
        data = {
            'ingresos': float(ingresos),
            'egresos': float(egresos),
            'balance': float(ingresos - egresos),
            'total': total_ops
        }
        
        return Response(data, status=status.HTTP_200_OK)
    
#   Agregar Nueva Orden
class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

class HistorialPedidosAPIView(ListAPIView):
    queryset = Orden.objects.all().order_by('-fecha')
    serializer_class = OrdenSerializer

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

# VENTAS
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
            producto = get_object_or_404(Producto, pk=item["producto"])
            cantidad = int(item["cantidad"])
            precio_unitario = Decimal(item.get("precio_unitario", producto.precio))
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
            producto = get_object_or_404(Producto, pk=item["producto"])
            cantidad = int(item["cantidad"])
            precio_unitario = Decimal(item.get("precio_unitario", producto.precio))
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
        return Response(
            {"mensaje": "Venta eliminada correctamente"},
            status=status.HTTP_204_NO_CONTENT,
        )