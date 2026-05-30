"""Detección de anomalías para AMCO."""

import numpy as np
from sklearn.ensemble import IsolationForest
from scipy import stats


def detect_speed_anomalies(velocities, threshold=2.5):
    """
    Detecta velocidades anómalas usando Z-score.
    
    Args:
        velocities: Array de velocidades
        threshold: Umbral de Z-score
    
    Returns:
        Índices de anomalías detectadas
    """
    z_scores = np.abs(stats.zscore(velocities))
    anomalies = np.where(z_scores > threshold)[0]
    
    return {
        'indices_anomalos': anomalies.tolist(),
        'velocidades_anomalas': velocities[anomalies].tolist(),
        'z_scores': z_scores[anomalies].tolist()
    }


def detect_behavior_anomalies(behavior_data):
    """
    Detecta comportamientos inusuales usando Isolation Forest.
    
    Args:
        behavior_data: Array de características de comportamiento
    
    Returns:
        Predicciones de anomalía (-1: anomalía, 1: normal)
    """
    model = IsolationForest(contamination=0.1, random_state=42)
    predictions = model.fit_predict(behavior_data)
    
    anomaly_scores = model.score_samples(behavior_data)
    
    return {
        'predicciones': predictions.tolist(),
        'scores': anomaly_scores.tolist(),
        'anomalias_detectadas': np.sum(predictions == -1)
    }


def detect_route_anomalies(route_telemetry, expected_duration):
    """
    Detecta anomalías en rutas (retrasos inusuales).
    
    Args:
        route_telemetry: Datos de telemetría de la ruta
        expected_duration: Duración esperada en minutos
    
    Returns:
        Alertas de anomalías
    """
    actual_duration = route_telemetry.get('duracion_real', 0)
    deviation = abs(actual_duration - expected_duration) / expected_duration
    
    if deviation > 0.3:  # 30% de desviación
        return {
            'anomalia_detectada': True,
            'tipo': 'retraso_inusual' if actual_duration > expected_duration else 'adelanto_inusual',
            'desviacion_porcentaje': round(deviation * 100, 2),
            'severidad': 'alta' if deviation > 0.5 else 'media'
        }
    
    return {'anomalia_detectada': False}
