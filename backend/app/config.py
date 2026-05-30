"""Configuración global del sistema."""

import os
from dotenv import load_dotenv

load_dotenv()

# Base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./empresa_transporte.db"
)

# JWT
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "tu-clave-secreta-muy-segura-cambiar-en-produccion"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

# API
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8000))

# CORS
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8501",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8501",
]

# ML Models
ML_MODELS_PATH = "backend/app/ml/models"
CLUSTERING_N_CLUSTERS = 5
FORECASTING_WINDOW = 24  # horas

# Cache
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CACHE_EXPIRY = 300  # segundos

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = "logs/amco.log"

# Seguridad
PASSWORD_MIN_LENGTH = 8
MAX_LOGIN_ATTEMPTS = 5
LOCK_TIME = 900  # 15 minutos
