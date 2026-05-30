# 📐 Matemáticas y Álgebra Lineal en AMCO

## Índice
1. [Haversine Distance](#haversine-distance)
2. [Matriz de Rotación](#matriz-de-rotación)
3. [Eigenvalues/Eigenvectors](#eigenvalueseigenvectors)
4. [SVD](#svd-singular-value-decomposition)
5. [Interpolación Polinómica](#interpolación-polinómica)
6. [Regresión Lineal](#regresión-lineal)
7. [Matrices de Distancia](#matrices-de-distancia)
8. [Z-Score](#z-score)

---

## Haversine Distance

### Fórmula
```
d = 2R * arcsin(√[sin²((lat₂-lat₁)/2) + cos(lat₁)*cos(lat₂)*sin²((lon₂-lon₁)/2)])
```

Donde:
- `R` = Radio terrestre (6371 km)
- `lat₁, lon₁` = Coordenadas del punto 1
- `lat₂, lon₂` = Coordenadas del punto 2
- `d` = Distancia en km

### Implementación
```python
import numpy as np
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula distancia entre dos puntos GPS usando Haversine.
    
    Args:
        lat1, lon1: Coordenadas punto 1
        lat2, lon2: Coordenadas punto 2
    
    Returns:
        Distancia en km
    """
    # Convertir a radianes
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Diferencias
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Fórmula de Haversine
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radio terrestre en km
    r = 6371
    
    return c * r
```

### Casos de Uso
- ✅ Cálculo de distancia entre paradas
- ✅ Búsqueda de paradas más cercanas
- ✅ Validación de rutas

---

## Matriz de Rotación

### Fórmula (2D)
```
[x']   [cos(θ)  -sin(θ)] [x]
[y'] = [sin(θ)   cos(θ)] [y]
```

### Implementación
```python
def rotation_matrix_2d(theta):
    """
    Crea matriz de rotación 2D.
    
    Args:
        theta: Ángulo en radianes
    
    Returns:
        Matriz de rotación 2x2
    """
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    
    return np.array([
        [cos_t, -sin_t],
        [sin_t, cos_t]
    ])

def rotate_point(x, y, theta):
    """
    Rota un punto (x, y) por ángulo theta.
    """
    R = rotation_matrix_2d(theta)
    point = np.array([x, y])
    rotated = R @ point
    return rotated[0], rotated[1]
```

### Casos de Uso
- ✅ Orientación de rutas
- ✅ Visualización de direcciones
- ✅ Cálculo de ángulos de giro

---

## Eigenvalues/Eigenvectors

### Concepto
Para una matriz cuadrada A:
```
A*v = λ*v
```

Donde:
- `λ` = Eigenvalue (autovalor)
- `v` = Eigenvector (autovector)

### Implementación
```python
def analyze_congestion_patterns(congestion_matrix):
    """
    Usa eigenvalues para identificar patrones de congestión.
    
    Args:
        congestion_matrix: Matriz de congestión por parada
    
    Returns:
        Eigenvalues y eigenvectors
    """
    eigenvalues, eigenvectors = np.linalg.eig(congestion_matrix)
    
    # Ordenar por importancia
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    return eigenvalues, eigenvectors
```

### Casos de Uso
- ✅ Análisis de congestión
- ✅ Identificación de patrones principales
- ✅ Reducción de dimensionalidad

---

## SVD (Singular Value Decomposition)

### Fórmula
```
A = U * Σ * V^T
```

Donde:
- `U` = Matriz ortogonal (m x m)
- `Σ` = Matriz diagonal con valores singulares
- `V^T` = Transpuesta de matriz ortogonal (n x n)

### Implementación
```python
def compress_telemetry_data(telemetry_matrix, components=20):
    """
    Comprime datos de telemetría usando SVD.
    
    Args:
        telemetry_matrix: Matriz de telemetría (m x n)
        components: Número de componentes principales
    
    Returns:
        Datos comprimidos
    """
    # Aplicar SVD
    U, s, Vt = np.linalg.svd(telemetry_matrix, full_matrices=False)
    
    # Mantener solo los primeros 'components'
    U_reduced = U[:, :components]
    s_reduced = np.diag(s[:components])
    Vt_reduced = Vt[:components, :]
    
    # Reconstruir matriz comprimida
    compressed = U_reduced @ s_reduced @ Vt_reduced
    
    # Calcular tasa de compresión
    original_size = telemetry_matrix.size
    compressed_size = U_reduced.size + s_reduced.size + Vt_reduced.size
    compression_ratio = compressed_size / original_size
    
    return {
        'datos_comprimidos': compressed,
        'ratio_compresion': compression_ratio,
        'energia_retenida': np.sum(s_reduced**2) / np.sum(s**2)
    }
```

### Casos de Uso
- ✅ Compresión de datos de telemetría
- ✅ Análisis de patrones de viaje
- ✅ Reducción de almacenamiento

---

## Interpolación Polinómica

### Concepto
Encuentra un polinomio que pasa por puntos dados:
```
P(x) = a₀ + a₁x + a₂x² + ... + aₙxⁿ
```

### Implementación
```python
def interpolate_route(waypoints, num_points=100):
    """
    Interpola ruta entre puntos de paso.
    
    Args:
        waypoints: Lista de (lat, lon) puntos
        num_points: Número de puntos de interpolación
    
    Returns:
        Lista interpolada de puntos
    """
    lats = np.array([p[0] for p in waypoints])
    lons = np.array([p[1] for p in waypoints])
    
    # Índices originales
    x_original = np.arange(len(waypoints))
    
    # Crear índices interpolados
    x_interp = np.linspace(0, len(waypoints)-1, num_points)
    
    # Interpolación polinómica (spline cúbico)
    lat_interp = np.interp(x_interp, x_original, lats)
    lon_interp = np.interp(x_interp, x_original, lons)
    
    return list(zip(lat_interp, lon_interp))
```

### Casos de Uso
- ✅ Suavizado de rutas
- ✅ Generación de trayectorias intermedias
- ✅ Visualización de rutas

---

## Regresión Lineal

### Fórmula
```
y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε
```

Donde:
- `β` = Coeficientes de regresión
- `ε` = Error (residual)

### Implementación
```python
def predict_travel_time(distance_km, time_hour):
    """
    Predice tiempo de viaje usando regresión lineal.
    
    Args:
        distance_km: Distancia en km
        time_hour: Hora del día (0-23)
    
    Returns:
        Tiempo estimado en minutos
    """
    from sklearn.linear_model import LinearRegression
    
    # Datos de entrenamiento (ejemplo)
    X = np.array([
        [5, 8],   # 5 km, hora 8
        [10, 8],  # 10 km, hora 8
        [5, 17],  # 5 km, hora 17
        [10, 17]  # 10 km, hora 17
    ])
    
    y = np.array([15, 30, 12, 28])  # Tiempos en minutos
    
    # Crear y entrenar modelo
    model = LinearRegression()
    model.fit(X, y)
    
    # Predecir
    prediccion = model.predict([[distance_km, time_hour]])[0]
    
    return {
        'tiempo_predicho_min': round(prediccion, 1),
        'coeficientes': model.coef_,
        'intercepcion': model.intercept_
    }
```

### Casos de Uso
- ✅ Predicción de tiempos de viaje
- ✅ Estimación de demanda
- ✅ Análisis de tendencias

---

## Matrices de Distancia

### Distancia Euclidiana
```
d(x₁, x₂) = √[Σ(xᵢ - yᵢ)²]
```

### Implementación
```python
def distance_matrix_euclidean(points):
    """
    Calcula matriz de distancias Euclidianas.
    
    Args:
        points: Matriz (n x 2) con coordenadas
    
    Returns:
        Matriz (n x n) de distancias
    """
    from scipy.spatial.distance import cdist
    
    # Calcular distancias
    distances = cdist(points, points, metric='euclidean')
    
    return distances

def nearest_stops(point, all_stops, k=5):
    """
    Encuentra las k paradas más cercanas.
    
    Args:
        point: Coordenada de referencia (lat, lon)
        all_stops: Array de todas las paradas
        k: Número de paradas a retornar
    
    Returns:
        k paradas más cercanas
    """
    from scipy.spatial.distance import cdist
    
    # Calcular distancias
    distances = cdist([point], all_stops, metric='euclidean')[0]
    
    # Encontrar índices de k menores
    nearest_indices = np.argsort(distances)[:k]
    
    return all_stops[nearest_indices]
```

### Casos de Uso
- ✅ Búsqueda de paradas cercanas
- ✅ Agrupamiento de paradas
- ✅ Optimización de rutas

---

## Z-Score

### Fórmula
```
z = (x - μ) / σ
```

Donde:
- `x` = Valor individual
- `μ` = Media
- `σ` = Desviación estándar
- `z` = Z-score

### Implementación
```python
def detect_anomalies(velocidades, threshold=2.5):
    """
    Detecta velocidades anómalas usando Z-score.
    
    Args:
        velocidades: Array de velocidades
        threshold: Umbral de Z-score (default: 2.5)
    
    Returns:
        Índices de velocidades anómalas
    """
    # Calcular media y std
    mean = np.mean(velocidades)
    std = np.std(velocidades)
    
    # Calcular Z-scores
    z_scores = np.abs((velocidades - mean) / std)
    
    # Encontrar anomalías
    anomalies = np.where(z_scores > threshold)[0]
    
    return {
        'indices_anomalos': anomalies.tolist(),
        'velocidades_anomalas': velocidades[anomalies].tolist(),
        'z_scores': z_scores[anomalies].tolist(),
        'media': mean,
        'desv_estandar': std
    }
```

### Casos de Uso
- ✅ Detección de exceso de velocidad
- ✅ Identificación de comportamientos inusuales
- ✅ Alertas automáticas

---

## 📊 Tabla Comparativa de Complejidades

| Operación | Complejidad | Memoria | Casos de Uso |
|-----------|-------------|---------|---------------|
| Haversine | O(1) | O(1) | Distancias GPS |
| Eigenvectors | O(n³) | O(n²) | Análisis de patrones |
| SVD | O(n³) | O(n²) | Compresión de datos |
| Interpolación | O(n log n) | O(n) | Suavizado de rutas |
| Regresión | O(n²) | O(n) | Predicciones |
| Euclidiana | O(n²) | O(n²) | Búsquedas espaciales |
| Z-Score | O(n) | O(n) | Detección anomalías |

---

## 🔗 Referencias Matemáticas

- **Álgebra Lineal**: 3Blue1Brown - Linear Algebra
- **Haversine**: Wikipedia - Haversine formula
- **SVD**: Stanford CS168 - Modern Algorithms
- **Regresión**: Intro to Statistical Learning

---

**Última actualización:** 2026-05-30  
**Precisión Numérica:** IEEE 754 (64-bit)