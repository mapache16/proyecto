"""
🔐 MÓDULO DE SEGURIDAD
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict
from passlib.context import CryptContext
import os

SECRET_KEY = os.getenv("SECRET_KEY", "amco-secret-key-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

PERMISOS_POR_ROL = {
    "admin": ["crear_usuario", "eliminar_usuario", "editar_config", "ver_todo"],
    "operador": ["controlar_simulacion", "crear_incidentes", "ver_analytics"],
    "usuario": ["ver_mapa", "ver_alertas"]
}

USUARIOS_DB = {
    "admin": {
        "username": "admin",
        "password_hash": pwd_context.hash("admin123"),
        "roles": ["admin"],
        "activo": True
    },
    "operador": {
        "username": "operador",
        "password_hash": pwd_context.hash("operador123"),
        "roles": ["operador"],
        "activo": True
    }
}

class RBAC:
    """Role-Based Access Control"""
    
    @staticmethod
    def obtener_permisos(roles: List[str]) -> List[str]:
        permisos = set()
        for rol in roles:
            permisos.update(PERMISOS_POR_ROL.get(rol, []))
        return list(permisos)
    
    @staticmethod
    def tiene_permiso(usuario: Dict, permiso: str) -> bool:
        roles = usuario.get("roles", [])
        permisos = RBAC.obtener_permisos(roles)
        return permiso in permisos
