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
  }, []);

  useEffect(() => {
    const fetchBuses = async () => {
      try {
        const response = await fetch('http://localhost:8000/telemetria');
        const data = await response.json();
        setBuses(data);
      } catch (error) {
        console.error('Error fetching buses:', error);
      }
    };

    fetchBuses();
    const interval = setInterval(fetchBuses, 2000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (map) {
      buses.forEach((bus) => {
        const color = bus.vel > 60 ? '#ff0000' : bus.vel > 40 ? '#ffaa00' : '#00ff00';
        L.circleMarker([bus.lat, bus.lon], {
          radius: 8,
          fillColor: color,
          color: '#000',
          weight: 1,
          opacity: 0.8,
          fillOpacity: 0.6
        })
          .bindPopup(`Bus ${bus.vehiculo_id}<br/>Velocidad: ${bus.vel} km/h`)
          .addTo(map);
      });
    }
  }, [buses, map]);

  return <div id="map" style={{ width: '100%', height: '600px' }} />;
};

export default Map;
