# views.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import User  # Usamos el modelo User predeterminado de Django
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')  
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'success': False, 'message': 'Email y contraseña son requeridos'}, status=400)

            user = authenticate(request, username=email, password=password)  

            if user is not None:
                return JsonResponse({'success': True, 'message': 'Login exitoso'})
            else:
                return JsonResponse({'success': False, 'message': 'Credenciales incorrectas'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Error al procesar los datos'}, status=400)

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)



@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'El correo electrónico ya está registrado'}, status=400)

        try:
            user = User.objects.create_user(
                username=email,  
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            return JsonResponse({'success': True, 'message': 'Usuario creado exitosamente'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al crear usuario: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)
