# 🚌 GUÍA - SISTEMA COMPACTO DE TRANSPORTE (2DO SEMESTRE)

## ¿Qué es?

Sistema simplificado de visualización de buses con:
- **~300 líneas** de código limpio
- **Ágebra Lineal** aplicada
- **Dos formas de ejecutar**: terminal o interfaz gráfica
- **100% Python** puro

## Archivos

### 1. `mini_bus.py` - Código Principal
- Sistema completo en un archivo
- Clases: Parada, Bus, SistemaBuses, Visor, Matematica
- Sin dependencias externas (solo numpy + matplotlib)

### 2. `ejecutor_gui.py` - Interfaz Gráfica (Recomendado)
- Interfaz con botones (sin línea de comandos)
- 5 opciones interactivas
- Fácil de usar

## Instalación (Primer Semestre)

### Opción 1: Windows
```bash
# 1. Abrir Command Prompt (cmd)
# 2. Copiar los archivos a una carpeta
# 3. Ejecutar:
pip install numpy matplotlib
```

### Opción 2: Directo en VS Code
```
1. Abrir carpeta con los archivos
2. Click derecho → "Abrir terminal integrada"
3. Pegar: pip install numpy matplotlib
4. Ejecutar
```

## Ejecución

### ✅ Forma 1: SIN Terminal (Interfaz Gráfica) - RECOMENDADO

```bash
python ejecutor_gui.py
```

**Aparece una ventana con 5 botones:**

1. 🎯 **CREAR SISTEMA** → Inicializa paradas y buses
2. 🔄 **EJECUTAR SIMULACIÓN** → Corre 50 pasos
3. 📊 **VER GRÁFICOS** → Muestra 4 gráficos
4. 📋 **VER ESTADÍSTICAS** → Datos en consola
5. ⚡ **EJECUTAR TODO** → Hace todo automático

### ✅ Forma 2: Terminal Tradicional

```bash
python mini_bus.py
```

**Resultado:**
- Ejecuta todo automáticamente
- Muestra gráficos
- Solo 1 comando

## Código Explicado (Ágebra Lineal)

### 1. Distancia Euclidiana
```python
# Norma L2: ||v|| = sqrt(x^2 + y^2)
def distancia(p1, p2):
    dlat = p2.lat - p1.lat
    dlon = p2.lon - p1.lon
    return np.sqrt(dlat**2 + dlon**2) * 111  # km
```

### 2. Interpolación Vectorial
```python
# P(t) = P1 + t*(P2 - P1)  donde t ∈ [0,1]
def interpolar(p1, p2, t):
    lat = p1[0] + t * (p2[0] - p1[0])
    lon = p1[1] + t * (p2[1] - p1[1])
    return (lat, lon)
```

### 3. Matriz de Distancias (implícita)
```python
# Distancia total = suma de segmentos
def distancia_total(ruta):
    total = 0.0
    for i in range(len(ruta) - 1):
        total += distancia(ruta[i], ruta[i + 1])
    return total
```

### 4. Congestión (Operación Matricial)
```python
# Ocupación = (pasajeros / capacidad) * 100
# Congestión = suma(ocupaciones) / num_buses
def congestion():
    ocupacion = sum(b.pasajeros for b in buses) / (len(buses) * 60)
    return min(1.0, ocupacion)
```

## Estructura de Datos

```python
Parada
  ├─ id: int
  ├─ nombre: str
  ├─ lat: float (latitud)
  └─ lon: float (longitud)

Bus
  ├─ id: int
  ├─ nombre: str
  ├─ ruta: List[Parada]
  ├─ progreso: float (0.0-1.0)
  └─ pasajeros: int

SistemaBuses
  ├─ paradas: List[Parada]
  ├─ buses: List[Bus]
  └─ historial: List[Dict]  # Datos de cada paso
```

## Visualización

### 4 Gráficos Generados

**1. Mapa de Rutas**
- Todas las rutas en líneas
- Paradas como puntos

**2. Posición de Buses**
- Rutas en gris
- Buses como triángulos:
  - 🟢 Verde: <50% ocupación
  - 🟡 Amarillo: 50-80%
  - 🔴 Rojo: >80%

**3. Ocupación Actual**
- Gráfico de barras
- Un bar por bus
- Colores según ocupación

**4. Historial de Congestión**
- Línea del tiempo
- Muestra evolución
- Área rellena

## Personalización

### Agregar Más Paradas
```python
sistema.agregar_parada(id, "Nombre", lat, lon)
```

### Agregar Más Buses
```python
sistema.agregar_bus(id, "Bus-XXX", [parada_ids])
```

### Cambiar Pasos de Simulación
```python
sistema.simular(pasos=100)  # En lugar de 50
```

### Cambiar Velocidad/Pasajeros
En `mini_bus.py`, función `simular()`:
```python
bus.progreso += 0.02      # Cambiar 0.02 por otro valor
bus.pasajeros += np.random.randint(-2, 3)  # Cambiar rango
```

## Solución de Problemas

### Error: "No module named 'numpy'"
```bash
pip install numpy matplotlib
```

### No aparece la ventana gráfica
```bash
# Probar:
python -m tkinter
```

### Los gráficos se ven pequeños
En `visor.mostrar_todo()`:
```python
fig, axes = plt.subplots(2, 2, figsize=(16, 12))  # Aumentar figsize
```

## Concepto de Proyecto (2do Semestre)

Este código demuestra:

✅ **Algoritmos**
- Interpolación
- Cálculos de distancia
- Iteración y acumulación

✅ **Estructuras de Datos**
- Clases y dataclasses
- Listas y diccionarios
- Estado compartido

✅ **Matemáticas**
- Norma euclidiana
- Vectores
- Operaciones matriciales

✅ **Programación**
- OOP
- Funciones
- Módulos

✅ **Visualización**
- Matplotlib
- Tkinter
- Representación de datos

## Extensiones Futuras

- [ ] Agregar más paradas dinámicamente
- [ ] Guardar datos en CSV
- [ ] Optimización de rutas
- [ ] Predicción de congestión
- [ ] API REST
- [ ] Base de datos

## Requisitos Mínimos

- Python 3.8+
- numpy
- matplotlib
- tkinter (generalmente incluido)

## Respuestas Frecuentes

**P: ¿Funciona solo en Python?**
R: Sí, código puro Python. Funciona en Windows, Mac y Linux.

**P: ¿Funciona en VS Code?**
R: Sí, ejecuta `python mini_bus.py` o `python ejecutor_gui.py`

**P: ¿Qué es lo más simple para ejecutar?**
R: `python ejecutor_gui.py` - Solo haz click en botones

**P: ¿Puedo modificar el código?**
R: Claro, es tu proyecto. Agrega paradas, buses, o nuevas funciones.

**P: ¿Cómo entrego esto?**
R: Comprime los archivos `.py` y envía como proyecto.

---

**¡Listo para usar!** 🚀
