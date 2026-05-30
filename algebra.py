"""
📐 MÓDULO DE ÁLGEBRA LINEAL AVANZADA
Implementa operaciones matemáticas para transporte metropolitano
"""

import numpy as np
from scipy.spatial.distance import cdist
from scipy.linalg import eig
from sklearn.preprocessing import StandardScaler
import pandas as pd
from typing import Tuple, List

class AlgebraTransporte:
    """Operaciones avanzadas de álgebra lineal para optimización de rutas"""
    
    @staticmethod
    def haversine_distance(coords1: np.ndarray, coords2: np.ndarray) -> float:
        """
        Calcula distancia GPS entre dos puntos usando fórmula Haversine
        
        Args:
            coords1: [lat, lon]
            coords2: [lat, lon]
        
        Returns:
            Distancia en km
        """
        lat1, lon1 = coords1
        lat2, lon2 = coords2
        
        R = 6371  # Radio tierra en km
        
        dlat = np.radians(lat2 - lat1)
        dlon = np.radians(lon2 - lon1)
        
        a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        
        return R * c
    
    @staticmethod
    def matriz_distancias_haversine(paradas: List[Tuple[float, float]]) -> np.ndarray:
        """Crea matriz de distancias GPS entre paradas"""
        n = len(paradas)
        matriz = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    matriz[i][j] = AlgebraTransporte.haversine_distance(paradas[i], paradas[j])
        
        return matriz
    
    @staticmethod
    def z_score_anomalias(datos: np.ndarray, umbral: float = 3.0) -> Tuple[np.ndarray, np.ndarray]:
        """Detección de anomalías usando Z-score"""
        media = np.mean(datos)
        std = np.std(datos)
        
        z_scores = np.abs((datos - media) / std)
        anomalias = z_scores > umbral
        
        return np.where(anomalias)[0], z_scores
    
    @staticmethod
    def regresion_lineal_tiempo(distancias: np.ndarray, tiempos: np.ndarray) -> Tuple[float, float, float]:
        """Regresión lineal para predecir tiempo de viaje"""
        n = len(distancias)
        x_mean = np.mean(distancias)
        y_mean = np.mean(tiempos)
        
        numerator = np.sum((distancias - x_mean) * (tiempos - y_mean))
        denominator = np.sum((distancias - x_mean) ** 2)
        
        m = numerator / denominator if denominator != 0 else 0
        b = y_mean - m * x_mean
        
        ss_tot = np.sum((tiempos - y_mean) ** 2)
        ss_res = np.sum((tiempos - (m * distancias + b)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        return m, b, r_squared
