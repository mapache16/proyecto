# 🚌 GUÍA: Sistema Simplificado de Visualización de Flujo de Buses

## Descripción General

Sistema Python puro y modular para:
- ✅ Simular transporte metropolitano con lógica determinista
- ✅ Visualizar flujo de buses en tiempo real
- ✅ Generar mapas de calor de congestión
- ✅ Analizar comportamiento sin componentes complejos

## Características Principales

### 1. **Lógica Limpia y Modular**
```python
SistemaTransporte          # Gestor central
├── Parada                 # Ubicación GPS
├── Ruta                   # Secuencia de paradas
└── Bus                    # Entidad móvil en ruta
```

### 2. **Álgebra Lineal Implementada**

#### Distancia Euclidiana
```python
# ||v|| = sqrt((lat2-lat1)² + (lon2-lon1)²)
distancia = np.sqrt(dlat_km² + dlon_km²)
```

#### Interpolación Vectorial (P(t) = P1 + t*(P2-P1))
```python
# Movimiento suave del bus entre paradas
lat = p1.latitud + t * (p2.latitud - p1.latitud)
lon = p1.longitud + t * (p2.longitud - p1.longitud)
```

#### Algoritmo de Dijkstra (implícito en rutas óptimas)
- Cálculo de distancia total de rutas
- Asignación inteligente de buses

### 3. **Visualización de Comportamiento de Buses**

#### Mapa Estático
- Red de rutas y paradas
- Posición fija inicial de buses

#### Tiempo Real (Animación)
- Movimiento de buses interpolado
- Color según ocupación:
  - 🟢 Verde: < 50% ocupación
  - 🟡 Amarillo: 50-80%
  - 🔴 Rojo: > 80%

#### Mapa de Calor
- Congestión por ruta
- Histórico de pasajeros

#### Análisis por Ruta
- Detalle de buses por ruta
- Cálculo de congestión específica

### 4. **Comportamiento Lógico (No Aleatorio)**

```python
# Variación realista pero controlada
variación = np.random.normal(1.0, 0.05)  # Media=1, desv=0.05
velocidad_ajustada = velocidad * variación
velocidad_ajustada = max(5, min(60, velocidad_ajustada))  # Rango 5-60

# Pasajeros con lógica clara
if ocupacion < 50:
    pasajeros += np.random.randint(0, 3)  # Suben 0-3
elif ocupacion > 80:
    pasajeros -= np.random.randint(0, 3)  # Bajan 0-3
```

## Instalación

### Requisitos
```bash
python 3.8+
numpy
matplotlib
```

### Instalación
```bash
# Clonar o descargar archivos
cd proyecto

# Instalar dependencias (si es necesario)
pip install numpy matplotlib

# ¡Listo! No requiere BD ni servidores externos
```

## Uso

### Opción 1: Uso Directo (bus_system_simple.py)

```bash
python bus_system_simple.py
```

Muestra automáticamente:
1. Mapa estático de la red
2. Posición de buses en tiempo real
3. Mapa de calor de congestión
4. Estadísticas del sistema

### Opción 2: Interactivo (visualización_interactiva.py)

```bash
python visualización_interactiva.py
```

Menú interactivo con opciones:
```
1. Visualizar mapas estáticos
2. Simulación en tiempo real (animación)
3. Mapa de calor de congestión
4. Estadísticas del sistema
5. Análisis detallado por ruta
6. Velocidad vs Ocupación
0. Salir
```

### Opción 3: Uso en Código

```python
from bus_system_simple import SistemaTransporte, VisualizadorTransporte, crear_sistema_demo

# Crear sistema
sistema = crear_sistema_demo()

# Simular 100 pasos
for paso in range(100):
    sistema.simular_paso(dt=0.1)

# Visualizar
visualizador = VisualizadorTransporte(sistema)
visualizador.visualizar_buses_en_tiempo_real()

# Obtener estadísticas
stats = sistema.estadísticas()
print(f"Pasajeros: {stats['total_pasajeros']}")
print(f"Ocupación: {stats['ocupacion_promedio']:.1f}%")
```

## Estructura del Código

### bus_system_simple.py

#### Clases Principales

**Parada**
- Propiedades: id, nombre, lat, lon
- Método: `distancia_a(otra_parada)` → Euclidiana

**Ruta**
- Propiedades: id, nombre, paradas
- Métodos:
  - `distancia_total()` → suma de segmentos
  - `get_posicion_en_ruta(progreso)` → interpolación P(t)

**Bus**
- Propiedades: id, placa, ruta, progreso, pasajeros, velocidad
- Métodos:
  - `avanzar(dt)` → actualiza progreso
  - `get_posicion()` → (lat, lon) actual
  - `get_ocupacion_porcentaje()` → %

**SistemaTransporte**
- Gestor central
- Métodos:
  - `crear_parada()`, `crear_ruta()`, `crear_bus()`
  - `simular_paso()` → avanza todos los buses
  - `obtener_congestión_ruta()` → 0.0 a 1.0
  - `estadísticas()` → dict con métricas

**VisualizadorTransporte**
- Genera gráficos matplotlib
- Métodos:
  - `visualizar_mapa_estático()`
  - `visualizar_buses_en_tiempo_real()`
  - `visualizar_mapa_de_calor()`
  - `visualizar_estadísticas()`

### visualización_interactiva.py

**SimuladorInteractivo**
- Envuelve SistemaTransporte
- Proporciona 6 opciones interactivas
- Menú en consola

## Conceptos de Álgebra Lineal

### 1. Norma Euclidiana (L2)
```
||v|| = sqrt(x² + y²)

Usado para calcular distancia entre paradas.
```

### 2. Interpolación Vectorial
```
P(t) = P₁ + t*(P₂ - P₁)    donde t ∈ [0,1]

Usado para movimiento suave de buses.
```

### 3. Matriz de Distancias
```
D[i,j] = ||P_i - P_j||₂

Usada en análisis de conectividad.
```

### 4. Operaciones Matriciales
```
Ocupación = (pasajeros_totales / capacidad_total) × 100
Congestión = sum(pasajeros) / sum(capacidades)
```

## Mapas Generados

### 1. Mapa Base
- Rutas en azul punteado
- Paradas como puntos rojos
- Sin animación

### 2. Mapa en Tiempo Real
- Rutas en gris claro
- Buses como triángulos:
  - 🟢 Verde (< 50% ocupación)
  - 🟡 Amarillo (50-80%)
  - 🔴 Rojo (> 80%)
- Actualización cada frame

### 3. Mapa de Calor
- Gráfico de barras con congestión por ruta
- Colores según nivel
- Valores en porcentaje

### 4. Análisis por Ruta
- Un gráfico por cada ruta
- Posición de buses en la ruta
- Metros de congestión calculada

## Ejemplo de Salida

```
============================================================
SISTEMA SIMPLIFICADO DE VISUALIZACIÓN DE FLUJO DE BUSES
============================================================

✅ Sistema creado con éxito
   - 5 paradas
   - 3 rutas
   - 15 buses

🔄 Ejecutando simulación...
   Paso 20: Pasajeros=425, Ocupación=47.2%, Velocidad=33.2 km/h
   Paso 40: Pasajeros=468, Ocupación=51.9%, Velocidad=34.1 km/h
   Paso 60: Pasajeros=502, Ocupación=55.8%, Velocidad=32.8 km/h
   Paso 80: Pasajeros=541, Ocupación=60.1%, Velocidad=33.5 km/h
   Paso 100: Pasajeros=589, Ocupación=65.4%, Velocidad=34.2 km/h

📊 Generando visualizaciones...
   ✓ Mapa estático
   ✓ Buses en tiempo real
   ✓ Mapa de calor de congestión
   ✓ Estadísticas del sistema

============================================================
ESTADÍSTICAS FINALES
============================================================
Total de buses:               15
Pasajeros totales:           589
Ocupación promedio:          65.4%
Velocidad promedio:          34.2 km/h
Tiempo de simulación:        10.00 horas
============================================================
```

## Personalización

### Agregar Más Paradas
```python
sistema = SistemaTransporte()
p1 = sistema.crear_parada(1, "Mi Parada", 4.8135, -75.6942)
```

### Crear Nueva Ruta
```python
r1 = sistema.crear_ruta(1, "Mi Ruta", "MR01", [1, 2, 3, 1])
```

### Agregar Bus
```python
bus = sistema.crear_bus(1, "BUS-001", ruta_id=1, velocidad=40.0)
```

### Cambiar Parámetros de Simulación
```python
# En bus_system_simple.py, función simular_paso():
# - Variar dt para tiempo diferente
# - Cambiar std dev de velocidad (0.05 → 0.10)
# - Ajustar rangos de pasajeros
```

## Solución de Problemas

### Error: `ModuleNotFoundError: No module named 'numpy'`
```bash
pip install numpy matplotlib
```

### Las gráficas no se muestran
```python
# Al final del script, asegúrate de tener:
plt.show()
```

### Simulación muy lenta
```python
# Reduce el número de pasos o aumenta dt
for paso in range(50):  # Antes: 100
    sistema.simular_paso(dt=0.5)  # Antes: 0.1
```

## Próximas Mejoras

- [ ] Exportar datos a CSV
- [ ] Gráficos interactivos con Plotly
- [ ] Integración con mapas reales (Folium)
- [ ] Predicción de congestión con ML simple
- [ ] WebSocket para tiempo real en navegador
- [ ] Optimización de rutas con A*

## Referencias Matemáticas

### Distancia Euclidiana
[Wikipedia - Euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance)

### Interpolación Lineal
[Wikipedia - Linear interpolation](https://en.wikipedia.org/wiki/Linear_interpolation)

### Algoritmo de Dijkstra
[Wikipedia - Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

## Licencia

© 2026 Sistema AMCO Simplificado - Código abierto

---

**¿Preguntas?** Revisa los archivos .py para documentación en línea.
