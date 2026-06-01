# 🚌 OPTIMIZADOR DE RUTAS - ÁLGEBRA LINEAL EN ACCIÓN

## 📌 ¿QUÉ ES?

Programa demostrativo que muestra cómo el **Álgebra Lineal** optimiza rutas de transporte cuando ocurren eventos del mundo real (accidentes, lluvia, bloqueos).

---

## 🎯 OBJETIVO

**Demostrar que:**

1. ✅ **El Álgebra Lineal es práctica**
   - Matrices de distancias
   - Algoritmo de Dijkstra
   - Optimización en tiempo real

2. ✅ **Los eventos afectan las rutas**
   - Accidentes ralentizan
   - Lluvia dificulta el tráfico
   - Protestas cierran calles
   - Construcciones desactivan paradas

3. ✅ **El sistema encuentra automáticamente la MEJOR ruta**
   - Evita paradas con eventos
   - Busca caminos alternativos
   - Minimiza tiempo total

---

## 🚀 CÓMO EJECUTAR

```bash
pip install numpy matplotlib
python optimizador_rutas_v2.py
```

---

## 🎮 CÓMO USAR LA INTERFAZ

### Paso 1: Seleccionar Parada
```
1. Observa el mapa en la izquierda
2. HAZ CLICK en una parada (puntos azules)
3. Verás confirmación en la consola
```

### Paso 2: Crear Evento
```
4. A la derecha hay 5 botones
5. CLICK en uno de los eventos:
   🚗💥 Accidente
   🌧️ Lluvia Fuerte  
   🚧 Protesta
   🏗️ Construcción
```

### Paso 3: Observar Cambios
```
6. Mira cómo la ruta VERDE cambia
7. Panel derecho muestra nueva distancia
8. Lee el camino recomendado
```

### Paso 4: Limpiar Eventos
```
9. Click en "✅ Limpiar Todo"
10. Se borran todos los eventos
11. Vuelve a la ruta original
```

---

## 📊 ÁLGEBRA LINEAL EXPLICADA

### 1. MATRIZ DE DISTANCIAS (Base)

```
        Centro  Parque  Comercial  Terminal  Dosq  Galicia
Centro    0     1.28      1.04      0.88     3.45   3.78
Parque    1.28   0        2.15      1.65     4.22   4.55
Comercial 1.04   2.15      0        1.50     2.78   3.10
Terminal  0.88   1.65     1.50       0       2.10   2.45
Dosq      3.45   4.22     2.78      2.10      0     1.10
Galicia   3.78   4.55     3.10      2.45     1.10    0
```

**Esto es una MATRIZ n×n donde:**
- n = número de paradas (6)
- M[i,j] = distancia de parada i a parada j
- Se usa para todos los cálculos

### 2. APLICAR EVENTOS (Modificación de Matriz)

Cuando ocurre un evento **en parada 1**:

```
Event: ACCIDENTE, Severidad: 0.7
Multiplicador: 1 + 0.7*3 = 3.1x más lento

Nueva matriz:
Terminal -> Centro: 0.88 → 2.73 km
Centro -> Parque: 1.28 → 3.97 km
Centro -> Comercial: 1.04 → 3.22 km
```

**La severidad modifica los pesos:**
- 🚗💥 Accidente: +300% (1 + 0.7*3)
- 🌧️ Lluvia: +260% (1 + 0.6*3)
- 🚧 Protesta: +350% (1 + 0.75*3)
- 🏗️ Construcción: +400% (1 + 0.8*3)

### 3. ALGORITMO DE DIJKSTRA (Optimización)

```python
Dijkstra busca el CAMINO MÍNIMO:

Sin eventos: Centro → Dosquebradas → Galicia
Distancia: 7.65 km

Con evento en Centro:
Dijkstra evita Centro y busca alternativa
Nuevo camino: Parque → Terminal → Dosquebradas → Galicia  
Distancia: 9.12 km (pero evita el problema)
```

**Pasos de Dijkstra:**
1. Inicializa distancias en ∞
2. Marca origen con 0
3. Explora nodos vecinos
4. Actualiza distancias menores
5. Marca visitados
6. Repite hasta llegar destino
7. Reconstruye camino

---

## 📌 PARADAS DEL MAPA

```
PEREIRA:
1. Centro Pereira (4.8135, -75.6942) - Corazón de la ciudad
2. Parque Arvi (4.8250, -75.7100) - Norte
3. Centro Comercial (4.8050, -75.6850) - Este
4. Terminal de Autobuses (4.8100, -75.7000) - Sureste

DOSQUEBRADAS:
5. Centro Dosquebradas (4.8000, -75.7200) - Oeste
6. Sector Galicia (4.7900, -75.7150) - Suroeste
```

---

## 🎨 COLORES Y SÍMBOLOS

### Paradas
```
🔵 Azul = Sin eventos
🔴 Rojo = Con evento activo
```

### Rutas
```
�� Verde = Ruta óptima calculada
📍 Triángulo = Puntos de la ruta
```

### Eventos en Mapa
```
🚗💥 Accidente
🌧️ Lluvia
🚧 Protesta
🏗️ Construcción
```

---

## 📈 INFORMACIÓN MOSTRADA

### Panel Derecho
```
📊 INFORMACIÓN DE RUTA ÓPTIMA:
════════════════════════════
📏 Distancia: 7.65 km
⏱️ Tiempo Est.: 0.2 horas (12 min)

🛣️ CAMINO (Dijkstra):
Centro → Dosquebradas → Galicia

✅ Álgebra Lineal Aplicada:
• Matriz de distancias
• Algoritmo de Dijkstra
• Optimización con eventos
```

---

## 🧮 EJEMPLO PASO A PASO

### Escenario 1: SIN EVENTOS
```
Origen: Centro Pereira (ID: 1)
Destino: Sector Galicia (ID: 6)

Ruta óptima encontrada:
Centro → Dosquebradas → Galicia

Distancia: 3.45 + 1.10 = 4.55 km
Tiempo: 0.11 horas ≈ 7 minutos
```

### Escenario 2: CON ACCIDENTE EN CENTRO
```
Accidente en Centro Pereira
Severidad: 70%
Multiplicador: 3.1x

¿Qué pasa?
Ir al Centro = 3.1x más lento

Dijkstra recalcula...

Nueva ruta óptima:
Parque Arvi → Terminal → Dosquebradas → Galicia

Distancia: 1.65 + 2.10 + 1.10 = 4.85 km
Tiempo: 0.12 horas ≈ 7.2 minutos

Conclusión: Ligeramente más largo pero EVITA el accidente ✅
```

### Escenario 3: CON CONSTRUCCIÓN EN DOSQUEBRADAS
```
Construcción en Centro Dosquebradas
Severidad: 80%
Multiplicador: 4x

Ruta debe evitar Dosquebradas

Dijkstra busca alternativas...

Nueva ruta:
Centro → Parque → ... (camino más largo pero posible)

Distancia: 5.2 km
Tiempo: 0.13 horas ≈ 8 minutos
```

---

## 💡 LO QUE DEMUESTRA

### ✅ Álgebra Lineal en Práctica
```
• Matrices: Representación de redes
• Vectores: Cálculo de distancias
• Optimización: Búsqueda de mínimos
• Algoritmos: Dijkstra aplicado
```

### ✅ Problema Real
```
• Eventos inesperados
• Tráfico dinámico
• Necesidad de adaptación
• Solución automática
```

### ✅ Aplicación Práctica
```
• Google Maps
• Waze
• Servicios de delivery
• Logística empresarial
• Sistemas de transporte público
```

---

## 🔧 PERSONALIZAR

### Agregar más paradas
```python
sistema.agregar_parada(7, "Nueva Parada", 4.81, -75.70, "Pereira")
```

### Cambiar severidad de evento
```python
sistema.crear_evento('ACCIDENTE', parada_id=1, severidad=0.9)  # Muy grave
```

### Agregar más autobuses
```python
sistema.agregar_autobus(4, "Autobús Ruta D", [1, 5, 6, 1])
```

---

## 📚 CONCEPTOS MATEMÁTICOS

### Distancia Euclidiana
```
||v|| = √((x₂-x₁)² + (y₂-y₁)²)

Usada para calcular distancia entre coordenadas GPS
```

### Matriz de Adyacencia Ponderada
```
A[i,j] = peso del borde de i a j
En nuestro caso: peso = distancia
```

### Dijkstra - Complejidad
```
O(n²) donde n = número de paradas
Con 6 paradas: ~36 operaciones por cálculo
```

### Optimización
```
Minimizar: Distancia total
Sujeto a: Paradas con eventos tienen peso mayor
Solución: Ruta que evita eventos cuando es posible
```

---

## 🎓 PARA PRESENTACIÓN

**Di esto en tu presentación:**

```
"Este programa demuestra cómo el Álgebra Lineal
sirve para problemas reales.

1. Tenemos una MATRIZ de distancias entre paradas
2. Cuando hay eventos, modificamos los PESOS
3. Usamos DIJKSTRA para encontrar la ruta óptima
4. El sistema se ADAPTA automáticamente

Esto es exactamente lo que usan:
- Google Maps
- Sistemas de transporte
- Logística empresarial

La Matemática no es teoría, ¡es práctica!"
```

---

## ✅ VERIFICACIÓN

Al ejecutar, deberías ver:

```
✅ Sistema inicializado
✅ 6 paradas creadas
✅ 3 autobuses creados
✅ Matrices construidas
✅ Ruta inicial calculada
✅ Interfaz abierta
```

---

**¡Listo para impresionar a tu profesor!** 🎓
