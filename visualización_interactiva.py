"""
VISUALIZACIÓN INTERACTIVA CON OPCIONES DE FLUJO DE BUSES
==========================================================

Permite:
1. Elegir diferentes opciones de visualización
2. Ver comportamiento del flujo de buses en tiempo real
3. Animar el movimiento de buses
4. Generar reportes de congestión

Uso: python visualización_interactiva.py
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from bus_system_simple import (
    SistemaTransporte, 
    VisualizadorTransporte, 
    crear_sistema_demo
)


class SimuladorInteractivo:
    """Simulador interactivo con animaciones"""
    
    def __init__(self):
        self.sistema = crear_sistema_demo()
        self.visualizador = VisualizadorTransporte(self.sistema)
        self.paso_actual = 0
        self.max_pasos = 500
    
    def opción_1_visualización_mapas(self):
        """Opción 1: Ver mapas estáticos"""
        print("\n📍 OPCIÓN 1: Visualización de Mapas Estáticos")
        print("-" * 50)
        
        # Mapa base
        self.visualizador.visualizar_mapa_estático()
        plt.suptitle('Red de Transporte - Mapa Base')
        plt.show()
    
    def opción_2_simulación_en_tiempo_real(self):
        """Opción 2: Simular y ver posición de buses"""
        print("\n🚌 OPCIÓN 2: Simulación en Tiempo Real")
        print("-" * 50)
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def actualizar(frame):
            ax.clear()
            
            # Avanzar simulación
            if frame > 0:
                self.sistema.simular_paso(dt=0.1)
            
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
                    estado = 'BAJO'
                elif ocupacion < 80:
                    color = 'yellow'
                    estado = 'MEDIO'
                else:
                    color = 'red'
                    estado = 'ALTO'
                
                ax.scatter(lon, lat, s=200, c=color, marker='^', 
                          edgecolors='black', linewidth=1, zorder=10)
            
            # Información
            stats = self.sistema.estadísticas()
            titulo = f"Simulación en Tiempo Real - Paso {frame}\n" \
                    f"Pasajeros: {stats['total_pasajeros']} | " \
                    f"Ocupación: {stats['ocupacion_promedio']:.1f}% | " \
                    f"Velocidad: {stats['velocidad_promedio_kmh']:.1f} km/h"
            
            ax.set_xlabel('Longitud')
            ax.set_ylabel('Latitud')
            ax.set_title(titulo, fontsize=10)
            ax.grid(True, alpha=0.3)
            
            # Leyenda
            from matplotlib.patches import Patch
            leyenda = [
                Patch(facecolor='green', edgecolor='black', label='Ocupación < 50%'),
                Patch(facecolor='yellow', edgecolor='black', label='Ocupación 50-80%'),
                Patch(facecolor='red', edgecolor='black', label='Ocupación > 80%')
            ]
            ax.legend(handles=leyenda, loc='upper right', fontsize=8)
        
        ani = FuncAnimation(fig, actualizar, frames=100, interval=100, repeat=True)
        plt.tight_layout()
        plt.show()
    
    def opción_3_mapa_de_calor(self):
        """Opción 3: Visualizar congestión"""
        print("\n🔥 OPCIÓN 3: Mapa de Calor de Congestión")
        print("-" * 50)
        
        # Simular 100 pasos primero
        for _ in range(100):
            self.sistema.simular_paso(dt=0.1)
        
        self.visualizador.visualizar_mapa_de_calor()
        plt.show()
    
    def opción_4_estadísticas(self):
        """Opción 4: Ver estadísticas"""
        print("\n📊 OPCIÓN 4: Estadísticas del Sistema")
        print("-" * 50)
        
        # Simular 100 pasos
        for _ in range(100):
            self.sistema.simular_paso(dt=0.1)
        
        stats = self.sistema.estadísticas()
        
        # Mostrar en consola
        print(f"\n✓ Buses en servicio:        {stats['total_buses']}")
        print(f"✓ Pasajeros totales:        {stats['total_pasajeros']}")
        print(f"✓ Ocupación promedio:       {stats['ocupacion_promedio']:.1f}%")
        print(f"✓ Velocidad promedio:       {stats['velocidad_promedio_kmh']:.1f} km/h")
        print(f"✓ Tiempo de simulación:     {stats['tiempo_simulacion_horas']:.2f} horas")
        
        # Mostrar gráficamente
        self.visualizador.visualizar_estadísticas()
        plt.show()
    
    def opción_5_análisis_por_ruta(self):
        """Opción 5: Análisis detallado por ruta"""
        print("\n🛣️  OPCIÓN 5: Análisis por Ruta")
        print("-" * 50)
        
        # Simular
        for _ in range(50):
            self.sistema.simular_paso(dt=0.1)
        
        fig, axes = plt.subplots(1, len(self.sistema.rutas), figsize=(14, 5))
        
        if len(self.sistema.rutas) == 1:
            axes = [axes]
        
        for idx, ruta in enumerate(self.sistema.rutas.values()):
            buses_en_ruta = [b for b in self.sistema.buses.values() if b.ruta.id == ruta.id]
            
            pasajeros_ruta = sum(b.pasajeros for b in buses_en_ruta)
            capacidad_total = len(buses_en_ruta) * 60
            congestión = (pasajeros_ruta / capacidad_total * 100) if capacidad_total > 0 else 0
            
            # Dibujar ruta
            ax = axes[idx]
            
            # Paradas
            lats = [p.latitud for p in ruta.paradas]
            lons = [p.longitud for p in ruta.paradas]
            ax.plot(lons, lats, 'b-', linewidth=2, alpha=0.5)
            ax.scatter(lons, lats, s=200, c='red', zorder=5)
            
            # Buses
            for bus in buses_en_ruta:
                lat, lon = bus.get_posicion()
                ax.scatter(lon, lat, s=150, c='green', marker='^', edgecolors='black')
            
            ax.set_title(f"{ruta.nombre}\nCongestión: {congestión:.1f}%")
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def opción_6_velocidad_vs_ocupación(self):
        """Opción 6: Análisis de velocidad vs ocupación"""
        print("\n⚡ OPCIÓN 6: Velocidad vs Ocupación")
        print("-" * 50)
        
        # Recolectar datos
        velocidades = []
        ocupaciones = []
        
        for _ in range(200):
            self.sistema.simular_paso(dt=0.1)
            
            for bus in self.sistema.buses.values():
                velocidades.append(bus.velocidad_kmh)
                ocupaciones.append(bus.get_ocupacion_porcentaje())
        
        # Gráfico
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Dispersión
        ax1 = axes[0]
        ax1.scatter(ocupaciones, velocidades, alpha=0.5, s=30)
        ax1.set_xlabel('Ocupación (%)')
        ax1.set_ylabel('Velocidad (km/h)')
        ax1.set_title('Relación: Ocupación vs Velocidad')
        ax1.grid(True, alpha=0.3)
        
        # Histogramas
        ax2 = axes[1]
        ax2.hist([o for o in ocupaciones], bins=20, alpha=0.5, label='Ocupación (%)', color='blue')
        ax2_twin = ax2.twinx()
        ax2_twin.hist([v for v in velocidades], bins=20, alpha=0.5, label='Velocidad (km/h)', color='red')
        ax2.set_xlabel('Valor')
        ax2.set_ylabel('Frecuencia - Ocupación', color='blue')
        ax2_twin.set_ylabel('Frecuencia - Velocidad', color='red')
        ax2.set_title('Distribuciones')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def mostrar_menú(self):
        """Muestra menú interactivo"""
        while True:
            print("\n" + "="*50)
            print("VISUALIZACIÓN INTERACTIVA DE FLUJO DE BUSES")
            print("="*50)
            print("\nOpciones disponibles:")
            print("  1. Visualizar mapas estáticos")
            print("  2. Simulación en tiempo real (animación)")
            print("  3. Mapa de calor de congestión")
            print("  4. Estadísticas del sistema")
            print("  5. Análisis detallado por ruta")
            print("  6. Velocidad vs Ocupación")
            print("  0. Salir")
            print("\n" + "-"*50)
            
            try:
                opción = input("Selecciona una opción (0-6): ").strip()
                
                if opción == '1':
                    self.opción_1_visualización_mapas()
                elif opción == '2':
                    self.opción_2_simulación_en_tiempo_real()
                elif opción == '3':
                    self.opción_3_mapa_de_calor()
                elif opción == '4':
                    self.opción_4_estadísticas()
                elif opción == '5':
                    self.opción_5_análisis_por_ruta()
                elif opción == '6':
                    self.opción_6_velocidad_vs_ocupación()
                elif opción == '0':
                    print("\n👋 ¡Hasta luego!\n")
                    break
                else:
                    print("❌ Opción no válida. Intenta de nuevo.")
            
            except KeyboardInterrupt:
                print("\n\n👋 Programa interrumpido. ¡Hasta luego!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    simulador = SimuladorInteractivo()
    simulador.mostrar_menú()
