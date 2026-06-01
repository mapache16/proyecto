"""
SISTEMA SIMPLIFICADO DE VISUALIZACIÓN DE FLUJO DE BUSES
=========================================================

Implementación limpia y modular que:
- Define rutas explícitamente
- Simula movimiento lógico de buses
- Visualiza congestión en mapa de calor
- Usa solo bibliotecas estándar + matplotlib + numpy

Autor: Sistema AMCO Simplificado
Fecha: 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from dataclasses import dataclass
from typing import List, Dict, Tuple
import time

# ============================================
# 1. DEFINICIONES DE DATOS
# ============================================

@dataclass
class Parada:
    """Parada de autobús con ubicación GPS"""
    id: int
    nombre: str
    latitud: float
    longitud: float
    
    def distancia_a(self, otra: 'Parada') -> float:
        """
        Distancia euclidiana entre dos paradas (Haversine simplificado).
        Álgebra Lineal: ||v1 - v2|| = sqrt((lat2-lat1)² + (lon2-lon1)²)
        """
        dlat = otra.latitud - self.latitud
        dlon = otra.longitud - self.longitud
        
        # Convertir a kilómetros (1 grado ≈ 111 km)
        dlat_km = dlat * 111
        dlon_km = dlon * 111
        
        # Norma L2: sqrt(x² + y²)
        distancia = np.sqrt(dlat_km**2 + dlon_km**2)
        return distancia


@dataclass
class Ruta:
    """Ruta de autobús con secuencia de paradas"""
    id: int
    nombre: str
    codigo: str
    paradas: List[Parada]
    
    def distancia_total(self) -> float:
        """Suma de distancias entre paradas consecutivas"""
        total = 0.0
        for i in range(len(self.paradas) - 1):
            total += self.paradas[i].distancia_a(self.paradas[i + 1])
        return total
    
    def get_posicion_en_ruta(self, progreso: float) -> Tuple[float, float]:
        """
        Interpola posición del bus en la ruta.
        Álgebra Lineal: P(t) = P1 + t*(P2 - P1) para t ∈ [0,1]
        
        Args:
            progreso: valor entre 0.0 y 1.0 indicando posición en la ruta
        
        Returns:
            (latitud, longitud) interpolada
        """
        # Calcular distancia acumulada
        distancias = [0.0]
        for i in range(len(self.paradas) - 1):
            distancia_seg = self.paradas[i].distancia_a(self.paradas[i + 1])
            distancias.append(distancias[-1] + distancia_seg)
        
        distancia_total = distancias[-1]
        distancia_objetivo = progreso * distancia_total
        
        # Encontrar segmento
        for i in range(len(distancias) - 1):
            if distancias[i] <= distancia_objetivo <= distancias[i + 1]:
                # Interpolar dentro del segmento
                if distancias[i + 1] - distancias[i] == 0:
                    t = 0
                else:
                    t = (distancia_objetivo - distancias[i]) / (distancias[i + 1] - distancias[i])
                
                p1 = self.paradas[i]
                p2 = self.paradas[i + 1]
                
                lat = p1.latitud + t * (p2.latitud - p1.latitud)
                lon = p1.longitud + t * (p2.longitud - p1.longitud)
                
                return (lat, lon)
        
        # Si está al final
        p_final = self.paradas[-1]
        return (p_final.latitud, p_final.longitud)


@dataclass
class Bus:
    """Bus en la flota"""
    id: int
    placa: str
    ruta: Ruta
    progreso: float = 0.0  # 0.0 a 1.0
    pasajeros: int = 0
    capacidad: int = 60
    velocidad_kmh: float = 0.0
    estado: str = "EN_SERVICIO"  # EN_SERVICIO, PARADO, MANTENIMIENTO
    
    def avanzar(self, dt: float = 0.1):
        """
        Avanza el bus en su ruta.
        
        Args:
            dt: intervalo de tiempo en horas
        """
        if self.estado != "EN_SERVICIO":
            return
        
        # Distancia en km = velocidad * tiempo
        distancia_km = self.velocidad_kmh * dt
        
        # Fracción de distancia en la ruta total
        ruta_total = self.ruta.distancia_total()
        if ruta_total > 0:
            delta_progreso = distancia_km / ruta_total
            self.progreso += delta_progreso
            
            # Reiniciar si completa la ruta
            if self.progreso >= 1.0:
                self.progreso = 0.0
    
    def get_posicion(self) -> Tuple[float, float]:
        """Retorna posición actual (lat, lon)"""
        return self.ruta.get_posicion_en_ruta(self.progreso)
    
    def get_ocupacion_porcentaje(self) -> float:
        """Retorna porcentaje de ocupación"""
        return (self.pasajeros / self.capacidad) * 100


# ============================================
# 2. SISTEMA DE RUTAS Y BUSES
# ============================================

class SistemaTransporte:
    """Gestor central del sistema de transporte"""
    
    def __init__(self):
        self.paradas: Dict[int, Parada] = {}
        self.rutas: Dict[int, Ruta] = {}
        self.buses: Dict[int, Bus] = {}
        self.historial_congestión: List[Dict] = []
        self.tiempo_simulación = 0.0
    
    def crear_parada(self, id: int, nombre: str, lat: float, lon: float) -> Parada:
        """Crea una parada en el sistema"""
        parada = Parada(id, nombre, lat, lon)
        self.paradas[id] = parada
        return parada
    
    def crear_ruta(self, id: int, nombre: str, codigo: str, parada_ids: List[int]) -> Ruta:
        """Crea una ruta conectando paradas"""
        paradas = [self.paradas[pid] for pid in parada_ids]
        ruta = Ruta(id, nombre, codigo, paradas)
        self.rutas[id] = ruta
        return ruta
    
    def crear_bus(self, id: int, placa: str, ruta_id: int, velocidad: float = 30.0) -> Bus:
        """Crea un bus asignado a una ruta"""
        ruta = self.rutas[ruta_id]
        bus = Bus(id, placa, ruta, velocidad_kmh=velocidad)
        self.buses[id] = bus
        return bus
    
    def simular_paso(self, dt: float = 0.1):
        """Ejecuta un paso de simulación"""
        # Avanzar todos los buses
        for bus in self.buses.values():
            # Variación realista de velocidad
            variación = np.random.normal(1.0, 0.05)  # Media=1, desv=0.05
            velocidad_ajustada = bus.velocidad_kmh * variación
            velocidad_ajustada = max(5, min(60, velocidad_ajustada))  # Rango 5-60 km/h
            
            bus.velocidad_kmh = velocidad_ajustada
            bus.avanzar(dt)
            
            # Actualizar pasajeros (con lógica simple)
            ocupación = bus.get_ocupacion_porcentaje()
            if ocupación < 50:
                # Más gente sube
                bus.pasajeros += np.random.randint(0, 3)
            elif ocupación > 80:
                # Más gente baja
                bus.pasajeros -= np.random.randint(0, 3)
            
            bus.pasajeros = max(0, min(bus.capacidad, bus.pasajeros))
        
        # Registrar congestión
        self._actualizar_congestión()
        self.tiempo_simulación += dt
    
    def _actualizar_congestión(self):
        """Calcula y registra métrica de congestión"""
        por_ruta = {}
        
        for bus in self.buses.values():
            ruta_id = bus.ruta.id
            if ruta_id not in por_ruta:
                por_ruta[ruta_id] = {'buses': 0, 'pasajeros': 0}
            
            por_ruta[ruta_id]['buses'] += 1
            por_ruta[ruta_id]['pasajeros'] += bus.pasajeros
        
        self.historial_congestión.append({
            'tiempo': self.tiempo_simulación,
            'por_ruta': por_ruta
        })
    
    def obtener_congestión_ruta(self, ruta_id: int) -> float:
        """Retorna congestión de una ruta (0.0 a 1.0)"""
        if not self.historial_congestión:
            return 0.0
        
        último = self.historial_congestión[-1]
        if ruta_id not in último['por_ruta']:
            return 0.0
        
        datos = último['por_ruta'][ruta_id]
        # Congestión = (pasajeros totales) / (capacidad total)
        capacidad_total = datos['buses'] * 60
        congestión = datos['pasajeros'] / capacidad_total if capacidad_total > 0 else 0
        return min(1.0, congestión)
    
    def estadísticas(self) -> Dict:
        """Retorna estadísticas del sistema"""
        total_buses = len(self.buses)
        total_pasajeros = sum(b.pasajeros for b in self.buses.values())
        ocupación_promedio = (total_pasajeros / (total_buses * 60)) * 100 if total_buses > 0 else 0
        velocidad_promedio = np.mean([b.velocidad_kmh for b in self.buses.values()])
        
        return {
            'total_buses': total_buses,
            'total_pasajeros': total_pasajeros,
            'ocupacion_promedio': round(ocupacion_promedio, 1),
            'velocidad_promedio_kmh': round(velocidad_promedio, 1),
            'tiempo_simulacion_horas': round(self.tiempo_simulación, 2)
        }


# ============================================
# 3. VISUALIZACIÓN
# ============================================

class VisualizadorTransporte:
    """Dibuja el sistema de transporte"""
    
    def __init__(self, sistema: SistemaTransporte):
        self.sistema = sistema
    
    def visualizar_mapa_estático(self):
        """Dibuja mapa estático con rutas y paradas"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Dibujar rutas
        for ruta in self.sistema.rutas.values():
            lats = [p.latitud for p in ruta.paradas]
            lons = [p.longitud for p in ruta.paradas]
            ax.plot(lons, lats, 'b-', alpha=0.5, linewidth=2, label=f"Ruta {ruta.nombre}" if ruta.id == 1 else "")
        
        # Dibujar paradas
        for parada in self.sistema.paradas.values():
            ax.scatter(parada.longitud, parada.latitud, s=100, c='red', zorder=5)
            ax.text(parada.longitud, parada.latitud, parada.nombre, fontsize=8, ha='center')
        
        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
        ax.set_title('Red de Transporte Metropolitano')
        ax.grid(True, alpha=0.3)
        ax.legend()
        plt.tight_layout()
        return fig, ax
    
    def visualizar_buses_en_tiempo_real(self):
        """Dibuja buses en tiempo real"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Dibujar rutas
        for ruta in self.sistema.rutas.values():
            lats = [p.latitud for p in ruta.paradas]
            lons = [p.longitud for p in ruta.paradas]
            ax.plot(lons, lats, 'b--', alpha=0.3, linewidth=1)
        
        # Dibujar buses
        for bus in self.sistema.buses.values():
            lat, lon = bus.get_posicion()
            ocupacion = bus.get_ocupacion_porcentaje()
            
            # Color según ocupación
            if ocupacion < 50:
                color = 'green'
            elif ocupacion < 80:
                color = 'yellow'
            else:
                color = 'red'
            
            ax.scatter(lon, lat, s=200, c=color, marker='^', edgecolors='black', zorder=10)
            ax.text(lon, lat+0.001, f"{bus.placa}\n{int(ocupacion)}%", fontsize=7, ha='center')
        
        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
        ax.set_title(f'Posición de Buses en Tiempo Real (t={self.sistema.tiempo_simulación:.2f}h)')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig, ax
    
    def visualizar_mapa_de_calor(self):
        """Visualiza congestión como mapa de calor"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Panel 1: Mapa base
        ax1 = axes[0]
        for ruta in self.sistema.rutas.values():
            lats = [p.latitud for p in ruta.paradas]
            lons = [p.longitud for p in ruta.paradas]
            ax1.plot(lons, lats, 'k-', alpha=0.3, linewidth=2)
        
        # Panel 2: Congestión por ruta
        ax2 = axes[1]
        rutas_nombres = []
        congestiones = []
        
        for ruta in self.sistema.rutas.values():
            congestión = self.sistema.obtener_congestión_ruta(ruta.id)
            rutas_nombres.append(ruta.nombre)
            congestiones.append(congestión * 100)
        
        colors = ['green' if c < 50 else 'yellow' if c < 80 else 'red' for c in congestiones]
        ax2.bar(range(len(rutas_nombres)), congestiones, color=colors)
        ax2.set_xticks(range(len(rutas_nombres)))
        ax2.set_xticklabels(rutas_nombres, rotation=45)
        ax2.set_ylabel('Congestión (%)')
        ax2.set_title('Nivel de Congestión por Ruta')
        ax2.set_ylim([0, 100])
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    def visualizar_estadísticas(self):
        """Dibuja estadísticas del sistema"""
        stats = self.sistema.estadísticas()
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('Estadísticas del Sistema de Transporte', fontsize=14, fontweight='bold')
        
        # Buses
        ax = axes[0, 0]
        ax.text(0.5, 0.5, f"{stats['total_buses']}", fontsize=40, ha='center', va='center', fontweight='bold')
        ax.text(0.5, 0.1, "Buses en Servicio", fontsize=12, ha='center')
        ax.axis('off')
        
        # Pasajeros
        ax = axes[0, 1]
        ax.text(0.5, 0.5, f"{stats['total_pasajeros']}", fontsize=40, ha='center', va='center', fontweight='bold')
        ax.text(0.5, 0.1, "Pasajeros Totales", fontsize=12, ha='center')
        ax.axis('off')
        
        # Ocupación
        ax = axes[1, 0]
        ocupacion = stats['ocupacion_promedio']
        color = 'green' if ocupacion < 50 else 'yellow' if ocupacion < 80 else 'red'
        ax.text(0.5, 0.5, f"{ocupacion:.1f}%", fontsize=40, ha='center', va='center', fontweight='bold', color=color)
        ax.text(0.5, 0.1, "Ocupación Promedio", fontsize=12, ha='center')
        ax.axis('off')
        
        # Velocidad
        ax = axes[1, 1]
        ax.text(0.5, 0.5, f"{stats['velocidad_promedio_kmh']:.1f}", fontsize=40, ha='center', va='center', fontweight='bold')
        ax.text(0.5, 0.1, "Velocidad Promedio (km/h)", fontsize=12, ha='center')
        ax.axis('off')
        
        plt.tight_layout()
        return fig


# ============================================
# 4. EJEMPLO DE USO
# ============================================

def crear_sistema_demo() -> SistemaTransporte:
    """Crea un sistema de demostración"""
    sistema = SistemaTransporte()
    
    # Crear paradas (coordenadas cercanas a Pereira, Colombia)
    p1 = sistema.crear_parada(1, "Centro Cívico", 4.8135, -75.6942)
    p2 = sistema.crear_parada(2, "Estación Sur", 4.8050, -75.6950)
    p3 = sistema.crear_parada(3, "Hospital", 4.8200, -75.6900)
    p4 = sistema.crear_parada(4, "Universidad", 4.8250, -75.7000)
    p5 = sistema.crear_parada(5, "Terminal Norte", 4.8300, -75.6850)
    
    # Crear rutas
    r1 = sistema.crear_ruta(1, "Ruta A - Centro", "A01", [1, 2, 3, 1])
    r2 = sistema.crear_ruta(2, "Ruta B - Periferia", "B01", [1, 4, 5, 1])
    r3 = sistema.crear_ruta(3, "Ruta C - Circular", "C01", [2, 3, 5, 4, 2])
    
    # Crear buses en cada ruta
    for i in range(5):
        sistema.crear_bus(i+1, f"BUS-{i+1:03d}", 1, velocidad=35.0)
    
    for i in range(5, 10):
        sistema.crear_bus(i+1, f"BUS-{i+1:03d}", 2, velocidad=40.0)
    
    for i in range(10, 15):
        sistema.crear_bus(i+1, f"BUS-{i+1:03d}", 3, velocidad=30.0)
    
    return sistema


if __name__ == "__main__":
    print("\n" + "="*60)
    print("SISTEMA SIMPLIFICADO DE VISUALIZACIÓN DE FLUJO DE BUSES")
    print("="*60 + "\n")
    
    # Crear sistema
    sistema = crear_sistema_demo()
    visualizador = VisualizadorTransporte(sistema)
    
    print("✅ Sistema creado con éxito")
    print(f"   - {len(sistema.paradas)} paradas")
    print(f"   - {len(sistema.rutas)} rutas")
    print(f"   - {len(sistema.buses)} buses\n")
    
    # Simular 100 pasos
    print("🔄 Ejecutando simulación...")
    for paso in range(100):
        sistema.simular_paso(dt=0.1)
        if (paso + 1) % 20 == 0:
            stats = sistema.estadísticas()
            print(f"   Paso {paso+1}: Pasajeros={stats['total_pasajeros']}, "
                  f"Ocupación={stats['ocupacion_promedio']:.1f}%, "
                  f"Velocidad={stats['velocidad_promedio_kmh']:.1f} km/h")
    
    print("\n📊 Generando visualizaciones...\n")
    
    # Mostrar visualizaciones
    visualizador.visualizar_mapa_estático()
    print("   ✓ Mapa estático")
    
    visualizador.visualizar_buses_en_tiempo_real()
    print("   ✓ Buses en tiempo real")
    
    visualizador.visualizar_mapa_de_calor()
    print("   ✓ Mapa de calor de congestión")
    
    visualizador.visualizar_estadísticas()
    print("   ✓ Estadísticas del sistema\n")
    
    # Estadísticas finales
    stats_finales = sistema.estadísticas()
    print("="*60)
    print("ESTADÍSTICAS FINALES")
    print("="*60)
    print(f"Total de buses:               {stats_finales['total_buses']}")
    print(f"Pasajeros totales:           {stats_finales['total_pasajeros']}")
    print(f"Ocupación promedio:          {stats_finales['ocupacion_promedio']:.1f}%")
    print(f"Velocidad promedio:          {stats_finales['velocidad_promedio_kmh']:.1f} km/h")
    print(f"Tiempo de simulación:        {stats_finales['tiempo_simulacion_horas']:.2f} horas")
    print("="*60 + "\n")
    
    plt.show()
