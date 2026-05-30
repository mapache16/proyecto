# 📁 ESTRUCTURA MODULAR DEL PROYECTO AMCO

## 🏗️ Organización General

```
proyecto1/
│
├── 📂 MÓDULOS PRINCIPALES
│   ├── algebra.py                 # Operaciones matemáticas avanzadas
│   ├── geo.py                    # Geoespacial y mapeo
│   ├── ml_models.py              # Machine Learning y predicción
│   ├── security.py               # Autenticación y RBAC
│   └── utils.py                  # Funciones auxiliares
│
├── 📂 INTERFACES Y DASHBOARDS
│   ├── interactive_simulator.py   # Simulador interactivo (NUEVO)
│   ├── dashboard_avanzado.py     # Dashboard principal
│   └── dashboard.py              # Dashboard básico
│
├── 📂 BACKEND API
│   ├── api.py                    # API FastAPI
│   ├── models.py                 # Modelos SQLAlchemy
│   ├── schemas.py                # Validación Pydantic
│   ├── database.py               # Configuración BD
│   └── iot_simulator.py          # Generador de telemetría
│
├── 📂 CONFIGURACIÓN Y DATOS
│   ├── requirements.txt           # Dependencias Python
│   ├── .env.example              # Variables de entorno
│   ├── .gitignore                # Archivos ignorados
│   └── empresa_transporte.db     # BD SQLite
│
├── 📂 DOCUMENTACIÓN
│   ├── README.md                 # Guía principal
│   ├── ESTRUCTURA_PROYECTO.md    # Este archivo
│   ├── MATH.md                   # Explicación de algoritmos
│   ├── ARCHITECTURE.md           # Arquitectura del sistema
│   └── API.md                    # Documentación de endpoints
│
└── 📂 SCRIPTS Y UTILIDADES
    ├── seed.py                   # Inicialización de datos
    ├── setup.sh                  # Script setup Linux
    └── setup.bat                 # Script setup Windows
```

## 🔧 MÓDULOS PRINCIPALES

### 1️⃣ **algebra.py** - Operaciones Matemáticas
**Propósito:** Implementar algoritmos de álgebra lineal y cálculos especializados

```python
AlgebraTransporte:
├── haversine_distance()        # Distancia GPS entre puntos
├── matriz_distancias_haversine() # Matriz de distancias
├── z_score_anomalias()         # Detección de anomalías
└── regresion_lineal_tiempo()   # Predicción de tiempos

MatrizGrafo:
├── laplaciana()                # Matriz Laplaciana
├── pagerank()                  # Importancia de paradas
└── betweenness_simplificado()  # Centralidad de nodos
```

### 2️⃣ **geo.py** - Operaciones Geoespaciales
**Propósito:** Manejo de coordenadas, mapas y análisis espacial

```python
GeoEspacial:
├── punto_en_poligono()         # Inclusión de punto
├── paradas_proximas()          # Búsqueda de paradas cercanas
├── heatmap_densidad()          # Mapas de calor
├── simplificacion_ruta_douglas_peucker() # Optimización de rutas
└── cluster_espacial_kmeans()   # Agrupamiento de paradas

AnaliticaGeo:
├── cobertura_red()             # Análisis de cobertura
└── tiempo_promedio_acceso()    # Accesibilidad del sistema
```

### 3️⃣ **ml_models.py** - Machine Learning
**Propósito:** Modelos predictivos y análisis de datos

```python
PrediccionCongestion:
├── entrenar_ruta()             # Entrenar modelo por ruta
├── predecir_congestion()       # Predicción de congestión
└── obtener_estado()            # Clasificación de estado

DeteccionAnomalias:
├── entrenar()                  # Entrenar detector
└── detectar()                  # Detección de anomalías

ModuloEvaluacionRendimiento:
├── calcular_eficiencia_ruta()  # Eficiencia operativa
└── calcular_puntualidad()      # Análisis de puntualidad
```

### 4️⃣ **security.py** - Seguridad y Autenticación
**Propósito:** Gestión de usuarios, JWT y control de acceso

```python
SeguridadJWT:
├── hash_password()             # Encriptación de contraseñas
├── crear_token_acceso()        # Generación de JWT
└── verificar_token()           # Validación de JWT

RBAC (Role-Based Access Control):
├── obtener_permisos_usuario()  # Obtener permisos
├── tiene_permiso()             # Verificar permiso específico
└── tiene_rol()                 # Verificar rol específico

AuditoriaSeguridad:
├── registrar_evento()          # Registrar evento
└── obtener_eventos()           # Recuperar historial

GestorSesiones:
├── crear_sesion()              # Crear sesión de usuario
├── cerrar_sesion()             # Cerrar sesión
└── obtener_sesiones_activas()  # Listar sesiones
```

### 5️⃣ **utils.py** - Utilidades Generales
**Propósito:** Funciones reutilizables y auxiliares

```python
UtilsGenerales:
├── formato_hora()              # Convertir minutos a HH:MM
├── porcentaje_a_color()        # Convertir valor a color
└── estado_a_emoji()            # Convertir estado a emoji

ValidacionDatos:
├── validar_rango()             # Validar rango numérico
├── validar_coordenadas()       # Validar lat/lon
└── validar_datos_df()          # Validar columnas DataFrame

OperacionesDataFrame:
├── filtrar_por_rango_fecha()   # Filtrar por fechas
├── estadisticas_basicas()      # Calcular estadísticas
└── agrupar_y_contar()          # Agrupación y conteo

CacheSimple:
├── set()                       # Almacenar en cache
├── get()                       # Recuperar del cache
└── limpiar()                   # Limpiar cache

GeneradorReportes:
├── generar_reporte_texto()     # Reporte en texto
├── generar_reporte_json()      # Reporte en JSON
└── generar_reporte_csv()       # Reporte en CSV

LoggerSimple:
├── log()                       # Registrar log
├── obtener_logs()              # Recuperar logs
└── limpiar()                   # Limpiar logs

NormalizadorDatos:
├── normalizar_0_1()            # Normalizar a [0,1]
└── normalizar_m1_1()           # Normalizar a [-1,1]

TiemposUtiles:
└── tiempo_hasta_ahora()        # Tiempo transcurrido legible
```

## 🎮 INTERFACES

### **interactive_simulator.py** - Simulador Interactivo (NUEVO)
**Tecnología:** Streamlit + Plotly
**Características:**

```
┌─────────────────────────────────────────────┐
│       🚌 AMCO - Simulador Interactivo      │
├─────────────────────────────────────────────┤
│                                             │
│  SIDEBAR (Control)          │  ÁREA PRINCIPAL      │
│  ├─ ▶️ Iniciar/Pausar      │  ├─ 🗺️ Mapa 3D      │
│  ├─ 📊 Factor Demanda      │  ├─ 📊 Análisis     │
│  ├─ 🏃 Factor Velocidad    │  ├─ 🚨 Alertas      │
│  ├─ 🚧 Eventos Especiales  │  └─ ⚙️ Config       │
│  └─ 🔄 Reiniciar           │                     │
│                                             │
└─────────────────────────────────────────────┘
```

**Funcionalidades:**
- Control en tiempo real de parámetros
- Simulación interactiva de tráfico
- Visualización de buses en mapa 3D
- Generación de eventos especiales
- Análisis de congestión
- Centro de alertas automáticas
- Historial de eventos

### **dashboard_avanzado.py** - Dashboard Principal
**Tecnología:** Streamlit + Plotly + Pydeck
**Características:**
- Mapa 3D con hexágonos
- Mapas de calor de congestión
- Semáforos de estado
- Análisis de rendimiento
- Métricas en tiempo real

## 📊 FLUJO DE DATOS

```
┌──────────────────┐
│  IoT Simulator   │  Genera telemetría de buses
└────────┬─────────┘
         │ POST /telemetria
         ↓
┌──────────────────┐
│  API FastAPI     │  Procesa y almacena
├──────────────────┤
│ - Base de Datos  │
│ - Lógica negocio │
│ - Análisis       │
└────────┬─────────┘
         │ GET /metricas
         ↓
┌──────────────────┐
│   Dashboards     │  Visualización
├──────────────────┤
│ - Mapa           │
│ - Análisis       │
│ - Alertas        │
└──────────────────┘
```

## 🔐 ROLES Y PERMISOS

```python
ADMIN
├── crear_usuario
├── eliminar_usuario
├── editar_configuracion
├── ver_analytics_completos
├── controlar_simulacion
├── crear_incidentes
├── ver_alertas
└── exportar_datos

OPERADOR
├── controlar_simulacion
├── crear_incidentes
├── ver_alertas
├── ver_analytics
└── generar_reportes

USUARIO
├── ver_mapa
├── ver_alertas_basicas
└── solicitar_ruta
```

## 🚀 CÓMO USAR CADA MÓDULO

### Algebra
```python
from algebra import AlgebraTransporte

# Calcular distancia GPS
dist = AlgebraTransporte.haversine_distance(
    [4.7110, -74.0086],
    [4.6539, -74.0642]
)  # 7.2 km

# Detectar anomalías
datos = np.array([30, 32, 31, 50, 29, 31])
anomalias, z_scores = AlgebraTransporte.z_score_anomalias(datos)
```

### Geoespacial
```python
from geo import GeoEspacial

# Encontrar paradas cercanas
cercanas = GeoEspacial.paradas_proximas(
    (4.7110, -74.0086),
    [(4.6539, -74.0642), (4.8156, -74.0233)],
    radio_km=2.0
)

# Crear heatmap
X, Y, densidad = GeoEspacial.heatmap_densidad(puntos)
```

### Machine Learning
```python
from ml_models import PrediccionCongestion

# Crear modelo
predictor = PrediccionCongestion()
predictor.entrenar_ruta("A", X_features, y_congestion)

# Predecir
congestion = predictor.predecir_congestion("A", X_test)
estado = PrediccionCongestion.obtener_estado(congestion[0])
```

### Seguridad
```python
from security import SeguridadJWT, RBAC

# Autenticar usuario
usuario = SeguridadJWT.autenticar_usuario("admin", "password")

# Verificar permisos
tiene_acceso = RBAC.tiene_permiso(usuario, "ver_analytics")
```

### Utilidades
```python
from utils import UtilsGenerales, CacheSimple

# Formatear hora
hora = UtilsGenerales.formato_hora(125)  # "02:05"

# Usar cache
cache = CacheSimple(ttl_segundos=300)
cache.set("buses_ruta_a", data)
resultado = cache.get("buses_ruta_a")
```

## 📈 EJECUCIÓN COMPLETA

```bash
# 1. Terminal 1: IoT Simulator
python iot_simulator.py

# 2. Terminal 2: API Backend
python api.py

# 3. Terminal 3: Simulador Interactivo (NUEVO)
streamlit run interactive_simulator.py

# 4. O Dashboard Principal
streamlit run dashboard_avanzado.py
```

## ✅ VENTAJAS DE ESTA ESTRUCTURA

1. **Modularidad:** Cada componente es independiente y reutilizable
2. **Escalabilidad:** Fácil agregar nuevas funcionalidades
3. **Mantenimiento:** Código organizado y documentado
4. **Testing:** Componentes aislados facilitando pruebas
5. **Colaboración:** Múltiples desarrolladores pueden trabajar en paralelo
6. **Profesionalismo:** Estructura estándar de proyectos Python

## 🎯 PRÓXIMAS FASES

- [ ] Agregar bases de datos avanzadas (PostgreSQL)
- [ ] Implementar WebSockets para actualización en tiempo real
- [ ] Agregar más modelos de ML (LSTM, Prophet)
- [ ] Deploy en la nube (AWS, GCP)
- [ ] Integración con APIs externas
- [ ] Tests unitarios y de integración
- [ ] CI/CD con GitHub Actions
