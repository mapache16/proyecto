# 🏗️ Arquitectura del Sistema AMCO

## Descripción General

**AMCO** (Centro Inteligente Metropolitano) es un sistema integral de monitoreo y optimización de transporte metropolitano. Implementa arquitectura de microservicios con FastAPI, machine learning avanzado y visualización en tiempo real.

---

## 📐 Arquitectura de Capas

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React/Streamlit)              │
│         • Mapas interactivos (Pydeck, Mapbox)             │
│         • Dashboard en tiempo real                         │
│         • Visualización de semáforos                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    API LAYER (FastAPI)                      │
│   • REST Endpoints (usuarios, rutas, telemetría)           │
│   • WebSocket para datos en tiempo real                     │
│   • Validación con Pydantic                                │
│   • CORS habilitado para múltiples orígenes               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  BUSINESS LOGIC LAYER                       │
│   • Servicios de optimización de rutas                      │
│   • Cálculos de congestión                                 │
│   • Predicción de demanda (ML)                             │
│   • Detección de anomalías                                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                               │
│   • SQLAlchemy ORM                                         │
│   • SQLite/PostgreSQL                                      │
│   • Caché Redis (opcional)                                 │
│   • Cache Memcached                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura de Carpetas

```
Proyecto-/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # Punto de entrada FastAPI
│   │   ├── config.py               # Configuración global
│   │   ├── security/
│   │   │   ├── __init__.py
│   │   │   ├── jwt_handler.py      # Manejo de JWT
│   │   │   ├── rbac.py             # Control de roles
│   │   │   └── password.py         # Hash de contraseñas
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── users.py            # Router de usuarios
│   │   │   ├── buses.py            # Router de buses
│   │   │   ├── routes.py           # Router de rutas
│   │   │   ├── analytics.py        # Router de análisis
│   │   │   └── health.py           # Health check
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── database.py         # Modelos SQLAlchemy
│   │   │   └── schemas.py          # Esquemas Pydantic
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── user_service.py     # Lógica de usuarios
│   │   │   ├── bus_service.py      # Lógica de buses
│   │   │   ├── route_service.py    # Lógica de rutas
│   │   │   └── analytics_service.py # Análisis
│   │   ├── ml/
│   │   │   ├── __init__.py
│   │   │   ├��─ clustering.py       # K-Means clustering
│   │   │   ├── forecasting.py      # Predicción de demanda
│   │   │   ├── anomaly.py          # Detección anomalías
│   │   │   └── models.pkl          # Modelos entrenados
│   │   └── tasks/
│   │       ├── __init__.py
│   │       └── celery_tasks.py     # Tareas asincrónicas
│   ├── algebra.py                  # Álgebra lineal
│   ├── geo.py                      # Operaciones geoespaciales
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Map/
│   │   │   │   ├── Map.jsx
│   │   │   │   ├── HeatMap.jsx
│   │   │   │   └── TrafficLight.jsx
│   │   │   ├── Dashboard/
│   │   │   ├── Analytics/
│   │   │   └── Auth/
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── .env.example
├── docs/
│   ├── ARCHITECTURE.md    # Este archivo
│   ├── API.md             # Documentación de endpoints
│   ├── MATH.md            # Explicación de álgebra lineal
│   ├── MAPPING.md         # Guía de mapas interactivos
│   └── DEPLOYMENT.md      # Guía de despliegue
├── scripts/
│   ├── setup.sh           # Setup Linux/Mac
│   ├── setup.bat          # Setup Windows
│   ├── deploy.py          # Script de despliegue
│   └── migrate.py         # Migraciones de BD
├── tests/
│   ├── test_api.py
│   ├── test_ml.py
│   └── test_security.py
├── docker-compose.yml     # Docker Compose
├── Dockerfile             # Docker imagen
├── Makefile               # Automatización
├── .gitignore
├── .env.example
├── requirements.txt       # Dependencias principales
└── README.md              # Este archivo
```

---

## 🔄 Flujo de Datos

### 1. **Ingesta de Datos** (IoT Simulator)
```
IoT Sensor → WebSocket → API → BD → Cache
```

### 2. **Procesamiento** (Business Logic)
```
BD → Servicios → ML Models → Analytics → Caché
```

### 3. **Visualización** (Frontend)
```
Frontend → API REST → Servicios → BD
Frontend → WebSocket → Datos en tiempo real
```

---

## 🔐 Seguridad

### Autenticación
- **JWT (JSON Web Tokens)** para autenticación sin estado
- **Refresh tokens** con expiración de 7 días
- **Access tokens** con expiración de 1 hora

### Autorización (RBAC)
- **Roles**: Admin, Manager, Operador, Usuario
- **Permisos** granulares por endpoint
- **Validación** en cada petición

### Encriptación
- **Contraseñas** con bcrypt (10 rounds)
- **JWT** con algoritmo HS256
- **HTTPS** en producción

---

## 🤖 Machine Learning

### Modelos Implementados

#### 1. **Clustering** (K-Means)
- Agrupa paradas por similaridad de demanda
- Identifica patrones geográficos
- Optimiza asignación de buses

#### 2. **Forecasting** (ARIMA/Prophet)
- Predice demanda por hora
- Proyecta necesidad de buses
- Anticipa congestión

#### 3. **Anomaly Detection**
- Z-score para detección de velocidades anómalas
- Isolation Forest para comportamientos inusuales
- Alertas automáticas en tiempo real

---

## 📊 Álgebra Lineal

### Operaciones Implementadas

#### 1. **Haversine Distance**
- Cálculo de distancia entre coordenadas GPS
- Fórmula: `d = 2R * arcsin(√[sin²((lat2-lat1)/2) + cos(lat1)*cos(lat2)*sin²((lon2-lon1)/2)])`

#### 2. **Matriz de Rotación**
- Transformación de coordenadas
- Casos de uso: Orientación de rutas

#### 3. **Eigenvalues/Eigenvectors**
- Análisis de componentes principales (PCA)
- Identificación de patrones dominantes

#### 4. **SVD (Singular Value Decomposition)**
- Compresión de datos de telemetría
- Reducción de dimensionalidad

#### 5. **Interpolación Polinómica**
- Suavizado de rutas
- Predicción de trayectorias

---

## 🗺️ Operaciones Geoespaciales

### Funciones Disponibles

1. **Geocodificación** - Convertir direcciones a coordenadas
2. **Reverse Geocoding** - Convertir coordenadas a direcciones
3. **Distancia de Rutas** - Calcular distancia real entre puntos
4. **Punto-en-Polígono** - Detectar si punto está en área de servicio
5. **Heat Maps** - Visualizar densidad de congestión
6. **Búsqueda Espacial** - Paradas más cercanas
7. **Simplificación de Rutas** - Algoritmo Douglas-Peucker

---

## 🚀 Tecnologías

### Backend
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM robusto
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI
- **Celery** - Tareas asincrónicas
- **Redis** - Caché y broker de mensajes

### Frontend
- **React** - Biblioteca UI
- **Streamlit** - Dashboard rápido
- **Pydeck** - Mapas 3D
- **Plotly** - Gráficos interactivos
- **Axios** - Cliente HTTP

### Data Science
- **NumPy** - Computación numérica
- **Pandas** - Análisis de datos
- **Scikit-learn** - Machine Learning
- **Scipy** - Computación científica

### DevOps
- **Docker** - Containerización
- **Docker Compose** - Orquestación local
- **GitHub Actions** - CI/CD
- **Pytest** - Testing

---

## 📈 Escalabilidad

### Horizontal
- Múltiples instancias de API con load balancer
- Base de datos replicada (master-slave)
- Caché distribuido con Redis Cluster

### Vertical
- Optimización de queries
- Índices en tablas grandes
- Connection pooling

---

## 🔍 Monitoreo

### Métricas
- Latencia de API
- Uso de CPU/Memoria
- Errores por endpoint
- Tasa de requests

### Herramientas
- **Prometheus** - Recolección de métricas
- **Grafana** - Visualización
- **ELK Stack** - Logs centralizados

---

## 📋 API Overview

### Usuarios
- `POST /auth/register` - Registrar usuario
- `POST /auth/login` - Login
- `POST /auth/refresh` - Refrescar token

### Buses
- `GET /buses` - Listar buses
- `GET /buses/{id}` - Detalles de bus
- `POST /buses` - Crear bus
- `PUT /buses/{id}` - Actualizar bus

### Rutas
- `GET /rutas` - Listar rutas
- `GET /rutas/{id}` - Detalles de ruta
- `POST /rutas` - Crear ruta

### Analytics
- `GET /analytics/demanda` - Predicción de demanda
- `GET /analytics/congestión` - Estado de congestión
- `GET /analytics/salud` - Salud de flota

---

## 🧪 Testing

### Cobertura
- Unit tests: 85%
- Integration tests: 70%
- E2E tests: 50%

### Ejecución
```bash
pytest tests/ -v --cov=app
```

---

## 📚 Referencias

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Scikit-learn Docs](https://scikit-learn.org/)
- [Docker Docs](https://docs.docker.com/)

---

**Última actualización:** 2026-05-30  
**Versión:** 2.0