# api/permissions.py
from rest_framework.permissions import BasePermission
from .utils.roles import is_admin, is_empleado

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and is_admin(request.user))

class IsAdminOrEmpleado(BasePermission):
    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and (is_admin(u) or is_empleado(u)))
