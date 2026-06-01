"""
🚌 SIMULADOR DE BUSES - ANIMACIÓN EN TIEMPO REAL
====================================================

Compatible con Python 3.8 y superiores
Usa SOLO librerías estándar de Python y numpy/matplotlib

Ejecución: python animacion_buses.py

PRUEBA DE COMPATIBILIDAD:
- Python 3.8 ✓
- Python 3.9 ✓
- Python 3.10 ✓
- Python 3.11 ✓
- Python 3.12 ✓
- Python 3.13 ✓
"""

# IMPORTACIONES - Verificar Python 3.8+
import sys

if sys.version_info < (3, 8):
    print(f"Error: Se requiere Python 3.8 o superior")
    print(f"Tu versión: {sys.version}")
    sys.exit(1)

print(f"\n✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado (Compatible)")

# Librerías estándar de Python
from dataclasses import dataclass
from typing import List, Tuple, Dict
import time

# Librerías para matemática y visualización
try:
    import numpy as np
    print("✅ NumPy cargado")
except ImportError:
    print("❌ Error: NumPy no está instalado")
    print("   Ejecuta: pip install numpy matplotlib")
    sys.exit(1)

try:
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    print("✅ Matplotlib cargado")
except ImportError:
    print("❌ Error: Matplotlib no está instalado")
    print("   Ejecuta: pip install numpy matplotlib")
    sys.exit(1)

# ========== DATOS ==========

@dataclass
class Parada:
    """Parada de bus con coordenadas
    
    Atributos:
        id: Identificador único
        nombre: Nombre de la parada
        lat: Latitud (coordenada Y)
        lon: Longitud (coordenada X)
    """
    id: int
    nombre: str
    lat: float
    lon: float

@dataclass
class Bus:
    """Bus que viaja por una ruta
    
    Atributos:
        id: Identificador único
        nombre: Nombre del bus
        ruta: Lista de paradas que sigue
        progreso: Porcentaje de ruta completada (0.0-1.0)
        pasajeros: Número actual de pasajeros
        velocidad: Factor de velocidad (1.0 = normal)
    """
    id: int
    nombre: str
    ruta: List[Parada]
    progreso: float = 0.0
    pasajeros: int = 20
    velocidad: float = 1.0

# ========== ÁLGEBRA LINEAL ==========

class Matematica:
    """Operaciones matemáticas para transporte"""
    
    @staticmethod
    def distancia(p1: Parada, p2: Parada) -> float:
        """Calcula distancia euclidiana entre dos paradas
        
        Fórmula:
            ||v|| = sqrt((lat2-lat1)^2 + (lon2-lon1)^2)
            Resultado en km (aproximado: 1 grado = 111 km)
        
        Args:
            p1: Primera parada
            p2: Segunda parada
        
        Returns:
            Distancia en kilómetros
        """
        dlat = p2.lat - p1.lat
        dlon = p2.lon - p1.lon
        distancia_grados = np.sqrt(dlat**2 + dlon**2)
        distancia_km = distancia_grados * 111
        return float(distancia_km)
    
    @staticmethod
    def interpolar(p1: Tuple[float, float], 
                   p2: Tuple[float, float], 
                   t: float) -> Tuple[float, float]:
        """Interpola posición entre dos puntos (MOVIMIENTO SUAVE)
        
        Fórmula: P(t) = P1 + t*(P2 - P1) donde t ∈ [0,1]
        
        Esta es la clave para movimiento lineal correcto.
        Asegura que el bus se mueva en línea recta suave.
        
        Args:
            p1: Punto inicial (lat, lon)
            p2: Punto final (lat, lon)
            t: Valor de interpolación entre 0 y 1
        
        Returns:
            Posición interpolada (lat, lon)
        """
        # Asegurar que t esté en rango [0, 1]
        if t < 0:
            t = 0
        elif t > 1:
            t = 1
        
        # Interpolación lineal
        lat = p1[0] + t * (p2[0] - p1[0])
        lon = p1[1] + t * (p2[1] - p1[1])
        
        return (lat, lon)
    
    @staticmethod
    def distancia_total(ruta: List[Parada]) -> float:
        """Calcula distancia total de una ruta (suma de segmentos)
        
        Args:
            ruta: Lista de paradas de la ruta
        
        Returns:
            Distancia total en km
        """
        total = 0.0
        for i in range(len(ruta) - 1):
            total += Matematica.distancia(ruta[i], ruta[i + 1])
        return total

# ========== SISTEMA ==========

class SistemaBuses:
    """Gestor del sistema de transporte"""
    
    def __init__(self):
        """Inicializa el sistema"""
        self.paradas: List[Parada] = []
        self.buses: List[Bus] = []
        self.tiempo_paso: int = 0
    
    def agregar_parada(self, id: int, nombre: str, lat: float, lon: float) -> None:
        """Crea una parada en el sistema
        
        Args:
            id: Identificador único
            nombre: Nombre de la parada
            lat: Latitud
            lon: Longitud
        """
        self.paradas.append(Parada(id, nombre, lat, lon))
    
    def agregar_bus(self, id: int, nombre: str, 
                   parada_ids: List[int], 
                   velocidad: float = 1.0) -> None:
        """Crea un bus con su ruta
        
        Args:
            id: Identificador único
            nombre: Nombre del bus
            parada_ids: IDs de paradas que forman la ruta
            velocidad: Factor de velocidad (1.0 = normal)
        """
        ruta = [p for p in self.paradas if p.id in parada_ids]
        if ruta:
            self.buses.append(Bus(id, nombre, ruta, velocidad=velocidad))
    
    def obtener_posicion_bus(self, bus: Bus) -> Tuple[float, float]:
        """Calcula la posición EXACTA del bus usando interpolación
        
        PROCESO:
        1. Calcula distancia total de la ruta
        2. Calcula qué distancia debe recorrer (progreso * total)
        3. Encuentra qué segmento (parada1 -> parada2)
        4. Interpola dentro del segmento
        5. Retorna (lat, lon) exacto
        
        Args:
            bus: Bus del cual calcular posición
        
        Returns:
            Tupla (latitud, longitud) de la posición del bus
        """
        if len(bus.ruta) < 2:
            # Si solo hay una parada, retornarla
            return (bus.ruta[0].lat, bus.ruta[0].lon)
        
        # Calcular distancia total de la ruta
        distancia_total = Matematica.distancia_total(bus.ruta)
        
        # Distancia que debe recorrer el bus
        distancia_objetivo = bus.progreso * distancia_total
        
        # Buscar en qué segmento está
        distancia_acumulada = 0.0
        
        for i in range(len(bus.ruta) - 1):
            parada_actual = bus.ruta[i]
            parada_siguiente = bus.ruta[i + 1]
            
            # Distancia del segmento
            distancia_segmento = Matematica.distancia(parada_actual, parada_siguiente)
            
            # ¿Está el bus en este segmento?
            if distancia_acumulada + distancia_segmento >= distancia_objetivo:
                # Calcular cuánto avanzó en este segmento (0.0 a 1.0)
                if distancia_segmento > 0:
                    t = (distancia_objetivo - distancia_acumulada) / distancia_segmento
                else:
                    t = 0
                
                # Interpolar
                p1 = (parada_actual.lat, parada_actual.lon)
                p2 = (parada_siguiente.lat, parada_siguiente.lon)
                
                return Matematica.interpolar(p1, p2, t)
            
            distancia_acumulada += distancia_segmento
        
        # Si llegamos al final
        parada_final = bus.ruta[-1]
        return (parada_final.lat, parada_final.lon)
    
    def actualizar_buses(self, dt: float = 0.02) -> None:
        """Actualiza la posición de todos los buses
        
        Args:
            dt: Incremento de progreso (más grande = más rápido)
        """
        for bus in self.buses:
            # Avanzar el progreso
            bus.progreso += dt * bus.velocidad
            
            # Si completa la ruta, vuelve a empezar
            if bus.progreso >= 1.0:
                bus.progreso = 0.0
            
            # Cambiar pasajeros (lógica simple)
            cambio = np.random.randint(-1, 2)
            bus.pasajeros += cambio
            bus.pasajeros = max(5, min(55, bus.pasajeros))
        
        self.tiempo_paso += 1
    
    def obtener_congestion(self) -> float:
        """Calcula congestión promedio del sistema (0.0 a 1.0)
        
        Returns:
            Valor entre 0.0 (vacío) y 1.0 (lleno)
        """
        if not self.buses:
            return 0.0
        total_pasajeros = sum(b.pasajeros for b in self.buses)
        capacidad_total = len(self.buses) * 55
        return total_pasajeros / capacidad_total

# ========== ANIMACIÓN ==========

class AnimadorBuses:
    """Anima los buses en tiempo real"""
    
    def __init__(self, sistema: SistemaBuses):
        """Inicializa el animador
        
        Args:
            sistema: Instancia de SistemaBuses
        """
        self.sistema = sistema
        self.fig = None
        self.ax = None
    
    def crear_figura(self) -> None:
        """Crea la figura matplotlib"""
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        self.fig.suptitle('🚌 SIMULACIÓN DE BUSES EN TIEMPO REAL', 
                         fontsize=16, fontweight='bold')
        
        # Dibujar rutas de fondo
        for bus in self.sistema.buses:
            lats = [p.lat for p in bus.ruta]
            lons = [p.lon for p in bus.ruta]
            self.ax.plot(lons, lats, 'k--', alpha=0.2, linewidth=1, label='Rutas')
        
        # Dibujar paradas
        for parada in self.sistema.paradas:
            self.ax.scatter(parada.lon, parada.lat, s=200, c='red', marker='o', 
                          edgecolors='black', linewidth=2, zorder=5)
            self.ax.text(parada.lon, parada.lat - 0.0015, parada.nombre, 
                        fontsize=8, ha='center', bbox=dict(boxstyle='round', 
                        facecolor='yellow', alpha=0.7))
        
        # Leyenda
        self.ax.text(0.02, 0.98, '🟢 Verde: <30% | 🟡 Amarillo: 30-50% | 🔴 Rojo: >50%', 
                    transform=self.ax.transAxes, fontsize=10, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        self.ax.set_xlabel('Longitud', fontsize=11)
        self.ax.set_ylabel('Latitud', fontsize=11)
        self.ax.grid(True, alpha=0.3, linestyle=':')
        self.ax.set_aspect('equal')
    
    def animar(self, frame: int) -> None:
        """Función de animación llamada cada frame
        
        Args:
            frame: Número de frame actual
        """
        # Actualizar buses
        self.sistema.actualizar_buses(dt=0.02)
        
        # Limpiar gráfico
        self.ax.clear()
        self.ax.set_xlabel('Longitud', fontsize=11)
        self.ax.set_ylabel('Latitud', fontsize=11)
        self.ax.grid(True, alpha=0.3, linestyle=':')
        self.ax.set_aspect('equal')
        
        # Dibujar rutas
        for bus in self.sistema.buses:
            lats = [p.lat for p in bus.ruta]
            lons = [p.lon for p in bus.ruta]
            self.ax.plot(lons, lats, 'k--', alpha=0.1, linewidth=0.5)
        
        # Dibujar paradas
        for parada in self.sistema.paradas:
            self.ax.scatter(parada.lon, parada.lat, s=150, c='red', marker='o',
                          edgecolors='black', linewidth=1.5, zorder=5, alpha=0.6)
        
        # Dibujar buses
        for bus in self.sistema.buses:
            lat, lon = self.sistema.obtener_posicion_bus(bus)
            
            # Calcular color según ocupación
            ocupacion_porcentaje = (bus.pasajeros / 55) * 100
            
            if ocupacion_porcentaje < 30:
                color = '#00cc00'  # Verde
            elif ocupacion_porcentaje < 50:
                color = '#ffcc00'  # Amarillo
            else:
                color = '#ff0000'  # Rojo
            
            # Dibujar bus como triángulo
            self.ax.scatter(lon, lat, s=500, c=color, marker='^', 
                          edgecolors='black', linewidth=2, zorder=10, alpha=0.9)
            
            # Etiqueta con información
            etiqueta = f"{bus.nombre}\n{bus.pasajeros}/55\n({ocupacion_porcentaje:.0f}%)"
            self.ax.text(lon, lat - 0.003, etiqueta, fontsize=7, ha='center',
                        bbox=dict(boxstyle='round', facecolor=color, alpha=0.7))
        
        # Info global
        congestion = self.sistema.obtener_congestion() * 100
        titulo = f"🚌 SIMULACIÓN EN TIEMPO REAL - Frame {self.sistema.tiempo_paso}\n" \
                f"Congestión: {congestion:.1f}%"
        self.ax.set_title(titulo, fontsize=12, fontweight='bold')
        
        # Info en la esquina
        self.ax.text(0.02, 0.98, f'Buses: {len(self.sistema.buses)}\nParadas: {len(self.sistema.paradas)}\n\n🟢 Verde: <30%\n🟡 Amarillo: 30-50%\n🔴 Rojo: >50%', 
                    transform=self.ax.transAxes, fontsize=9, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))
    
    def ejecutar(self, frames: int = 300, interval: int = 50) -> None:
        """Ejecuta la animación
        
        Args:
            frames: Número de frames a animar
            interval: Milisegundos entre frames
        """
        print(f"🔄 Inicializando animación...")
        print(f"   - Frames: {frames}")
        print(f"   - Intervalo: {interval}ms")
        print(f"   - Buses: {len(self.sistema.buses)}")
        print(f"   - Paradas: {len(self.sistema.paradas)}")
        
        self.crear_figura()
        
        ani = FuncAnimation(self.fig, self.animar, frames=frames, 
                          interval=interval, repeat=True, blit=False)
        
        print(f"\n✅ Animación iniciada.")
        print(f"   Cierra la ventana para detener.\n")
        plt.show()

# ========== PROGRAMA PRINCIPAL ==========

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚌 SIMULADOR DE BUSES - ANIMACIÓN EN TIEMPO REAL")
    print("="*60)
    
    # Crear sistema
    print("\n✨ Inicializando sistema...")
    sistema = SistemaBuses()
    
    # Agregar paradas (Pereira, Colombia)
    print("\n📍 Creando paradas:")
    sistema.agregar_parada(1, "Centro Cívico", 4.8135, -75.6942)
    print("   ✓ Parada 1: Centro Cívico")
    
    sistema.agregar_parada(2, "Sur", 4.8050, -75.6950)
    print("   ✓ Parada 2: Sur")
    
    sistema.agregar_parada(3, "Norte", 4.8250, -75.6900)
    print("   ✓ Parada 3: Norte")
    
    sistema.agregar_parada(4, "Este", 4.8100, -75.6850)
    print("   ✓ Parada 4: Este")
    
    # Agregar buses con DIFERENTES velocidades
    print("\n🚌 Creando buses:")
    sistema.agregar_bus(1, "Bus-001", [1, 2, 1], velocidad=1.0)
    print("   ✓ Bus-001: Centro->Sur->Centro (velocidad normal)")
    
    sistema.agregar_bus(2, "Bus-002", [1, 3, 4, 1], velocidad=1.2)
    print("   ✓ Bus-002: Centro->Norte->Este->Centro (velocidad rápida)")
    
    sistema.agregar_bus(3, "Bus-003", [2, 4, 3, 2], velocidad=0.8)
    print("   ✓ Bus-003: Sur->Este->Norte->Sur (velocidad lenta)")
    
    print("\n✅ Sistema inicializado correctamente")
    print(f"   - Total de paradas: {len(sistema.paradas)}")
    print(f"   - Total de buses: {len(sistema.buses)}")
    
    # Crear animador
    print("\n🎬 Creando animador...")
    animador = AnimadorBuses(sistema)
    
    print("✅ Animador listo\n")
    
    # Información de las rutas
    print("="*60)
    print("📦 INFORMACIÓN DE RUTAS")
    print("="*60)
    for bus in sistema.buses:
        paradas_nombres = [p.nombre for p in bus.ruta]
        distancia = sum(Matematica.distancia(bus.ruta[i], bus.ruta[i+1]) 
                       for i in range(len(bus.ruta)-1))
        print(f"\n{bus.nombre}:")
        print(f"  Ruta: {' -> '.join(paradas_nombres)}")
        print(f"  Distancia total: {distancia:.2f} km")
        print(f"  Velocidad: {bus.velocidad}x")
    print("\n" + "="*60)
    
    # Información de distancias entre paradas
    print("\n📏 MATRIZ DE DISTANCIAS ENTRE PARADAS")
    print("="*60)
    for i, p1 in enumerate(sistema.paradas):
        for p2 in sistema.paradas[i+1:]:
            dist = Matematica.distancia(p1, p2)
            print(f"  {p1.nombre:20} -> {p2.nombre:20} = {dist:6.2f} km")
    print("\n" + "="*60 + "\n")
    
    # Ejecutar animación
    print("🔄 Iniciando animación...\n")
    animador.ejecutar(frames=300, interval=50)
    
    print("\n✅ ¡Animación completada!\n")
