from django.contrib import admin
from django.urls import path
from users.views import login_user 
from users.views import register_user 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login_user, name='login_user'),  
    path('api/register/', register_user, name='register_user'),
]

