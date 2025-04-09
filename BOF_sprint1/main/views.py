from django.shortcuts import render

from django.shortcuts import render

def home(request):
    materiales = {
        'Telas grices': 100,
        'Telas azules': 20,
        'Tablas de Madera': 50,
        'Pintura': 10,
        'Hilo negro': 15,
        'Hilo verde': 15,  # Asegúrate de incluir todos los materiales que necesites
    }

    context = {
        'labels': list(materiales.keys()),
        'data': list(materiales.values())
    }

    return render(request, 'home.html', context)


def clientes(request):
    return render(request, 'clientes.html')

def facturas(request):
    return render(request, 'facturas.html')

def reportes_venta(request):
    return render(request, 'reportes_venta.html')

def calculadora_materia(request):
    return render(request, 'calculadora_materia.html')

def contabilidad(request):
    return render(request, 'contabilidad.html')

def mi_inventario(request):
    materiales = {
        'Telas grices': 100,
        'Telas azules': 20,
        'Tablas de Madera': 50,
        'Pintura': 10,
        'Hilo negro': 15,
        'Hilo verde': 15,  # Agrega más materiales según sea necesario
    }

    context = {
        'materiales': materiales,
        'labels': list(materiales.keys()),
        'data': list(materiales.values())
    }

    return render(request, 'mi_inventario.html', context)