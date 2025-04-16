# RULES DEL PROYECTO BOF

## ❌ Archivos y Carpetas que NO deben modificarse o subirse

Por favor, **NO editar ni eliminar** los siguientes archivos/carpetas a menos que sea absolutamente necesario y con consentimiento del equipo:

- `.gitignore`: evita subir archivos innecesarios al repositorio.
- `node_modules/`: nunca debe subirse (ya está en `.gitignore`).
- `__pycache__/`: nunca debe subirse (ya está en `.gitignore`).
- `.venv/` o `venv/`: entornos virtuales, no deben subirse.
- `postgres_data/`: volumen de la base de datos, no modificar.
- Archivos como `.env` que contengan datos sensibles (ya está ignorado).
- Archivos de configuración del sistema personal (por ejemplo, `.vscode/`, `.idea/`).

## ⚙️ Explicación del ejemplo API (Django + Vue)

### Backend (Django + DRF)
Se implementó un endpoint simple para pruebas: `GET /api/ping/`

Este endpoint está definido en `Backend/api/views.py`:

```python
from django.http import JsonResponse

def ping(request):
    return JsonResponse({"message": "pong"})
```

Y está enlazado en `Backend/api/urls.py`:

```python
from django.urls import path
from .views import ping

urlpatterns = [
    path("ping/", ping),
]
```

Finalmente, se incluye en el archivo principal `Backend/proyecto_django/urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    path("api/", include("api.urls")),
]
```

### Frontend (Vue 3 + Vite)

En el archivo `Frontend/src/App.vue` se hace una llamada al endpoint `/api/ping`:

```javascript
fetch("/api/ping")
  .then(res => res.json())
  .then(data => console.log(data));
```

Y se configura el proxy en `Frontend/vite.config.js` para redirigir `/api` al backend:

```js
server: {
  host: true,
  proxy: {
    '/api': {
      target: 'http://backend:8000',
      changeOrigin: true,
    }
  }
}
```

> Gracias a esto, podemos trabajar con el frontend y backend en entornos separados usando Docker y que se comuniquen de forma transparente.

---

📌 **Recuerda**: si tienes dudas, mejor pregunta antes de hacer cambios en archivos sensibles o de configuración.