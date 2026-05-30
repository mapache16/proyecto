# 📚 Documentación de API - AMCO

## Base URL
```
http://localhost:8000/api/v1
```

## Autenticación

Todos los endpoints (excepto `/auth/*`) requieren:
```
Authorization: Bearer {access_token}
```

---

## 🔐 Endpoints de Autenticación

### 1. Registrar Usuario
```http
POST /auth/register
```

**Body:**
```json
{
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "contraseña": "SecurePass123!",
  "rol": "usuario"
}
```

**Response (201):**
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "rol": "usuario",
  "fecha_creacion": "2026-05-30T10:30:00Z"
}
```

---

### 2. Login
```http
POST /auth/login
```

**Body:**
```json
{
  "email": "juan@example.com",
  "contraseña": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

### 3. Refrescar Token
```http
POST /auth/refresh
```

**Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

## 🚌 Endpoints de Buses

### 1. Listar Todos los Buses
```http
GET /buses?estado=activo&pagina=1&limite=10
```

**Query Parameters:**
- `estado` (optional): activo, inactivo, mantenimiento
- `pagina` (optional): Número de página (default: 1)
- `limite` (optional): Resultados por página (default: 10)

**Response (200):**
```json
{
  "buses": [
    {
      "id": 1,
      "placa": "ABC-123",
      "capacidad": 50,
      "tipo_motor": "Diesel",
      "estado_mecanico": "Bueno",
      "estado_operacion": "activo",
      "ruta_asignada_id": 5
    }
  ],
  "total": 150,
  "pagina": 1,
  "total_paginas": 15
}
```

---

### 2. Obtener Bus Específico
```http
GET /buses/{id}
```

**Response (200):**
```json
{
  "id": 1,
  "placa": "ABC-123",
  "capacidad": 50,
  "tipo_motor": "Diesel",
  "estado_mecanico": "Bueno",
  "estado_operacion": "activo",
  "ruta_asignada_id": 5,
  "telemetria": {
    "velocidad_kmh": 45.3,
    "nivel_energia": 87.5,
    "pasajeros_a_bordo": 32,
    "latitud": 4.8156,
    "longitud": -75.6951,
    "ultima_actualizacion": "2026-05-30T10:45:30Z"
  },
  "alertas_activas": 0
}
```

---

### 3. Crear Bus (Admin)
```http
POST /buses
```

**Body:**
```json
{
  "placa": "XYZ-789",
  "capacidad": 50,
  "tipo_motor": "Diesel",
  "estado_mecanico": "Bueno",
  "marca": "Volvo",
  "modelo": "B370"
}
```

**Response (201):**
```json
{
  "id": 151,
  "placa": "XYZ-789",
  "capacidad": 50,
  "tipo_motor": "Diesel",
  "mensaje": "Bus creado exitosamente"
}
```

---

### 4. Actualizar Bus
```http
PUT /buses/{id}
```

**Body:**
```json
{
  "estado_mecanico": "Mantenimiento",
  "ruta_asignada_id": 6
}
```

**Response (200):**
```json
{
  "id": 1,
  "mensaje": "Bus actualizado exitosamente"
}
```

---

## 🛣️ Endpoints de Rutas

### 1. Listar Rutas
```http
GET /rutas?estado=activa&demanda_minima=50
```

**Response (200):**
```json
{
  "rutas": [
    {
      "id": 5,
      "nombre": "Ruta Centro-Pereira",
      "codigo_ruta": "C-01",
      "distancia_km": 12.5,
      "tiempo_estimado_min": 45,
      "demanda_promedio": 325,
      "estado": "activa",
      "paradas_total": 8,
      "tarifa_base": 2500
    }
  ],
  "total": 45
}
```

---

### 2. Obtener Ruta Específica
```http
GET /rutas/{id}
```

**Response (200):**
```json
{
  "id": 5,
  "nombre": "Ruta Centro-Pereira",
  "codigo_ruta": "C-01",
  "distancia_km": 12.5,
  "tiempo_estimado_min": 45,
  "demanda_promedio": 325,
  "paradas": [
    {
      "id": 1,
      "nombre": "Centro",
      "latitud": 4.8156,
      "longitud": -75.6951,
      "orden": 1
    }
  ],
  "buses_asignados": 3,
  "congestión_actual": "media"
}
```

---

### 3. Calcular Ruta Óptima (Dijkstra)
```http
GET /rutas/optima?origen_id=1&destino_id=10
```

**Response (200):**
```json
{
  "distancia_km": 8.5,
  "tiempo_estimado_min": 22,
  "paradas_ids": [1, 3, 5, 10],
  "paradas_nombres": ["Centro", "Parque", "Hospital", "Terminal"],
  "num_paradas": 4
}
```

---

## 📊 Endpoints de Analytics

### 1. Predicción de Demanda
```http
GET /analytics/prediccion?ruta_id=5&hora_inicio=6&hora_fin=22
```

**Response (200):**
```json
{
  "ruta_id": 5,
  "rango": "6:00 a 22:00",
  "pasajeros_esperados": 2145,
  "desglose": {
    "6:00": 120,
    "7:00": 250,
    "8:00": 350,
    "...": "..."
  }
}
```

---

### 2. Estado de Congestión
```http
GET /analytics/congestion
```

**Response (200):**
```json
{
  "congestiones": {
    "Ruta Centro-Pereira": {
      "ruta_id": 5,
      "num_buses": 3,
      "capacidad_total": 150,
      "pasajeros_total": 98,
      "congestion_porcentaje": 65.3,
      "estado": "🟡 MEDIA"
    }
  },
  "timestamp": "2026-05-30T10:45:30Z"
}
```

---

### 3. Salud de la Flota
```http
GET /analytics/salud/flota
```

**Response (200):**
```json
{
  "salud_general": "🟢 EXCELENTE",
  "estados_resumido": {
    "VERDE": 120,
    "AMARILLO": 20,
    "ROJO": 5
  },
  "porcentaje_verde": 82.2,
  "total_buses": 145,
  "timestamp": "2026-05-30T10:45:30Z"
}
```

---

### 4. Salud de Bus Específico
```http
GET /analytics/salud/bus/{id}
```

**Response (200):**
```json
{
  "vehiculo_id": 1,
  "placa": "ABC-123",
  "salud_actual": "🟢 NORMAL",
  "alertas_activas": 0,
  "telemetria": {
    "velocidad_kmh": 45.3,
    "nivel_energia": 87.5,
    "pasajeros_a_bordo": 32
  }
}
```

---

### 5. Mapa de Calor de Paradas
```http
GET /analytics/mapa-calor/paradas
```

**Response (200):**
```json
{
  "mapa_calor": [
    {
      "parada_id": 1,
      "nombre": "Centro",
      "latitud": 4.8156,
      "longitud": -75.6951,
      "personas_esperando": 45,
      "intensidad": 0.95,
      "categoria": "🔴 ALTA"
    }
  ],
  "max_personas": 47,
  "timestamp": "2026-05-30T10:45:30Z"
}
```

---

## ⚠️ Endpoints de Alertas

### 1. Obtener Alertas Activas
```http
GET /alertas/activas?limite=50&tipo=EXCESO_VELOCIDAD
```

**Response (200):**
```json
{
  "alertas": [
    {
      "alerta_id": 1,
      "vehiculo_id": 5,
      "placa": "XYZ-789",
      "tipo_alerta": "EXCESO_VELOCIDAD",
      "descripcion": "Velocidad: 95.5 km/h",
      "fecha": "2026-05-30T10:40:00Z",
      "severidad": "🔴 CRÍTICA"
    }
  ],
  "total": 1
}
```

---

### 2. Crear Incidente
```http
POST /incidentes
```

**Body:**
```json
{
  "vehiculo_id": 5,
  "descripcion": "Accidente en Cra. 10 con Cll. 19",
  "ubicacion": {"lat": 4.8156, "lon": -75.6951}
}
```

**Response (201):**
```json
{
  "id": 1,
  "status": "Incidente reportado exitosamente",
  "timestamp": "2026-05-30T10:45:00Z"
}
```

---

## ✅ Códigos de Respuesta

| Código | Significado |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - Token inválido |
| 403 | Forbidden - Sin permisos |
| 404 | Not Found - Recurso no encontrado |
| 500 | Server Error - Error interno |

---

## 🔄 WebSocket

### Conexión en Tiempo Real
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/telemetria');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Actualización:', data);
};
```

---

## 📝 Ejemplo de Uso Completo

```bash
# 1. Registrarse
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan",
    "email": "juan@test.com",
    "contraseña": "Pass123!",
    "rol": "usuario"
  }'

# 2. Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@test.com",
    "contraseña": "Pass123!"
  }'

# 3. Usar token
curl -X GET http://localhost:8000/buses \
  -H "Authorization: Bearer {access_token}"
```

---

**Última actualización:** 2026-05-30  
**API Version:** 1.0