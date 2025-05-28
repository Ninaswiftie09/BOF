from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cliente/', include('clientes.urls')), 
    path("api/", include("api.urls")), 
]
