"""Modelos de clustering para AMCO."""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def cluster_stops(stops_data, n_clusters=5):
    """
    Agrupa paradas por similaridad de demanda.
    
    Args:
        stops_data: Array de características (lat, lon, demanda)
        n_clusters: Número de clusters
    
    Returns:
        Labels de clusters y centroides
    """
    # Normalizar datos
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(stops_data)
    
    # Aplicar K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(data_scaled)
    
    # Desnormalizar centroides
    centroids = scaler.inverse_transform(kmeans.cluster_centers_)
    
    return {
        'labels': labels,
        'centroids': centroids,
        'inertia': kmeans.inertia_,
        'n_clusters': n_clusters
    }


def cluster_routes(routes_data, n_clusters=3):
    """
    Agrupa rutas por similaridad de características.
    
    Args:
        routes_data: Array de características (distancia, demanda, duración)
        n_clusters: Número de clusters
    
    Returns:
        Labels de clusters
    """
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(routes_data)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(data_scaled)
    
    return {
        'labels': labels,
        'centroids': scaler.inverse_transform(kmeans.cluster_centers_)
    }
