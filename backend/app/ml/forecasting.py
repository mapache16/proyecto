"""Modelos de predicción de demanda para AMCO."""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor


def forecast_demand(historical_data, hours_ahead=24):
    """
    Predice demanda futura basada en datos históricos.
    
    Args:
        historical_data: Array de demanda histórica
        hours_ahead: Horas a predecir
    
    Returns:
        Predicciones de demanda
    """
    # Preparar datos
    X = np.arange(len(historical_data)).reshape(-1, 1)
    y = historical_data
    
    # Entrenar modelo
    model = LinearRegression()
    model.fit(X, y)
    
    # Predecir
    future_X = np.arange(len(historical_data), len(historical_data) + hours_ahead).reshape(-1, 1)
    predictions = model.predict(future_X)
    
    # Asegurar valores no negativos
    predictions = np.maximum(predictions, 0)
    
    return {
        'predicciones': predictions,
        'horas': hours_ahead,
        'modelo': 'LinearRegression'
    }


def forecast_demand_by_route(route_id, historical_demand, day_of_week):
    """
    Predice demanda específica por ruta y día.
    
    Args:
        route_id: ID de la ruta
        historical_demand: Demanda histórica por hora
        day_of_week: Día de la semana (0-6)
    
    Returns:
        Predicción de demanda
    """
    # Características: hora_del_día, día_semana, demanda_histórica
    X = np.array([
        [h, day_of_week, historical_demand[h % 24]] 
        for h in range(24)
    ])
    
    y = historical_demand[:24]
    
    # Entrenar Random Forest
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return {
        'importancias': model.feature_importances_,
        'modelo_entrenado': True
    }
