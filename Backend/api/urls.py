from django.urls import path
from .views import ping, register_user  

urlpatterns = [
    path("ping/", ping), 
    path('register/', register_user),  
]
