"""
🚌 SISTEMA COMPACTO DE TRANSPORTE - 2DO SEMESTRE
=======================================================

Código simple, fácil de entender y ejecutar.
Álgebra Lineal + Visualización en ~300 líneas.

Ejecución: python mini_bus.py
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple

# ========== DATOS ==========

@dataclass
class Parada:
    """Parada de bus con coordenadas"""
    id: int
    nombre: str
    lat: float
    lon: float

@dataclass  
class Bus:
    """Bus que viaja por una ruta"""
    id: int
    nombre: str
    ruta: List[Parada]
    progreso: float = 0.0  # 0.0 a 1.0
    pasajeros: int = 20

# ========== ÁLGEBRA LINEAL ==========

class Matematica:
    """Operaciones de álgebra lineal para transporte"""
    
    @staticmethod
    def distancia(p1: Parada, p2: Parada) -> float:
        """Distancia euclidiana entre dos paradas
        
        Fórmula: ||v|| = sqrt((lat2-lat1)^2 + (lon2-lon1)^2)
        """
        dlat = p2.lat - p1.lat
        dlon = p2.lon - p1.lon
        return np.sqrt(dlat**2 + dlon**2) * 111  # Convertir a km
    
    @staticmethod
    def interpolar(p1: Tuple, p2: Tuple, t: float) -> Tuple:
        """Interpola posición entre dos puntos
        
        Fórmula: P(t) = P1 + t*(P2 - P1) donde t ∈ [0,1]
        """
        lat = p1[0] + t * (p2[0] - p1[0])
        lon = p1[1] + t * (p2[1] - p1[1])
        return (lat, lon)
    
    @staticmethod
    def distancia_total(ruta: List[Parada]) -> float:
        """Distancia total de una ruta (suma de segmentos)"""
        total = 0.0
        for i in range(len(ruta) - 1):
            total += Matematica.distancia(ruta[i], ruta[i + 1])
        return total

# ========== SISTEMA ==========

class SistemaBuses:
    """Gestor del sistema de transporte"""
    
    def __init__(self):
        self.paradas = []
        self.buses = []
        self.historial = []
    
    def agregar_parada(self, id: int, nombre: str, lat: float, lon: float):
        """Crea una parada"""
        self.paradas.append(Parada(id, nombre, lat, lon))
    
    def agregar_bus(self, id: int, nombre: str, parada_ids: List[int]):
        """Crea un bus con su ruta"""
        ruta = [p for p in self.paradas if p.id in parada_ids]
        self.buses.append(Bus(id, nombre, ruta))
    
    def simular(self, pasos: int = 50):
        """Ejecuta simulación"""
        for paso in range(pasos):
            for bus in self.buses:
                # Avanzar bus
                bus.progreso += 0.02
                if bus.progreso >= 1.0:
                    bus.progreso = 0.0
                
                # Cambiar pasajeros
                bus.pasajeros += np.random.randint(-2, 3)
                bus.pasajeros = max(10, min(60, bus.pasajeros))
            
            # Guardar datos
            self.historial.append({
                'paso': paso,
                'buses': [(b.id, b.progreso, b.pasajeros) for b in self.buses]
            })
    
    def posicion_bus(self, bus: Bus) -> Tuple:
        """Calcula posición actual del bus (interpolación)"""
        if len(bus.ruta) < 2:
            return (bus.ruta[0].lat, bus.ruta[0].lon)
        
        # Encontrar segmento
        distancia_total = Matematica.distancia_total(bus.ruta)
        distancia_objetivo = bus.progreso * distancia_total
        
        distancia_acum = 0
        for i in range(len(bus.ruta) - 1):
            seg_dist = Matematica.distancia(bus.ruta[i], bus.ruta[i + 1])
            
            if distancia_acum + seg_dist >= distancia_objetivo:
                # Interpolar en este segmento
                t = (distancia_objetivo - distancia_acum) / seg_dist if seg_dist > 0 else 0
                return Matematica.interpolar(
                    (bus.ruta[i].lat, bus.ruta[i].lon),
                    (bus.ruta[i + 1].lat, bus.ruta[i + 1].lon),
                    t
                )
            
            distancia_acum += seg_dist
        
        # Final
        return (bus.ruta[-1].lat, bus.ruta[-1].lon)
    
    def congestión(self) -> float:
        """Congestión promedio del sistema (0.0 a 1.0)"""
        if not self.buses:
            return 0.0
        ocupación = sum(b.pasajeros for b in self.buses) / (len(self.buses) * 60)
        return min(1.0, ocupación)

# ========== VISUALIZACIÓN ==========

class Visor:
    """Visualiza el sistema"""
    
    def __init__(self, sistema: SistemaBuses):
        self.sistema = sistema
    
    def mostrar_todo(self):
        """Muestra 4 gráficos en uno"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("🚌 SISTEMA DE TRANSPORTE - VISUALIZACIÓN COMPLETA", 
                     fontsize=14, fontweight='bold')
        
        # Gráfico 1: Mapa de rutas
        ax1 = axes[0, 0]
        for bus in self.sistema.buses:
            lats = [p.lat for p in bus.ruta]
            lons = [p.lon for p in bus.ruta]
            ax1.plot(lons, lats, 'o-', label=bus.nombre, linewidth=2, markersize=6)
        ax1.set_xlabel('Longitud')
        ax1.set_ylabel('Latitud')
        ax1.set_title('Red de Rutas')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Gráfico 2: Posición actual de buses
        ax2 = axes[0, 1]
        for bus in self.sistema.buses:
            lats = [p.lat for p in bus.ruta]
            lons = [p.lon for p in bus.ruta]
            ax2.plot(lons, lats, 'k--', alpha=0.3, linewidth=1)
            
            lat, lon = self.sistema.posicion_bus(bus)
            ocupacion = bus.pasajeros / 60
            color = 'green' if ocupacion < 0.5 else 'yellow' if ocupacion < 0.8 else 'red'
            ax2.scatter(lon, lat, s=300, c=color, marker='^', edgecolors='black', linewidth=2)
        
        ax2.set_xlabel('Longitud')
        ax2.set_ylabel('Latitud')
        ax2.set_title('Posición de Buses (colores: verde<50%, amarillo<80%, rojo>80%)')
        ax2.grid(True, alpha=0.3)
        
        # Gráfico 3: Ocupación de buses
        ax3 = axes[1, 0]
        nombres = [b.nombre for b in self.sistema.buses]
        ocupaciones = [b.pasajeros for b in self.sistema.buses]
        colors = ['green' if o < 30 else 'yellow' if o < 48 else 'red' for o in ocupaciones]
        ax3.bar(nombres, ocupaciones, color=colors, edgecolor='black')
        ax3.set_ylabel('Pasajeros')
        ax3.set_title('Ocupación Actual de Buses')
        ax3.set_ylim([0, 70])
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Gráfico 4: Historial de congestión
        ax4 = axes[1, 1]
        if self.sistema.historial:
            pasos = [h['paso'] for h in self.sistema.historial]
            congestiones = []
            for h in self.sistema.historial:
                pasajeros_total = sum(b[2] for b in h['buses'])
                cong = pasajeros_total / (len(self.sistema.buses) * 60)
                congestiones.append(cong * 100)
            
            ax4.plot(pasos, congestiones, 'b-', linewidth=2)
            ax4.fill_between(pasos, congestiones, alpha=0.3)
            ax4.set_xlabel('Paso de Simulación')
            ax4.set_ylabel('Congestión (%)')
            ax4.set_title('Historial de Congestión')
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def estadisticas(self):
        """Imprime estadísticas en consola"""
        print("\n" + "="*50)
        print("ESTADÍSTICAS DEL SISTEMA")
        print("="*50)
        print(f"Total de buses: {len(self.sistema.buses)}")
        print(f"Total de paradas: {len(self.sistema.paradas)}")
        print(f"Pasajeros totales: {sum(b.pasajeros for b in self.sistema.buses)}")
        print(f"Congestión promedio: {self.sistema.congestión()*100:.1f}%")
        print("\nDetalle de buses:")
        for bus in self.sistema.buses:
            print(f"  {bus.nombre}: {bus.pasajeros}/60 pasajeros ({bus.pasajeros/60*100:.0f}%)")
        print("="*50 + "\n")

# ========== EJECUCIÓN PRINCIPAL ==========

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚌 SISTEMA COMPACTO DE TRANSPORTE - 2DO SEMESTRE")
    print("="*50)
    
    # Crear sistema
    print("\n✨ Inicializando sistema...")
    sistema = SistemaBuses()
    
    # Agregar paradas (Pereira)
    sistema.agregar_parada(1, "Centro", 4.8135, -75.6942)
    sistema.agregar_parada(2, "Sur", 4.8050, -75.6950)
    sistema.agregar_parada(3, "Norte", 4.8250, -75.6900)
    sistema.agregar_parada(4, "Este", 4.8100, -75.6850)
    
    # Agregar buses
    sistema.agregar_bus(1, "Bus-001", [1, 2, 1])
    sistema.agregar_bus(2, "Bus-002", [1, 3, 4, 1])
    sistema.agregar_bus(3, "Bus-003", [2, 4, 3, 2])
    
    print("✅ Sistema creado:")
    print(f"   - {len(sistema.paradas)} paradas")
    print(f"   - {len(sistema.buses)} buses")
    
    # Simular
    print("\n🔄 Ejecutando simulación (50 pasos)...")
    sistema.simular(pasos=50)
    print("✅ Simulación completada")
    
    # Mostrar resultados
    visor = Visor(sistema)
    visor.estadisticas()
    
    # Visualizar
    print("\n📊 Generando gráficos...")
    visor.mostrar_todo()
    
    print("\n✅ ¡Listo!\n")
