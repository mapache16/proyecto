"""
🚌 OPTIMIZADOR DE RUTAS - PEREIRA Y DOSQUEBRADAS
========================================================

Demostrador de optimización de rutas usando Álgebra Lineal
con eventos del mundo real (accidentes, lluvia, bloqueos).

Características:
- Interfaz interactiva con botones para eventos
- Cálculo de ruta óptima usando Dijkstra
- Matriz de pesos dinámicos según eventos
- Demostración de álgebra lineal aplicada

Ejecución: python optimizador_rutas.py
"""

import sys
if sys.version_info < (3, 8):
    print(f"Error: Se requiere Python 3.8 o superior")
    sys.exit(1)

from dataclasses import dataclass
from typing import List, Tuple, Dict, Set
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import heapq

# ========== DATOS ==========

@dataclass
class Parada:
    """Parada de transporte"""
    id: int
    nombre: str
    lat: float
    lon: float
    ciudad: str

@dataclass
class Autobus:
    """Autobús con posición y estado"""
    id: int
    nombre: str
    ruta_actual: List[int]  # IDs de paradas
    posicion_actual: int  # Índice en la ruta
    pasajeros: int = 20
    estado: str = "NORMAL"  # NORMAL, LENTO, ATRAPADO, DESVIADO

# ========== EVENTOS ==========

class EventoTransporte:
    """Evento que afecta el transporte"""
    
    def __init__(self, tipo: str, parada_id: int, severidad: float = 0.5):
        self.tipo = tipo  # ACCIDENTE, LLUVIA, PROTESTA, CONSTRUCCION
        self.parada_id = parada_id
        self.severidad = severidad  # 0.0 a 1.0
        self.activo = True
    
    def __repr__(self):
        emojis = {
            'ACCIDENTE': '🚗💥',
            'LLUVIA': '🌧️',
            'PROTESTA': '🚧',
            'CONSTRUCCION': '🏗️'
        }
        return f"{emojis.get(self.tipo, '⚠️')} {self.tipo} (Severidad: {self.severidad*100:.0f}%)"

# ========== ÁLGEBRA LINEAL ==========

class MatematicasTransporte:
    """Operaciones de álgebra lineal para transporte"""
    
    @staticmethod
    def distancia_euclidiana(p1: Parada, p2: Parada) -> float:
        """Norma L2: ||v|| = sqrt((lat2-lat1)^2 + (lon2-lon1)^2)"""
        dlat = p2.lat - p1.lat
        dlon = p2.lon - p1.lon
        return np.sqrt(dlat**2 + dlon**2) * 111  # km
    
    @staticmethod
    def construir_matriz_distancias(paradas: List[Parada]) -> np.ndarray:
        """Construye matriz de distancias (n×n)
        
        Esta es la BASE para Dijkstra.
        Cada elemento M[i,j] = distancia de parada i a j
        """
        n = len(paradas)
        matriz = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    matriz[i][j] = MatematicasTransporte.distancia_euclidiana(paradas[i], paradas[j])
        
        return matriz
    
    @staticmethod
    def aplicar_eventos_a_matriz(matriz: np.ndarray, 
                                  paradas: List[Parada],
                                  eventos: List[EventoTransporte]) -> np.ndarray:
        """Modifica matriz según eventos activos
        
        La severidad del evento aumenta el peso (tiempo) de la ruta.
        Esto demuestra cómo el álgebra lineal se adapta a cambios.
        """
        matriz_modificada = matriz.copy()
        
        # Agrupar eventos por parada
        eventos_por_parada = {}
        for evento in eventos:
            if evento.activo:
                if evento.parada_id not in eventos_por_parada:
                    eventos_por_parada[evento.parada_id] = []
                eventos_por_parada[evento.parada_id].append(evento)
        
        # Aplicar multiplicador a las distancias
        for parada_id, evento_lista in eventos_por_parada.items():
            idx = parada_id - 1
            severidad_max = max(e.severidad for e in evento_lista)
            
            # Aumentar todas las distancias hacia y desde esta parada
            multiplicador = 1 + severidad_max * 3  # Hasta 4x más lento
            matriz_modificada[idx, :] *= multiplicador
            matriz_modificada[:, idx] *= multiplicador
        
        return matriz_modificada
    
    @staticmethod
    def dijkstra(matriz: np.ndarray, inicio: int, fin: int) -> Tuple[float, List[int]]:
        """Algoritmo de Dijkstra para encontrar ruta óptima
        
        DEMOSTRACIÓN DE ÁLGEBRA LINEAL:
        - Usa matriz de pesos (distancias modificadas)
        - Encuentra camino mínimo
        - Demuestra optimización matemática
        
        Complejidad: O(n^2)
        """
        n = len(matriz)
        distancias = [float('inf')] * n
        distancias[inicio] = 0
        padres = [-1] * n
        visitados = set()
        
        # Cola de prioridad: (distancia, nodo)
        cola = [(0, inicio)]
        
        while cola:
            dist_actual, nodo = heapq.heappop(cola)
            
            if nodo in visitados:
                continue
            
            visitados.add(nodo)
            
            # Si llegamos al destino
            if nodo == fin:
                break
            
            # Explorar vecinos
            for vecino in range(n):
                if vecino not in visitados and matriz[nodo][vecino] > 0:
                    nueva_dist = dist_actual + matriz[nodo][vecino]
                    
                    if nueva_dist < distancias[vecino]:
                        distancias[vecino] = nueva_dist
                        padres[vecino] = nodo
                        heapq.heappush(cola, (nueva_dist, vecino))
        
        # Reconstruir camino
        camino = []
        actual = fin
        while actual != -1:
            camino.append(actual)
            actual = padres[actual]
        camino.reverse()
        
        return distancias[fin], camino

# ========== SISTEMA ==========

class SistemaOptimizacion:
    """Sistema de optimización de rutas"""
    
    def __init__(self):
        self.paradas: List[Parada] = []
        self.autobuses: List[Autobus] = []
        self.eventos: List[EventoTransporte] = []
        self.matriz_distancias: np.ndarray = None
        self.ruta_recomendada: Dict = {'distancia': 0, 'camino': [], 'paradas': []}
    
    def agregar_parada(self, id: int, nombre: str, lat: float, lon: float, ciudad: str):
        self.paradas.append(Parada(id, nombre, lat, lon, ciudad))
    
    def agregar_autobus(self, id: int, nombre: str, ruta: List[int]):
        self.autobuses.append(Autobus(id, nombre, ruta, 0))
    
    def crear_evento(self, tipo: str, parada_id: int, severidad: float = 0.5):
        """Crea un evento que afecta la ruta"""
        # Verificar si ya existe evento en esta parada
        for evento in self.eventos:
            if evento.parada_id == parada_id and evento.tipo == tipo:
                evento.activo = True
                evento.severidad = severidad
                return
        
        self.eventos.append(EventoTransporte(tipo, parada_id, severidad))
    
    def eliminar_evento(self, parada_id: int):
        """Elimina todos los eventos de una parada"""
        for evento in self.eventos:
            if evento.parada_id == parada_id:
                evento.activo = False
    
    def construir_matrices(self):
        """Construye la matriz base de distancias"""
        self.matriz_distancias = MatematicasTransporte.construir_matriz_distancias(self.paradas)
    
    def obtener_ruta_optima(self, inicio_id: int, fin_id: int) -> Dict:
        """Calcula ruta óptima usando Dijkstra con eventos"""
        # Aplicar eventos a la matriz
        matriz_modificada = MatematicasTransporte.aplicar_eventos_a_matriz(
            self.matriz_distancias, self.paradas, self.eventos
        )
        
        inicio_idx = inicio_id - 1
        fin_idx = fin_id - 1
        
        distancia, camino = MatematicasTransporte.dijkstra(matriz_modificada, inicio_idx, fin_idx)
        
        # Convertir a IDs y nombres
        paradas_camino = [self.paradas[idx] for idx in camino]
        
        return {
            'distancia': distancia,
            'camino': camino,
            'paradas': paradas_camino,
            'tiempo_estimado': distancia / 40  # 40 km/h promedio
        }

# ========== VISUALIZACIÓN CON BOTONES ==========

class VisualizadorInteractivo:
    """Visualizador con botones para eventos"""
    
    def __init__(self, sistema: SistemaOptimizacion):
        self.sistema = sistema
        self.fig = None
        self.ax = None
        self.botones = {}
        self.evento_seleccionado = None
        self.parada_seleccionada = None
    
    def crear_interfaz(self):
        """Crea la interfaz con botones"""
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.suptitle(
            '🚌 OPTIMIZADOR DE RUTAS - PEREIRA Y DOSQUEBRADAS\n'
            '📊 Demostra: Álgebra Lineal + Optimización con Dijkstra',
            fontsize=16, fontweight='bold', color='#003d99'
        )
        
        # Mapa principal
        self.ax = self.fig.add_subplot(121)
        self.dibujar_mapa()
        
        # Panel de control
        ax_control = self.fig.add_subplot(122)
        ax_control.axis('off')
        
        # Instrucciones
        instrucciones = (
            '📌 INSTRUCCIONES:\n'
            '1. Haz click en una parada del mapa\n'
            '2. Selecciona un evento\n'
            '3. Observa cómo cambia la ruta óptima\n\n'
            '🎯 EVENTOS DISPONIBLES:\n'
        )
        ax_control.text(0.05, 0.95, instrucciones, transform=ax_control.transAxes,
                       fontsize=10, verticalalignment='top', fontfamily='monospace',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Botones de eventos
        eventos_config = [
            ('🚗💥 Accidente', 'ACCIDENTE', 0.70),
            ('🌧️ Lluvia Fuerte', 'LLUVIA', 0.60),
            ('🚧 Protesta', 'PROTESTA', 0.75),
            ('🏗️ Construcción', 'CONSTRUCCION', 0.80),
            ('✅ Limpiar Todo', 'LIMPIAR', 1.0)
        ]
        
        y_pos = 0.60
        for label, evento_tipo, _ in eventos_config:
            ax_boton = self.fig.add_axes([0.55, y_pos, 0.35, 0.05])
            boton = Button(ax_boton, label, color='#ffeb3b', hovercolor='#fdd835')
            boton.on_clicked(lambda event, t=evento_tipo: self.manejar_evento(event, t))
            self.botones[evento_tipo] = boton
            y_pos -= 0.08
        
        # Información de ruta
        self.ax_info = self.fig.add_axes([0.55, 0.02, 0.40, 0.18])
        self.ax_info.axis('off')
        
        # Interactividad con el mapa
        self.fig.canvas.mpl_connect('button_press_event', self.on_click_mapa)
    
    def dibujar_mapa(self):
        """Dibuja el mapa base"""
        self.ax.clear()
        
        # Dibujar paradas
        colores_paradas = {}
        for parada in self.sistema.paradas:
            # Verificar si tiene eventos
            tiene_evento = any(e.parada_id == parada.id and e.activo for e in self.sistema.eventos)
            color = '#ff5555' if tiene_evento else '#0066cc'
            colores_paradas[parada.id] = color
            
            self.ax.scatter(parada.lon, parada.lat, s=400, c=color, marker='o',
                          edgecolors='black', linewidth=2.5, zorder=5)
            
            # Etiqueta
            self.ax.text(parada.lon + 0.0003, parada.lat + 0.0003, 
                        f"{parada.nombre}", fontsize=8, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.7))
        
        # Dibujar ruta recomendada si existe
        if self.sistema.ruta_recomendada['camino']:
            camino = self.sistema.ruta_recomendada['paradas']
            lons = [p.lon for p in camino]
            lats = [p.lat for p in camino]
            self.ax.plot(lons, lats, 'g-', linewidth=3, alpha=0.6, label='Ruta Óptima')
            self.ax.plot(lons, lats, 'g^', markersize=10, alpha=0.8)
        
        # Eventos activos
        for evento in self.sistema.eventos:
            if evento.activo:
                parada = next(p for p in self.sistema.paradas if p.id == evento.parada_id)
                emojis = {'ACCIDENTE': '🚗💥', 'LLUVIA': '🌧️', 'PROTESTA': '🚧', 'CONSTRUCCION': '🏗️'}
                self.ax.text(parada.lon, parada.lat - 0.0025, emojis.get(evento.tipo, '⚠️'),
                           fontsize=20, ha='center')
        
        self.ax.set_xlabel('Longitud', fontsize=10)
        self.ax.set_ylabel('Latitud', fontsize=10)
        self.ax.set_title('Mapa de Pereira y Dosquebradas', fontsize=12, fontweight='bold')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlim(-75.76, -75.65)
        self.ax.set_ylim(4.78, 4.84)
        self.ax.legend(loc='upper left')
    
    def on_click_mapa(self, event):
        """Maneja clicks en el mapa"""
        if event.inaxes != self.ax:
            return
        
        # Buscar parada más cercana
        min_dist = float('inf')
        parada_cercana = None
        
        for parada in self.sistema.paradas:
            dist = np.sqrt((event.xdata - parada.lon)**2 + (event.ydata - parada.lat)**2)
            if dist < min_dist:
                min_dist = dist
                parada_cercana = parada
        
        if min_dist < 0.002:  # Threshold de proximidad
            self.parada_seleccionada = parada_cercana
            print(f"\n✅ Parada seleccionada: {parada_cercana.nombre} (ID: {parada_cercana.id})")
            print(f"   Ahora selecciona un evento...")
    
    def manejar_evento(self, event, tipo_evento):
        """Maneja selección de eventos"""
        if tipo_evento == 'LIMPIAR':
            print("\n🧹 Limpiando todos los eventos...")
            for evento in self.sistema.eventos:
                evento.activo = False
            self.parada_seleccionada = None
        elif self.parada_seleccionada:
            print(f"\n⚠️ Evento '{tipo_evento}' creado en {self.parada_seleccionada.nombre}")
            self.sistema.crear_evento(tipo_evento, self.parada_seleccionada.id, 0.7)
            
            # Calcular nueva ruta óptima
            ruta = self.sistema.obtener_ruta_optima(1, 6)
            self.sistema.ruta_recomendada = ruta
            
            # Mostrar información
            self.mostrar_info_ruta(ruta)
        else:
            print("\n⚠️ Debes seleccionar una parada primero (haz click en el mapa)")
        
        self.dibujar_mapa()
        self.fig.canvas.draw_idle()
    
    def mostrar_info_ruta(self, ruta):
        """Muestra información de la ruta calculada"""
        self.ax_info.clear()
        self.ax_info.axis('off')
        
        info_texto = (
            f"📊 INFORMACIÓN DE RUTA ÓPTIMA:\n"
            f"════════════════════════════\n"
            f"📏 Distancia: {ruta['distancia']:.2f} km\n"
            f"⏱️ Tiempo Est.: {ruta['tiempo_estimado']:.1f} horas\n\n"
            f"🛣️ CAMINO (Dijkstra):\n"
            f"{' → '.join(p.nombre for p in ruta['paradas'])}\n\n"
            f"✅ Álgebra Lineal Aplicada:\n"
            f"• Matriz de distancias\n"
            f"• Algoritmo de Dijkstra\n"
            f"• Optimización con eventos"
        )
        
        self.ax_info.text(0.05, 0.95, info_texto, transform=self.ax_info.transAxes,
                         fontsize=9, verticalalignment='top', fontfamily='monospace',
                         bbox=dict(boxstyle='round', facecolor='#e8f5e9', alpha=0.9, 
                                 edgecolor='green', linewidth=2))

# ========== PROGRAMA PRINCIPAL ==========

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚌 OPTIMIZADOR DE RUTAS - DEMOSTRA ÁLGEBRA LINEAL")
    print("="*70)
    
    # Crear sistema
    print("\n⚙️ Inicializando sistema...")
    sistema = SistemaOptimizacion()
    
    # Paradas
    print("\n📌 Creando paradas:")
    sistema.agregar_parada(1, "Centro Pereira", 4.8135, -75.6942, "Pereira")
    sistema.agregar_parada(2, "Parque Arvi", 4.8250, -75.7100, "Pereira")
    sistema.agregar_parada(3, "Centro Comercial", 4.8050, -75.6850, "Pereira")
    sistema.agregar_parada(4, "Terminal Autobuses", 4.8100, -75.7000, "Pereira")
    sistema.agregar_parada(5, "Centro Dosquebradas", 4.8000, -75.7200, "Dosquebradas")
    sistema.agregar_parada(6, "Sector Galicia", 4.7900, -75.7150, "Dosquebradas")
    print("   ✓ 6 paradas creadas")
    
    # Autobuses
    print("\n🚌 Creando autobuses:")
    sistema.agregar_autobus(1, "Autobús Ruta A", [1, 4, 3, 1])
    sistema.agregar_autobus(2, "Autobús Ruta B", [1, 5, 6, 1])
    sistema.agregar_autobus(3, "Autobús Ruta C", [2, 1, 4, 2])
    print("   ✓ 3 autobuses creados")
    
    # Construir matrices
    print("\n📊 Construyendo matrices de distancias...")
    sistema.construir_matrices()
    print("   ✓ Matriz base construida")
    
    # Calcular ruta inicial
    print("\n🎯 Calculando ruta óptima inicial (sin eventos)...")
    ruta_inicial = sistema.obtener_ruta_optima(1, 6)
    sistema.ruta_recomendada = ruta_inicial
    
    print(f"   📏 Distancia: {ruta_inicial['distancia']:.2f} km")
    print(f"   ⏱️ Tiempo: {ruta_inicial['tiempo_estimado']:.1f} horas")
    print(f"   🛣️ Camino: {' → '.join(p.nombre for p in ruta_inicial['paradas'])}")
    
    # Mostrar interfaz
    print("\n" + "="*70)
    print("🎮 INTERFAZ INTERACTIVA - CÓMO USAR:")
    print("="*70)
    print("""
1. HAZE CLICK en una parada del mapa
2. SELECCIONA un evento (botones a la derecha)
3. OBSERVA cómo cambia la ruta óptima
4. ANALIZA el impacto de los eventos
5. LIMPIA eventos con el botón "Limpiar Todo"

📌 EVENTOS DISPONIBLES:
   🚗💥 Accidente (3x más lento)
   🌧️ Lluvia Fuerte (2.6x más lento)
   🚧 Protesta (3.75x más lento)
   🏗️ Construcción (4x más lento)

✅ ÁLGEBRA LINEAL DEMOSTRADA:
   • Matriz de distancias (n×n)
   • Aplicación de pesos dinámicos
   • Algoritmo de Dijkstra
   • Optimización en tiempo real
    """)
    
    # Crear visualizador
    print("\n" + "="*70)
    print("Abriendo interfaz gráfica...")
    print("="*70 + "\n")
    
    visualizador = VisualizadorInteractivo(sistema)
    visualizador.crear_interfaz()
    
    plt.tight_layout()
    plt.show()
    
    print("\n✅ Programa finalizado\n")
