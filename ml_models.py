"""
🤖 MÓDULO DE MACHINE LEARNING
"""

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from typing import List, Tuple

class PrediccionCongestión:
    """Predice niveles de congestión en rutas"""
    
    def __init__(self):
        self.modelos = {}
        self.scalers = {}
    
    def entrenar_ruta(self, ruta_id: str, 
                     características: np.ndarray, 
                     congestión: np.ndarray):
        """Entrena modelo para ruta específica"""
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(características)
        
        modelo = RandomForestRegressor(n_estimators=50, random_state=42)
        modelo.fit(X_scaled, congestión)
        
        self.modelos[ruta_id] = modelo
        self.scalers[ruta_id] = scaler
    
    def predecir_congestión(self, ruta_id: str, características: np.ndarray) -> np.ndarray:
        """Predice congestión para ruta"""
        if ruta_id not in self.modelos:
            return np.zeros(len(características))
        
        scaler = self.scalers[ruta_id]
        modelo = self.modelos[ruta_id]
        
        X_scaled = scaler.transform(características)
        predicciones = modelo.predict(X_scaled)
        
        return np.clip(predicciones, 0, 100)
    
    @staticmethod
    def obtener_estado(nivel: float) -> str:
        """Convierte nivel a estado descriptivo"""
        if nivel < 25:
            return "🟢 Baja"
        elif nivel < 50:
            return "🟡 Media"
        elif nivel < 75:
            return "🟠 Alta"
        else:
            return "🔴 Crítica"

class ModuloEvaluacionRendimiento:
    """Evalúa rendimiento del transporte"""
    
    @staticmethod
    def calcular_eficiencia_ruta(distancia_km: float,
                                tiempo_real_min: float,
                                velocidad_esperada_kmh: float = 30) -> float:
        """Calcula eficiencia de ruta"""
        tiempo_esperado = (distancia_km / velocidad_esperada_kmh) * 60
        if tiempo_real_min == 0:
            return 0
        eficiencia = (tiempo_esperado / tiempo_real_min) * 100
        return min(eficiencia, 100)
