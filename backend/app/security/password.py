"""Manejo seguro de contraseñas."""

from passlib.context import CryptContext
from backend.app.config import PASSWORD_MIN_LENGTH

# Configuración de encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Encripta una contraseña.
    
    Args:
        password: Contraseña en texto plano
    
    Returns:
        Contraseña encriptada
    """
    if len(password) < PASSWORD_MIN_LENGTH:
        raise ValueError(f"Contraseña debe tener al menos {PASSWORD_MIN_LENGTH} caracteres")
    
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña.
    
    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Contraseña encriptada
    
    Returns:
        True si coincide, False en caso contrario
    """
    return pwd_context.verify(plain_password, hashed_password)
