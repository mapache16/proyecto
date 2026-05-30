# 🗺️ Guía de Mapas Interactivos - AMCO

## 1. Introducción

Esta guía cubre la implementación de mapas interactivos en AMCO usando:
- **Pydeck** - Mapas 3D para Streamlit
- **Leaflet/Mapbox** - Mapas en React
- **Plotly** - Visualización de datos geoespaciales

---

## 2. Mapas con Pydeck (Streamlit)

### 2.1 Mapa Básico

```python
import pydeck as pdk
import streamlit as st

# Coordenadas de ejemplo
lat_inicial = 4.8156
lon_inicial = -75.6951

# Crear mapa
mapa = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=lat_inicial,
        longitude=lon_inicial,
        zoom=13,
        pitch=45
    ),
    layers=[]
)

st.pydeck_chart(mapa)
```

---

### 2.2 Capa de Hexágonos (Densidad de Buses)

```python
import pandas as pd
import pydeck as pdk

# Datos de buses
buses_data = pd.DataFrame([
    {'lat': 4.8156, 'lon': -75.6951, 'pasajeros': 45},
    {'lat': 4.8160, 'lon': -75.6955, 'pasajeros': 32},
    {'lat': 4.8150, 'lon': -75.6945, 'pasajeros': 28}
])

# Capa hexagonal
hexagon_layer = pdk.Layer(
    'HexagonLayer',
    data=buses_data,
    get_position=['lon', 'lat'],
    radius=200,
    elevation_scale=4,
    elevation_range=[0, 1000],
    pickable=True,
    extruded=True,
    colorRange=[
        [0, 255, 0],      # Verde (bajo)
        [255, 255, 0],    # Amarillo (medio)
        [255, 0, 0]       # Rojo (alto)
    ]
)

mapa = pdk.Deck(
    layers=[hexagon_layer],
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=4.8156,
        longitude=-75.6951,
        zoom=13,
        pitch=45
    )
)

st.pydeck_chart(mapa)
```

---

### 2.3 Capa de Puntos (Ubicaciones de Paradas)

```python
import pydeck as pdk
import pandas as pd

# Datos de paradas
paradas_data = pd.DataFrame([
    {'lat': 4.8156, 'lon': -75.6951, 'nombre': 'Centro', 'personas': 45},
    {'lat': 4.8160, 'lon': -75.6955, 'nombre': 'Parque', 'personas': 32},
    {'lat': 4.8150, 'lon': -75.6945, 'nombre': 'Hospital', 'personas': 28}
])

# Función para determinar color por congestión
def get_color(personas):
    if personas < 20:
        return [0, 255, 0]      # Verde
    elif personas < 40:
        return [255, 255, 0]    # Amarillo
    else:
        return [255, 0, 0]      # Rojo

paradas_data['color'] = paradas_data['personas'].apply(
    lambda p: get_color(p)
)

# Capa de puntos
points_layer = pdk.Layer(
    'ScatterplotLayer',
    data=paradas_data,
    get_position=['lon', 'lat'],
    get_color='color',
    get_radius=200,
    pickable=True
)

mapa = pdk.Deck(
    layers=[points_layer],
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=4.8156,
        longitude=-75.6951,
        zoom=13
    )
)

st.pydeck_chart(mapa)
```

---

### 2.4 Capa de Rutas (Paths)

```python
import pydeck as pdk
import pandas as pd

# Coordenadas de ruta
ruta_coords = [
    [[-75.6951, 4.8156],  # Punto 1
     [-75.6945, 4.8160],  # Punto 2
     [-75.6940, 4.8165]]  # Punto 3
]

ruta_data = pd.DataFrame([
    {'path': ruta_coords[0], 'nombre': 'Ruta Centro-Pereira'}
])

# Capa de rutas
paths_layer = pdk.Layer(
    'PathLayer',
    data=ruta_data,
    get_path='path',
    get_color=[255, 0, 0],
    width_scale=20,
    width_min_pixels=2,
    pickable=True
)

mapa = pdk.Deck(
    layers=[paths_layer],
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=4.8156,
        longitude=-75.6951,
        zoom=13
    )
)

st.pydeck_chart(mapa)
```

---

## 3. Heat Maps con Plotly

### 3.1 Mapa de Calor de Paradas

```python
import plotly.express as px
import pandas as pd

# Datos de paradas
paradas = pd.DataFrame([
    {'nombre': 'Centro', 'lat': 4.8156, 'lon': -75.6951, 'personas': 45},
    {'nombre': 'Parque', 'lat': 4.8160, 'lon': -75.6955, 'personas': 32},
    {'nombre': 'Hospital', 'lat': 4.8150, 'lon': -75.6945, 'personas': 28},
    {'nombre': 'Terminal', 'lat': 4.8145, 'lon': -75.6940, 'personas': 55}
])

# Heat map
fig = px.density_mapbox(
    paradas,
    lat='lat',
    lon='lon',
    z='personas',
    radius=10,
    center=dict(lat=4.8156, lon=-75.6951),
    zoom=13,
    mapbox_style="open-street-map",
    color_continuous_scale='Viridis',
    hover_data=['nombre', 'personas']
)

fig.update_layout(
    title='Mapa de Calor - Demanda por Parada',
    height=600
)

fig.show()
```

---

### 3.2 Scatter Map con Tamaño Variable

```python
import plotly.express as px
import pandas as pd

# Datos de buses en tiempo real
buses = pd.DataFrame([
    {'id': 1, 'lat': 4.8156, 'lon': -75.6951, 'pasajeros': 45, 'velocidad': 35},
    {'id': 2, 'lat': 4.8160, 'lon': -75.6955, 'pasajeros': 32, 'velocidad': 40},
    {'id': 3, 'lat': 4.8150, 'lon': -75.6945, 'pasajeros': 28, 'velocidad': 25}
])

# Mapa de scatter
fig = px.scatter_mapbox(
    buses,
    lat='lat',
    lon='lon',
    size='pasajeros',
    color='velocidad',
    hover_name='id',
    hover_data=['pasajeros', 'velocidad'],
    color_continuous_scale='Viridis',
    size_max=50,
    zoom=13,
    center=dict(lat=4.8156, lon=-75.6951),
    mapbox_style="open-street-map"
)

fig.update_layout(
    title='Ubicación de Buses en Tiempo Real',
    height=600
)

fig.show()
```

---

## 4. Componentes React

### 4.1 Componente Map.jsx con Leaflet

```jsx
import React, { useEffect, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const Map = () => {
  const [map, setMap] = useState(null);
  const [buses, setBuses] = useState([]);

  useEffect(() => {
    // Inicializar mapa
    const mapInstance = L.map('map').setView([4.8156, -75.6951], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(mapInstance);

    setMap(mapInstance);

    return () => mapInstance.remove();
  }, []);

  useEffect(() => {
    // Obtener datos de buses
    const fetchBuses = async () => {
      const response = await fetch('http://localhost:8000/telemetria');
      const data = await response.json();
      setBuses(data);
    };

    fetchBuses();
    const interval = setInterval(fetchBuses, 2000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (map) {
      // Agregar marcadores
      buses.forEach((bus) => {
        const marker = L.circleMarker([bus.lat, bus.lon], {
          radius: 8,
          fillColor: bus.vel > 50 ? '#ff0000' : '#00ff00',
          color: '#000',
          weight: 1,
          opacity: 0.8,
          fillOpacity: 0.6
        });

        marker.bindPopup(`
          <b>Bus ${bus.vehiculo_id}</b><br/>
          Placa: ${bus.placa}<br/>
          Velocidad: ${bus.vel} km/h<br/>
          Pasajeros: ${bus.pasajeros}
        `);

        marker.addTo(map);
      });
    }
  }, [buses, map]);

  return <div id="map" style={{ width: '100%', height: '600px' }} />;
};

export default Map;
```

---

### 4.2 Componente HeatMap.jsx

```jsx
import React, { useEffect, useState } from 'react';
import L from 'leaflet';
import 'leaflet-heat';
import 'leaflet/dist/leaflet.css';

const HeatMap = () => {
  const [map, setMap] = useState(null);

  useEffect(() => {
    const mapInstance = L.map('heatmap').setView([4.8156, -75.6951], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(mapInstance);
    setMap(mapInstance);
  }, []);

  useEffect(() => {
    if (map) {
      const fetchHeatData = async () => {
        const response = await fetch('http://localhost:8000/mapa-calor/paradas');
        const data = await response.json();

        const heatPoints = data.mapa_calor.map((parada) => [
          parada.latitud,
          parada.longitud,
          parada.intensidad * 100
        ]);

        L.heatLayer(heatPoints, {
          radius: 25,
          blur: 15,
          maxZoom: 17
        }).addTo(map);
      };

      fetchHeatData();
    }
  }, [map]);

  return <div id="heatmap" style={{ width: '100%', height: '600px' }} />;
};

export default HeatMap;
```

---

## 5. Semáforos de Congestión

### 5.1 Componente TrafficLight.jsx

```jsx
import React, { useEffect, useState } from 'react';
import './TrafficLight.css';

const TrafficLight = () => {
  const [congestiones, setCongestiones] = useState({});

  useEffect(() => {
    const fetchCongestion = async () => {
      const response = await fetch('http://localhost:8000/congestión/por-ruta');
      const data = await response.json();
      setCongestiones(data.congestiones);
    };

    fetchCongestion();
    const interval = setInterval(fetchCongestion, 5000);

    return () => clearInterval(interval);
  }, []);

  const getColor = (congestion) => {
    if (congestion < 50) return 'green';
    if (congestion < 75) return 'yellow';
    if (congestion < 90) return 'orange';
    return 'red';
  };

  return (
    <div className="traffic-lights">
      {Object.entries(congestiones).map(([nombre, datos]) => (
        <div key={nombre} className="traffic-light-item">
          <div className={`light ${getColor(datos.congestion_porcentaje)}`} />
          <div className="label">
            <p>{nombre}</p>
            <p>{datos.congestion_porcentaje.toFixed(1)}%</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default TrafficLight;
```

### 5.2 TrafficLight.css

```css
.traffic-lights {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  padding: 20px;
}

.traffic-light-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.light {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  animation: pulse 1s infinite;
}

.light.green {
  background-color: #4caf50;
  box-shadow: 0 0 20px rgba(76, 175, 80, 0.8);
}

.light.yellow {
  background-color: #ffc107;
  box-shadow: 0 0 20px rgba(255, 193, 7, 0.8);
}

.light.orange {
  background-color: #ff9800;
  box-shadow: 0 0 20px rgba(255, 152, 0, 0.8);
}

.light.red {
  background-color: #f44336;
  box-shadow: 0 0 20px rgba(244, 67, 54, 0.8);
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.label {
  text-align: center;
}

.label p {
  margin: 0;
  font-weight: bold;
}
```

---

## 6. Mejores Prácticas

✅ **Usar caché** para no recalcular constantemente  
✅ **Limitar zoom** para no sobrecargar  
✅ **Actualizar cada 2-5 segundos** en tiempo real  
✅ **Usar clusters** para muchos puntos  
✅ **Colores intuitivos**: Rojo = Crítico, Verde = Normal  
✅ **Incluir tooltips** con información adicional  

---

**Última actualización:** 2026-05-30