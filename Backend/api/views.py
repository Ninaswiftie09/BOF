from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import json
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from .models import Venta, DetalleVenta, Producto
from .serializers import VentaSerializer

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