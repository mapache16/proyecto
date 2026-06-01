# 🚌 DESCARGAR Y EJECUTAR EL CÓDIGO

## 📄 ¿DÓNDE ESTÁ EL CÓDIGO?

### Opción 1: GITHUB (Recomendado)

**En el repositorio:** https://github.com/mapache16/proyecto

**Archivos a descargar:**
```
📄 mini_bus.py              (Sistema básico - 300 líneas)
📄 ejecutor_gui.py          (Interfaz gráfica - SIN terminal)
📄 animacion_buses.py       (Animación en TIEMPO REAL)
📄 MINI_GUIDE.md            (Guía rápida)
```

### ✅ Paso 1: DESCARGAR desde GitHub

**Opción A - Descargar ZIP:**
```
1. Ir a: https://github.com/mapache16/proyecto
2. Click en "⮕️ Code" (verde)
3. Seleccionar "⬇️ Download ZIP"
4. Descomprimir en tu computadora
```

**Opción B - Clonar (si tienes Git):**
```bash
git clone https://github.com/mapache16/proyecto.git
cd proyecto
```

---

## 💻 INSTALACIÓN

### Paso 1: Instalar Dependencias

**Windows (Command Prompt):**
```bash
pip install numpy matplotlib
```

**Mac/Linux (Terminal):**
```bash
pip3 install numpy matplotlib
```

**En VS Code:**
```
1. Click derecho en carpeta
2. "Abrir terminal integrada"
3. Pegar: pip install numpy matplotlib
4. Enter
```

✅ **Esto solo se hace UNA SOLA VEZ**

---

## 🚌 ✅ EJECUTAR (El Código Principal)

### ⭐ **RECOMENDADO: Animación en Tiempo Real**

```bash
python animacion_buses.py
```

**¿Qué hace?**
```
✅ Crea 4 paradas en Pereira, Colombia
✅ Crea 3 buses con DIFERENTES velocidades
✅ ANIMA el movimiento de cada bus en TIEMPO REAL
✅ Muestra ocupación de cada bus
✅ Muestra congestión del sistema
✅ Todo actualizado cada frame
```

**Resultado: Una ventana con buses moviéndose**

```
┌───────────────────────────────────┐
│ 🚌 SIMULACIÓN DE BUSES EN TIEMPO REAL             │
│                                                 │
│   🟢 Bus-001 (😔 Verde)    Ocupación: 35%  │
│   🟡 Bus-002 (😨 Amarillo)   Ocupación: 48%  │
│   🔴 Bus-003 (😴 Rojo)     Ocupación: 52%  │
│                                                 │
│   Congestión Sistema: 45.2%                    │
│   Frame: 125                                    │
│                                                 │
├───────────────────────────────────┤
│ Norte •                       │
│        🚌 Bus-002 (vel 1.2x)  │  Parada
│                       │
│ Centro •---(🚌)---• Este   │  Bus en movimiento
│        🚌 Bus-001 (vel 1.0x)  │  Triángulo = Bus
│                       │
│        🚌 Bus-003 (vel 0.8x)  │
│ Sur •                       │
├───────────────────────────────────┤
│ 🟢 Verde: <30%   🟡 Amarillo: 30-50%   🔴 Rojo: >50%    │
├───────────────────────────────────┤
```

---

### Otras Opciones

**Opción B: Interfaz Gráfica (Botones)**
```bash
python ejecutor_gui.py
```
Aparece ventana con 5 botones para controlar todo.

**Opción C: Sistema Básico (Todo automático)**
```bash
python mini_bus.py
```
Crea sistema, simula, muestra gráficos.

---

## 👉 LO QUE VERÁS EN LA ANIMACIÓN

### ✅ Movimiento PERFECTO

```
Características matemáticas:

1. INTERPOLACIÓN LINEAL: P(t) = P1 + t*(P2 - P1)
   → Movimiento suave y continuo
   → NO saltador
   → Sigue la ruta exactamente

2. DIFERENTES VELOCIDADES
   → Bus-001: Velocidad normal (1.0x)
   → Bus-002: Más rápido (1.2x)
   → Bus-003: Más lento (0.8x)
   → Se ve CLARAMENTE diferente

3. OCUPACIÓN COHERENTE
   → Pasajeros suben/bajan realista
   → No excede capacidad (55 max)
   → Color cambia según ocupación

4. CICLOS COMPLETOS
   → Cada bus completa su ruta
   → Vuelve a empezar
   → Continuo y fluido
```

### 📊 Color de Buses

```
🟢 VERDE:  <30% ocupación (Buena capacidad)
🟡 AMARILLO: 30-50% ocupación (Normal)
🔴 ROJO:   >50% ocupación (Congestionado)
```

### 📦 Información que Muestra

```
En la consola al iniciar:
- Distancia total de cada ruta
- Matriz de distancias entre paradas
- Velocidad de cada bus

En la ventana de animación:
- Número de frame
- Congestión del sistema
- Ocupación de cada bus
- Nombre de paradas
- Leyenda de colores
```

---

## 🚗 ¿Qué Significa "COHERENTE"?

```
✅ Los buses se mueven en línea recta entre paradas
   (Interpolación correcta)

✅ Los tres buses tienen velocidades DIFERENTES
   Bus-002 llega primero (más rápido)
   Bus-001 en medio (normal)
   Bus-003 llega último (más lento)

✅ La ocupación sube/baja naturalmente
   Sin saltos absurdos
   Dentro de rango 5-55 pasajeros

✅ Los ciclos son continuos
   Cuando termina ruta, vuelve a empezar
   Sin reseteos visuales extraños

✅ Todo actualizado cada frame (50ms)
   Animación suave a 20 FPS
```

---

## 📁 ESTRUCTURA DE ARCHIVOS

```
proyecto/
├── mini_bus.py              ✓ Sistema básico
├── ejecutor_gui.py          ✓ Interfaz gráfica
├── animacion_buses.py       ✓ ANIMACIÓN (RECOMENDADO)
├── bus_system_simple.py     (Versión anterior)
├── visualización_interactiva.py  (Versión anterior)
├── MINI_GUIDE.md            ✓ Guía rápida
├── DESCARGAR_EJECUTAR.md    ✓ Este archivo
└── GUIDE_SISTEMA_SIMPLIFICADO.md  (Guía extendida)
```

---

## 🐄 SOLUCIONAR PROBLEMAS

### Error: "ModuleNotFoundError: No module named 'numpy'"
```bash
pip install numpy matplotlib
```

### Error: "Python not found"
Asegúrate de tener Python 3.8+ instalado.
Descarga de: https://www.python.org/

### La animación es muy lenta
Cambia `interval=50` a `interval=100` en `animacion_buses.py`

### La animación es muy rápida
Cambia `interval=50` a `interval=25` en `animacion_buses.py`

### No veo diferencia de velocidades entre buses
Verifica que cada bus tenga diferente valor de `velocidad`:
- Bus-001: velocidad=1.0
- Bus-002: velocidad=1.2  (20% más rápido)
- Bus-003: velocidad=0.8  (20% más lento)

---

## 🎯 PERSONALIZAR

### Agregar más paradas
En `animacion_buses.py`, busca "Agregar paradas":
```python
sistema.agregar_parada(5, "Mi Parada", 4.81, -75.69)
```

### Cambiar velocidad de bus
```python
sistema.agregar_bus(1, "Bus-001", [1, 2, 1], velocidad=1.5)  # Más rápido
```

### Agregar más buses
```python
sistema.agregar_bus(4, "Bus-004", [3, 4, 3], velocidad=1.1)
```

### Cambiar número de frames
```python
animador.ejecutar(frames=500, interval=50)  # Más tiempo de animación
```

---

## 📆 PARA ENTREGAR COMO PROYECTO

```
1. Descargar los 3 archivos:
   ✓ animacion_buses.py
   ✓ mini_bus.py
   ✓ ejecutor_gui.py

2. Crear carpeta "mi_proyecto"

3. Copiar archivos en la carpeta

4. Comprimir carpeta como ZIP

5. Entregar:
   - Archivo ZIP
   - O enlace a GitHub
   - O los 3 archivos .py directamente

6. Profesor ejecuta:
   python animacion_buses.py
   
   (Ve animación perfecta con buses moviéndose)
```

---

## 🔗 ENLACES IMPORTANTES

**GitHub del Proyecto:**
https://github.com/mapache16/proyecto

**Python Download:**
https://www.python.org/downloads/

**NumPy Docs:**
https://numpy.org/doc/stable/

**Matplotlib Docs:**
https://matplotlib.org/stable/contents.html

---

## ✅ VERIFICACIÓN DE INSTALACIÓN

Para verificar que todo está bien:

```bash
# Verificar Python
python --version

# Verificar NumPy
python -c "import numpy; print('NumPy OK')"

# Verificar Matplotlib  
python -c "import matplotlib; print('Matplotlib OK')"

# Ejecutar animación
python animacion_buses.py
```

Si todo imprime "OK" y la animación corre, ¡estás listo!

---

**¿Mas preguntas?** Lee MINI_GUIDE.md o GUIDE_SISTEMA_SIMPLIFICADO.md

🚀 **¡Listo para ejecutar!**
