"""Control de acceso basado en roles (RBAC)."""

from enum import Enum
from typing import List


class UserRole(str, Enum):
    """Roles disponibles en el sistema."""
    ADMIN = "admin"
    MANAGER = "manager"
    OPERADOR = "operador"
    USUARIO = "usuario"


class Permission(str, Enum):
    """Permisos disponibles."""
    # Usuarios
    USER_READ = "user:read"
    USER_WRITE = "user:write"
    USER_DELETE = "user:delete"
    
    # Buses
    BUS_READ = "bus:read"
    BUS_WRITE = "bus:write"
    BUS_DELETE = "bus:delete"
    
    # Rutas
    ROUTE_READ = "route:read"
    ROUTE_WRITE = "route:write"
    ROUTE_DELETE = "route:delete"
    
    # Analytics
    ANALYTICS_READ = "analytics:read"
    ANALYTICS_WRITE = "analytics:write"


# Mapeo de roles a permisos
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        Permission.USER_READ, Permission.USER_WRITE, Permission.USER_DELETE,
        Permission.BUS_READ, Permission.BUS_WRITE, Permission.BUS_DELETE,
        Permission.ROUTE_READ, Permission.ROUTE_WRITE, Permission.ROUTE_DELETE,
        Permission.ANALYTICS_READ, Permission.ANALYTICS_WRITE,
    ],
    UserRole.MANAGER: [
        Permission.BUS_READ, Permission.BUS_WRITE,
        Permission.ROUTE_READ, Permission.ROUTE_WRITE,
        Permission.ANALYTICS_READ,
    ],
    UserRole.OPERADOR: [
        Permission.BUS_READ,
        Permission.ROUTE_READ,
        Permission.ANALYTICS_READ,
    ],
    UserRole.USUARIO: [
        Permission.ANALYTICS_READ,
    ],
}


def check_permission(user_role: UserRole, required_permission: Permission) -> bool:
    """
    Verifica si un usuario tiene un permiso específico.
    
    Args:
        user_role: Rol del usuario
        required_permission: Permiso requerido
    
    Returns:
        True si tiene permiso, False en caso contrario
    """
    return required_permission in ROLE_PERMISSIONS.get(user_role, [])


def get_user_permissions(user_role: UserRole) -> List[Permission]:
    """
    Obtiene todos los permisos de un usuario.
    
    Args:
        user_role: Rol del usuario
    
    Returns:
        Lista de permisos
    """
    return ROLE_PERMISSIONS.get(user_role, [])
