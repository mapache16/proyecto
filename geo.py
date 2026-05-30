"""
🗺️ MÓDULO GEOESPACIAL AVANZADO
"""

import numpy as np
from typing import List, Tuple, Dict
from algebra import AlgebraTransporte
import warnings

warnings.filterwarnings('ignore')

class GeoEspacial:
    """Operaciones geoespaciales avanzadas"""
    
    @staticmethod
    def punto_en_poligono(punto: Tuple[float, float], poligono: List[Tuple[float, float]]) -> bool:
        """Determina si un punto está dentro de un polígono"""
        x, y = punto
        n = len(poligono)
        dentro = False
        
        p1x, p1y = poligono[0]
        for i in range(1, n + 1):
            p2x, p2y = poligono[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            dentro = not dentro
            p1x, p1y = p2x, p2y
        
        return dentro
    
    @staticmethod
    def paradas_proximas(punto: Tuple[float, float], 
                        paradas: List[Tuple[float, float]], 
                        radio_km: float = 1.0) -> List[Tuple[int, float]]:
        """Encuentra paradas más cercanas"""
        distancias = []
        
        for i, parada in enumerate(paradas):
            dist = AlgebraTransporte.haversine_distance(punto, parada)
            if dist <= radio_km:
                distancias.append((i, dist))
        
        distancias.sort(key=lambda x: x[1])
        return distancias[:5]
    
    @staticmethod
    def heatmap_densidad(puntos: List[Tuple[float, float]], 
                        gridsize: int = 10) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Crea mapa de calor de densidad"""
        puntos_array = np.array(puntos)
        
        lats = puntos_array[:, 0]
        lons = puntos_array[:, 1]
        
        lat_min, lat_max = lats.min(), lats.max()
        lon_min, lon_max = lons.min(), lons.max()
        
        lat_bins = np.linspace(lat_min, lat_max, gridsize)
        lon_bins = np.linspace(lon_min, lon_max, gridsize)
        
        densidad, _, _ = np.histogram2d(lats, lons, bins=[lat_bins, lon_bins])
        X, Y = np.meshgrid(lat_bins[:-1], lon_bins[:-1], indexing='ij')
        
        return X, Y, densidad
