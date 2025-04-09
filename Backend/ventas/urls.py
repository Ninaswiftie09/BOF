from django.urls import path
from .views import VentaList

urlpatterns = [
    path('ventas/', VentaList.as_view()),
]
