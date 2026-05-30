# 🚌 SIMULADOR INTERACTIVO DE TRÁFICO DE BUSES

## 🎯 Descripción General

Este simulador interactivo permite **jugar con el sistema de transporte de buses**, ver cómo se comporta el tráfico en tiempo real y demostrar la efectividad del sistema.

### ✨ Características Principales

✅ **Simulación en Tiempo Real**
- Actualización dinámica de posiciones de buses
- Cálculo real de tiempos basado en distancias
- Congestión realista según demanda

✅ **Controles Interactivos**
- Iniciar/pausar/reiniciar simulación
- Ajustar demanda de pasajeros
- Cambiar velocidad de buses
- Generar eventos especiales

✅ **Visualización Avanzada**
- Gráficos dinámicos con Plotly
- Tablas interactivas
- Histórico de métricas
- Centro de alertas

✅ **Datos Lógicos y Coherentes**
- Pasajeros suben/bajan en estaciones
- Delays basados en congestión real
- Ocupación realista de buses
- Impacto de eventos en el sistema

---

## 🚀 INSTALACIÓN Y EJECUCIÓN

### Requisitos Previos

```bash
Python 3.8+
pip (gestor de paquetes)
```

### 1. Instalar Dependencias

```bash
# Opción A: Usar requirements.txt existente
pip install -r requirements.txt

# Opción B: Instalar solo lo necesario para el simulador
pip install streamlit plotly pandas numpy
```

### 2. Ejecutar el Simulador

```bash
# Navegar a la carpeta del proyecto
cd /ruta/a/tu/proyecto

# Ejecutar el simulador interactivo
streamlit run interactive_simulator.py
```

### 3. Acceder a la Interfaz

Se abrirá automáticamente en tu navegador:
```
http://localhost:8501
```

---

## 🎮 GUÍA DE USO

### Panel de Control (Sidebar Izquierdo)

#### 1️⃣ Controles de Simulación
- **▶️ Iniciar**: Comienza la simulación
- **⏸️ Pausar**: Pausa la simulación
- **🔄 Reiniciar**: Reinicia todo desde cero

#### 2️⃣ Parámetros del Sistema
- **📊 Demanda de Pasajeros** (0.5x - 2.0x)
  - Controla cuántos pasajeros suben/bajan
  - Más demanda = más congestión

- **🚀 Velocidad de Simulación** (0.5x - 5.0x)
  - Controla qué tan rápido avanza el tiempo
  - 1.0x = velocidad normal

- **🛣️ Velocidad de Buses** (10 - 50 km/h)
  - Velocidad promedio de viaje
  - Afecta los tiempos de llegada

#### 3️⃣ Eventos Especiales
Haz clic para generar eventos que impacten el sistema:

- **🚗 Accidente**
  - Aumenta congestión en 40%
  - Dura ~30 minutos
  - Causa retrasos significativos

- **🌧️ Lluvia**
  - Aumenta congestión en 20%
  - Dura ~60 minutos
  - Reduce velocidad de buses

- **🛠️ Mantenimiento**
  - Bloquea algunos tramos
  - Dura ~45 minutos
  - Afecta ocupación de buses

- **🎉 Gran Evento**
  - Pico máximo de demanda
  - Aumenta congestión en 60%
  - Dura ~120 minutos

### Panel Principal

#### 📈 Métricas Principales
Muestra en tiempo real:
- 🚌 Número de autobuses activos
- 👥 Ocupación promedio (%)
- ⏱️ Delay promedio (minutos)
- 👨‍👩‍👧‍👦 Total de pasajeros en el sistema
- 🚗 Nivel de congestión (%)

#### 📊 Gráficos Dinámicos

**Gráfico 1: Distribución de Ocupación**
- Histograma de ocupación de buses
- Muestra cuántos buses están al 50%, 75%, 90% de ocupación, etc.
- Ayuda a identificar desequilibrios

**Gráfico 2: Pasajeros por Ruta**
- Gráfico de barras con distribución por ruta
- Identifica rutas sobrecargadas
- Sugiere necesidad de más buses

**Gráfico 3: Ocupación Histórica**
- Línea de tendencia de ocupación a lo largo del tiempo
- Muestra picos y valles de demanda

**Gráfico 4: Delay Histórico**
- Evolución de retrasos
- Muestra impacto de eventos

#### 🚌 Tabla de Autobuses
Muestra detalles individuales:
- ID del bus
- Ruta asignada
- Pasajeros actuales
- Porcentaje de ocupación
- Estación actual
- Minutos de retraso
- Velocidad actual

#### 🚧 Historial de Eventos
Registra los últimos 10 eventos:
- Tipo de evento
- Tiempo de ocurrencia
- Severidad

---

## 📋 ESCENARIOS DE DEMOSTRACIÓN

### Escenario 1: Sistema Normal
```
1. Iniciar simulador
2. Demanda: 1.0x
3. Velocidad buses: 30 km/h
4. Dejar correr 5 minutos
5. Observar: Ocupación estable ~40-50%, delays mínimos
```

### Escenario 2: Hora Pico
```
1. Iniciar simulador
2. Aumentar demanda a 1.8x
3. Velocidad de simulación: 2.0x
4. Dejar correr 3 minutos
5. Observar: Ocupación sube a 60-80%, delays aumentan
```

### Escenario 3: Con Incidente
```
1. Iniciar simulador en estado normal
2. Dejar correr 1 minuto
3. Hacer clic en "🚗 Accidente"
4. Observar: Congestión sube a 70-80%
5. Ver cómo se recupera el sistema después
```

### Escenario 4: Múltiples Eventos
```
1. Iniciar simulador
2. Aumentar demanda a 1.5x
3. Generar "🚗 Accidente"
4. Después de 2 minutos, generar "🌧️ Lluvia"
5. Observar cómo se componen los efectos
6. Ver la recuperación gradual
```

### Escenario 5: Caos Total
```
1. Aumentar demanda a 2.0x
2. Reducir velocidad de buses a 15 km/h
3. Generar "🎉 Gran Evento"
4. Dejar correr 2 minutos
5. Generar "🚗 Accidente"
6. Observar punto crítico del sistema
```

---

## 📊 DATOS Y LÓGICA

### ¿Cómo se Calculan los Datos?

#### Ocupación de Buses
```
Ocupación = Pasajeros Actuales / Capacidad Máxima
```

#### Tiempo de Viaje
```
Tiempo = Distancia Total / (Velocidad Base * Factor de Congestión)
```

#### Congestión
```
Congestión = Base (0.3) + Demanda (0-0.4) + Eventos (0-0.3)
Máximo: 1.0 (totalmente congestionado)
```

#### Delays
```
Delay = Delay Anterior + (Congestión * Factor Acumulativo)
```

#### Cambio de Pasajeros
```
- 30% de probabilidad por minuto
- Cambio aleatorio: -5 a +10 pasajeros
- Se respeta la capacidad máxima
```

### Validaciones de Datos

✅ **Coherencia**
- Los pasajeros nunca superan la capacidad
- Los delays son siempre positivos
- La congestión está entre 0 y 1

✅ **Realismo**
- Los buses se mueven linealmente
- Los eventos tienen duración realista
- Los multiplicadores de demanda son progresivos

---

## 🔧 PERSONALIZACIÓN

### Cambiar Configuración Base

Edita `simulator_config.py`:

```python
# Número de autobuses
SIMULATION_CONFIG.BUSES_PER_ROUTE = 5  # más buses

# Capacidad de autobuses
BUS_CONFIG.DEFAULT_CAPACITY = 80  # más grande

# Congestión base
SIMULATION_CONFIG.BASE_CONGESTION = 0.2  # menos congestionado

# Impacto de eventos
EVENT_CONFIG.ACCIDENT_CONGESTION_IMPACT = 0.5  # más impacto
```

### Agregar Nuevas Rutas

Edita `interactive_simulator.py`:

```python
route_names = [
    "Ruta Centro-Norte",
    "Ruta Sur-Este",
    "Tu Nueva Ruta",  # Agregar aquí
    # ...
]
```

---

## 🐛 TROUBLESHOOTING

### Problema: "ModuleNotFoundError: No module named 'streamlit'"

**Solución:**
```bash
pip install streamlit
```

### Problema: La simulación va muy lenta

**Solución:**
- Aumenta "🚀 Velocidad de Simulación" a 3.0x o más
- Reduce la ventana del navegador
- Cierra otras aplicaciones

### Problema: Los números no tiene sentido

**Solución:**
- Reinicia con el botón 🔄
- Verifica que los controles estén en valores razonables
- Comprueba la carpeta `logs/` para errores

---

## 📈 MÉTRICAS Y KPIs

### Key Performance Indicators (KPIs)

1. **Ocupación Promedio**
   - Ideal: 50-65%
   - Advertencia: > 75%
   - Crítico: > 85%

2. **Delay Promedio**
   - Ideal: < 5 minutos
   - Advertencia: 5-15 minutos
   - Crítico: > 15 minutos

3. **Congestión**
   - Baja: < 40%
   - Moderada: 40-60%
   - Alta: 60-80%
   - Crítica: > 80%

4. **Pasajeros Transportados**
   - Metrica de capacidad del sistema
   - Tendencia ascendente = crecimiento

---

## 🎓 PUNTOS DE APRENDIZAJE

### Conceptos Demostrados

✅ **Simulación de Sistemas**
- Actualización en tiempo real
- Propagación de eventos
- Efectos cascada

✅ **Gestión de Tráfico**
- Balanceo de demanda
- Identificación de cuellos de botella
- Planificación de recursos

✅ **Análisis de Datos**
- Distribuciones estadísticas
- Series de tiempo
- Alertas automáticas

✅ **Experiencia de Usuario**
- Interfaz intuitiva
- Feedback en tiempo real
- Controles responsivos

---

## 📞 SOPORTE

¿Problemas? Revisa:
- `ESTRUCTURA_PROYECTO.md` - Arquitectura completa
- `MEJORAS_FASE6.md` - Historial de cambios
- Comentarios en el código

---

## 🚀 Próximas Mejoras Planeadas

- [ ] Mapa interactivo 3D con ubicación de buses
- [ ] Predicción de demanda con ML
- [ ] Optimización automática de rutas
- [ ] Exportación de reportes
- [ ] Integración con datos reales de GPS
- [ ] Sistema de recomendaciones

---

**¡Diviértete experimentando con el simulador! 🎮**
