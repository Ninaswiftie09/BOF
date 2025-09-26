# api/utils/roles.py
from typing import Literal

# IDs fijos segun tu BD (auth_user_groups.group_id):
ADMIN_GROUP_ID = 1
EMPLEADO_GROUP_ID = 2

Role = Literal["admin", "empleado", "ninguno"]

def get_role(user) -> Role:
    if not user or not user.is_authenticated:
        return "ninguno"
    if user.is_superuser:
        return "admin"
    # Chequeo directo por IDs de grupo
    if user.groups.filter(id=ADMIN_GROUP_ID).exists():
        return "admin"
    if user.groups.filter(id=EMPLEADO_GROUP_ID).exists():
        return "empleado"
    return "ninguno"

def is_admin(user) -> bool:
    return get_role(user) == "admin"

def is_empleado(user) -> bool:
    return get_role(user) == "empleado"
