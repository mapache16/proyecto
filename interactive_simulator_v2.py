"""
🎮 ADVANCED INTERACTIVE SIMULATOR - VERSIÓN 2.0
Dashboard mejorado con fluctuaciones del entorno, comportamiento operativo 
y controles interactivos para demostración
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple

# Importar módulos creados
from fluctuations_engine import (
    EnvironmentalConditions,
    BusOperationalState,
    BusStop,
    Incident,
    IncidentType,
    BottleneckEngine,
    AccordionEffectDetector,
    WaitingTimeCalculator,
    RandomEventGenerator,
    Weather,
    TimeOfDay,
    Bottleneck,
    BOTTLENECK_LOCATIONS
)

# ============================================================================
# 🎨 STREAMLIT PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="🚌 Advanced Bus Simulator 2.0",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS avanzado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #667eea;
        margin: 10px 0;
    }
    
    .alert-critical {
        background-color: #f8d7da;
        padding: 12px;
        border-radius: 5px;
        border-left: 5px solid #dc3545;
        margin: 10px 0;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        padding: 12px;
        border-radius: 5px;
        border-left: 5px solid #ffc107;
        margin: 10px 0;
    }
    
    .alert-success {
        background-color: #d4edda;
        padding: 12px;
        border-radius: 5px;
        border-left: 5px solid #28a745;
        margin: 10px 0;
    }
    
    .occupancy-bar {
        display: inline-block;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 🏗️ ENHANCED BUS & SYSTEM CLASSES
# ============================================================================

class AdvancedBus:
    """Bus mejorado con comportamiento operativo realista"""
    
    def __init__(self, bus_id: int, route_id: int, max_capacity: int = 80, num_stops: int = 10):
        self.bus_id = bus_id
        self.route_id = route_id
        self.operational_state = BusOperationalState(
            bus_id=bus_id,
            max_capacity=max_capacity,
            total_stops=num_stops
        )
        
        # Ubicación
        self.current_lat = 4.71
        self.current_lon = -74.07
        self.current_station = 0
        
        # Performance
        self.total_passengers_transported = 0
        self.trip_count = 0
    
    def update_position(self, 
                       env: EnvironmentalConditions,
                       bottleneck_engine: BottleneckEngine,
                       distance_to_next_stop: float = 1.5):
        """Actualiza posición considerando condiciones del entorno"""
        
        if self.operational_state.is_broken:
            self.operational_state.time_broken += 1
            if self.operational_state.time_broken > random.randint(15, 30):
                self.operational_state.is_broken = False
                self.operational_state.time_broken = 0
            return
        
        # Velocidad base afectada por clima
        base_speed = 30 * env.speed_factor  # 30 km/h ajustado por clima
        
        # Reducción por cuello de botella
        bottleneck_factor = bottleneck_engine.get_speed_reduction_at_location(
            self.current_lat, self.current_lon
        )
        
        # Velocidad final
        effective_speed = base_speed * bottleneck_factor
        
        # Reducción adicional por congestión
        congestion_factor = min(1.0, env.demand_multiplier / 3.0)
        effective_speed *= (1 - congestion_factor * 0.3)
        
        # Mover bus
        distance_traveled = (effective_speed / 60) / 60  # km por segundo simulado
        self.current_lat += distance_traveled * 0.01
        self.current_lon += distance_traveled * 0.01

class AdvancedBusNetwork:
    """Red avanzada de autobuses con todas las fluctuaciones"""
    
    def __init__(self, num_buses: int = 20, num_stops: int = 10):
        self.num_buses = num_buses
        self.num_stops = num_stops
        self.buses: List[AdvancedBus] = []
        self.stops: List[BusStop] = []
        self.simulation_time = datetime.now()
        
        # Motores
        self.environment = EnvironmentalConditions()
        self.bottleneck_engine = BottleneckEngine()
        self.accordion_detector = AccordionEffectDetector()
        self.waiting_calculator = WaitingTimeCalculator()
        self.event_generator = RandomEventGenerator()
        
        # Histórico
        self.history: List[Dict] = []
        
        self._initialize_network()
    
    def _initialize_network(self):
        """Inicializa la red de autobuses y paradas"""
        # Crear buses
        for i in range(self.num_buses):
            bus = AdvancedBus(
                bus_id=i+1,
                route_id=i % 5 + 1,
                max_capacity=80,
                num_stops=self.num_stops
            )
            self.buses.append(bus)
        
        # Crear paradas
        for i in range(self.num_stops):
            stop = BusStop(
                stop_id=i+1,
                name=f"Parada {i+1}",
                lat=4.70 + i * 0.02,
                lon=-74.08 + i * 0.01,
                capacity=100
            )
            self.stops.append(stop)
    
    def update_step(self, 
                   generate_random_events: bool = True,
                   simulation_speed: float = 1.0):
        """Ejecuta un paso de simulación"""
        
        # Avanzar tiempo
        self.environment.update_time(minutes=int(simulation_speed))
        self.simulation_time += timedelta(minutes=simulation_speed)
        
        # Generar eventos aleatorios
        if generate_random_events:
            incident = self.event_generator.generate_random_incident(
                self.simulation_time,
                probability=0.01 * simulation_speed
            )
            if incident:
                st.sidebar.warning(f"⚠️ {incident.incident_type.value.upper()} generado!")
        
        # Actualizar incidentes activos
        self.event_generator.update_incidents(self.simulation_time)
        
        # Actualizar cada bus
        for bus in self.buses:
            bus.update_position(
                self.environment,
                self.bottleneck_engine
            )
            
            # Pasajeros en paradas subiendo/bajando
            if random.random() > 0.7:
                passengers_to_board = random.randint(1, 15)
                boarded, boarding_time = bus.operational_state.board_passengers(passengers_to_board)
                
                # Calcular tiempo de espera
                wait_time = (boarding_time / 60)  # convertir a minutos
                self.waiting_calculator.update_wait_time(wait_time)
        
        # Detectar efecto acordeón
        bunching_report = self.accordion_detector.get_bunching_report(self.buses)
        
        # Guardar histórico
        self._record_history(bunching_report)
    
    def _record_history(self, bunching_report: Dict):
        """Guarda el estado actual en el histórico"""
        state = {
            'timestamp': self.simulation_time,
            'avg_occupancy': np.mean([b.operational_state.get_occupancy_rate() 
                                     for b in self.buses]),
            'avg_delay': np.mean([b.operational_state.total_delay_accumulated 
                                 for b in self.buses]),
            'total_passengers': sum([b.operational_state.current_passengers 
                                    for b in self.buses]),
            'congestion': self.environment.demand_multiplier / 3.0,
            'wait_time': self.waiting_calculator.average_wait_time,
            'bunched_buses': bunching_report['total_bunched_buses'],
            'demand_multiplier': self.environment.demand_multiplier,
            'active_incidents': len(self.event_generator.active_incidents)
        }
        self.history.append(state)
        
        # Limitar histórico a últimos 500 registros
        if len(self.history) > 500:
            self.history = self.history[-500:]
    
    def get_metrics(self) -> Dict:
        """Obtiene métricas actuales del sistema"""
        occupancy_rates = [b.operational_state.get_occupancy_rate() for b in self.buses]
        
        return {
            'time': self.simulation_time.strftime("%Y-%m-%d %H:%M"),
            'total_buses': len(self.buses),
            'avg_occupancy': np.mean(occupancy_rates) * 100,
            'max_occupancy': np.max(occupancy_rates) * 100 if occupancy_rates else 0,
            'avg_delay': np.mean([b.operational_state.total_delay_accumulated for b in self.buses]),
            'total_passengers': sum([b.operational_state.current_passengers for b in self.buses]),
            'congestion': self.environment.demand_multiplier / 3.0 * 100,
            'avg_wait_time': self.waiting_calculator.average_wait_time,
            'is_peak_hour': self.environment.is_peak_hour,
            'weather': self.environment.weather.value,
            'temperature': self.environment.temperature,
            'active_incidents': len(self.event_generator.active_incidents),
            'turned_away_total': sum([b.operational_state.times_turned_away_passengers 
                                     for b in self.buses]),
            'demand_multiplier': self.environment.demand_multiplier,
            'speed_factor': self.environment.speed_factor,
        }

# ============================================================================
# 🎮 STREAMLIT APP
# ============================================================================

def main():
    # Inicializar estado
    if 'network' not in st.session_state:
        st.session_state.network = AdvancedBusNetwork(num_buses=20, num_stops=10)
        st.session_state.is_running = False
        st.session_state.simulation_speed = 1.0
        st.session_state.step_count = 0
    
    network = st.session_state.network
    
    # ========================================================================
    # HEADER
    # ========================================================================
    
    st.markdown("""
    <div class="main-header">
        <h1>🚌 Advanced Bus Traffic Simulator 2.0</h1>
        <p>Simulador interactivo con fluctuaciones del entorno, 
        comportamiento operativo y análisis avanzado</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # SIDEBAR - CONTROLES
    # ========================================================================
    
    with st.sidebar:
        st.markdown("## 🎮 CONTROLES")
        
        # Control de simulación
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("▶️ Play", use_container_width=True):
                st.session_state.is_running = True
        with col2:
            if st.button("⏸️ Pause", use_container_width=True):
                st.session_state.is_running = False
        with col3:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.network = AdvancedBusNetwork()
                st.session_state.is_running = False
                st.session_state.step_count = 0
        
        st.markdown("---")
        
        # ========================================================================
        # 🌤️ ENVIRONMENTAL CONTROLS
        # ========================================================================
        
        st.markdown("### 🌍 FLUCTUACIONES DEL ENTORNO")
        
        # Hora del día
        st.subheader("⏰ Hora del Día")
        selected_hour = st.slider("Selecciona hora", 0, 23, 
                                 value=network.environment.current_time.hour)
        selected_minute = st.slider("Minutos", 0, 59,
                                   value=network.environment.current_time.minute)
        
        network.environment.current_time = network.environment.current_time.replace(
            hour=selected_hour,
            minute=selected_minute
        )
        network.environment._update_time_period()
        network.environment._calculate_demand_multiplier()
        
        # Mostrar si es hora pico
        if network.environment.is_peak_hour:
            st.markdown("""
            <div class="alert-critical">
                🔴 ¡HORA PICO! Demanda se ha TRIPLICADO
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Clima
        st.subheader("🌤️ Clima")
        weather_option = st.selectbox(
            "Condiciones climáticas",
            [w.value for w in Weather],
            index=0
        )
        network.environment.set_weather(Weather(weather_option))
        
        if network.environment.weather != Weather.SUNNY:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📉 Velocidad", 
                         f"{network.environment.speed_factor*100:.0f}%")
            with col2:
                st.metric("⬆️ Demanda", 
                         f"+{network.environment.passenger_demand_boost*100:.0f}%")
        
        st.markdown("---")
        
        # ========================================================================
        # 🚧 OPERATIONAL CONTROLS
        # ========================================================================
        
        st.markdown("### 🚌 COMPORTAMIENTO OPERATIVO")
        
        # Demanda de pasajeros
        demand = st.slider(
            "📊 Demanda de Pasajeros",
            min_value=0.5, max_value=2.0, value=1.0, step=0.1
        )
        network.environment.demand_multiplier = demand
        
        # Velocidad de simulación
        sim_speed = st.slider(
            "⏱️ Velocidad de Simulación",
            min_value=0.5, max_value=10.0, value=1.0, step=0.5
        )
        st.session_state.simulation_speed = sim_speed
        
        st.markdown("---")
        
        # ========================================================================
        # 🚧 INCIDENT CONTROLS
        # ========================================================================
        
        st.markdown("### 🚧 INYECTAR CAOS")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚗 Accidente", use_container_width=True):
                incident = Incident(
                    incident_id=len(network.event_generator.active_incidents),
                    incident_type=IncidentType.ACCIDENT,
                    location=(4.71, -74.07),
                    duration=30,
                    severity=0.8
                )
                network.event_generator.add_manual_incident(incident)
                st.success("🚗 Accidente generado")
        
        with col2:
            if st.button("🛑 Manifestación", use_container_width=True):
                incident = Incident(
                    incident_id=len(network.event_generator.active_incidents),
                    incident_type=IncidentType.MANIFESTATION,
                    location=(4.71, -74.07),
                    duration=60,
                    severity=0.9
                )
                network.event_generator.add_manual_incident(incident)
                st.success("🛑 Manifestación creada")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔧 Fallo Mecánico", use_container_width=True):
                random_bus = random.choice(network.buses)
                random_bus.operational_state.is_broken = True
                st.warning(f"🔧 Bus {random_bus.bus_id} averiad@")
        
        with col2:
            if st.button("🚔 Control Policial", use_container_width=True):
                incident = Incident(
                    incident_id=len(network.event_generator.active_incidents),
                    incident_type=IncidentType.POLICE_CONTROL,
                    location=(4.71, -74.07),
                    duration=20,
                    severity=0.6
                )
                network.event_generator.add_manual_incident(incident)
                st.info("🚔 Control policial activado")
        
        st.markdown("---")
        
        # ========================================================================
        # 🗺️ BOTTLENECK CONTROLS
        # ========================================================================
        
        st.markdown("### 🗺️ Cuellos de Botella")
        
        for bottleneck in Bottleneck:
            location = BOTTLENECK_LOCATIONS[bottleneck]
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"📍 {location['name']}")
            with col2:
                status = "✅" if network.bottleneck_engine.active_bottlenecks[bottleneck] else "❌"
                if st.button(status, key=bottleneck.value, use_container_width=True):
                    network.bottleneck_engine.toggle_bottleneck(bottleneck)
    
    # ========================================================================
    # ACTUALIZAR SIMULACIÓN
    # ========================================================================
    
    if st.session_state.is_running:
        for _ in range(int(st.session_state.simulation_speed)):
            network.update_step()
            st.session_state.step_count += 1
        st.rerun()
    
    # ========================================================================
    # MAIN CONTENT - MÉTRICAS
    # ========================================================================
    
    metrics = network.get_metrics()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🚌 Buses", f"{metrics['total_buses']}", "Activos")
    
    with col2:
        color = "🔴" if metrics['max_occupancy'] > 85 else "🟡" if metrics['max_occupancy'] > 70 else "🟢"
        st.metric("👥 Ocupación", f"{metrics['avg_occupancy']:.0f}%", color)
    
    with col3:
        color = "🔴" if metrics['avg_delay'] > 15 else "🟡" if metrics['avg_delay'] > 5 else "🟢"
        st.metric("⏱️ Delay", f"{metrics['avg_delay']:.1f}m", color)
    
    with col4:
        color = "🔴" if metrics['congestion'] > 70 else "🟡" if metrics['congestion'] > 40 else "🟢"
        st.metric("🚗 Congestión", f"{metrics['congestion']:.0f}%", color)
    
    with col5:
        st.metric("⏰ Tiempo Espera", f"{metrics['avg_wait_time']:.1f}m", "Promedio")
    
    st.markdown("---")
    
    # ========================================================================
    # INFORMACIÓN DEL ENTORNO
    # ========================================================================
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        env_info = network.environment.get_display_info()
        st.markdown(f"""
        <div class="metric-card">
            <h4>⏰ Hora Simulada</h4>
            <p style="font-size: 24px; color: #667eea; font-weight: bold;">
                {env_info['time']}
            </p>
            <p style="font-size: 14px;">
                Período: <strong>{env_info['period']}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>🌤️ Clima</h4>
            <p style="font-size: 18px;">
                {env_info['weather'].upper()}
            </p>
            <p style="font-size: 14px;">
                Temp: <strong>{env_info['temperature']:.0f}°C</strong><br>
                Humedad: <strong>{env_info['humidity']:.0f}%</strong><br>
                Viento: <strong>{env_info['wind_speed']:.0f} km/h</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>📊 Factores</h4>
            <p style="font-size: 14px;">
                Demanda: <strong>x{env_info['demand_multiplier']}</strong><br>
                Velocidad: <strong>x{env_info['speed_factor']:.2f}</strong><br>
                Boost Pasajeros: <strong>+{env_info['passenger_boost']:.0f}%</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # ALERTAS CRÍTICAS
    # ========================================================================
    
    alerts_col1, alerts_col2, alerts_col3 = st.columns(3)
    
    with alerts_col1:
        if metrics['max_occupancy'] > 85:
            st.markdown("""
            <div class="alert-critical">
                🔴 <strong>OCUPACIÓN CRÍTICA</strong><br>
                Buses con capacidad limitada
            </div>
            """, unsafe_allow_html=True)
    
    with alerts_col2:
        if metrics['avg_delay'] > 15:
            st.markdown("""
            <div class="alert-critical">
                🔴 <strong>RETRASOS SEVEROS</strong><br>
                Sistema sobrecargado
            </div>
            """, unsafe_allow_html=True)
    
    with alerts_col3:
        if metrics['congestion'] > 70:
            st.markdown("""
            <div class="alert-critical">
                🔴 <strong>CONGESTIÓN ALTA</strong><br>
                Considerar desvíos
            </div>
            """, unsafe_allow_html=True)
    
    # Efecto acordeón
    bunching_report = network.accordion_detector.get_bunching_report(network.buses)
    if bunching_report['total_bunched_buses'] > 0:
        st.markdown(f"""
        <div class="alert-warning">
            🚌 <strong>EFECTO ACORDEÓN DETECTADO</strong><br>
            {bunching_report['total_bunched_buses']} buses agrupados en {bunching_report['number_of_groups']} grupos<br>
            <em>Bus bunching: fenómeno donde buses se agrupan por congestión</em>
        </div>
        """, unsafe_allow_html=True)
    
    # Pasajeros rechazados
    if metrics['turned_away_total'] > 0:
        st.markdown(f"""
        <div class="alert-warning">
            ❌ <strong>PASAJEROS RECHAZADOS</strong><br>
            {metrics['turned_away_total']} veces buses llegaron llenos
        </div>
        """, unsafe_allow_html=True)
    
    # Incidentes activos
    if network.event_generator.active_incidents:
        st.markdown("### 🚧 Incidentes Activos")
        for incident_info in network.event_generator.get_active_incidents_info():
            st.info(f"**{incident_info['type'].upper()}** - Severidad: {incident_info['severity']} - Quedan: {incident_info['time_remaining']}m")
    
    st.markdown("---")
    
    # ========================================================================
    # GRÁFICOS
    # ========================================================================
    
    if len(network.history) > 1:
        history_df = pd.DataFrame(network.history)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=range(len(history_df)),
                y=history_df['avg_occupancy'] * 100,
                fill='tozeroy',
                name='Ocupación',
                line=dict(color='#667eea', width=2)
            ))
            fig.update_layout(
                title="📊 Ocupación Promedio (Histórico)",
                xaxis_title="Paso de Simulación",
                yaxis_title="Ocupación (%)",
                height=400,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=range(len(history_df)),
                y=history_df['wait_time'],
                fill='tozeroy',
                name='Tiempo Espera',
                line=dict(color='#764ba2', width=2)
            ))
            fig.update_layout(
                title="⏱️ Tiempo Promedio de Espera",
                xaxis_title="Paso de Simulación",
                yaxis_title="Minutos",
                height=400,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=range(len(history_df)),
                y=history_df['total_passengers'],
                fill='tozeroy',
                name='Pasajeros',
                line=dict(color='#28a745', width=2)
            ))
            fig.update_layout(
                title="👥 Pasajeros Totales en Sistema",
                xaxis_title="Paso de Simulación",
                yaxis_title="Cantidad",
                height=400,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=range(len(history_df)),
                y=history_df['bunched_buses'],
                fill='tozeroy',
                name='Buses Agrupados',
                line=dict(color='#dc3545', width=2)
            ))
            fig.update_layout(
                title="🚌 Efecto Acordeón (Bus Bunching)",
                xaxis_title="Paso de Simulación",
                yaxis_title="Buses Agrupados",
                height=400,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # TABLA DE BUSES
    # ========================================================================
    
    st.markdown("## 🚌 ESTADO DE AUTOBUSES")
    
    bus_data = []
    for bus in network.buses[:10]:  # Primeros 10
        state = bus.operational_state
        occupancy_color = state.get_occupancy_color()
        
        bus_data.append({
            'ID': bus.bus_id,
            'Ruta': bus.route_id,
            'Pasajeros': f"{state.current_passengers}/{state.max_capacity}",
            'Ocupación': f"{state.get_occupancy_rate()*100:.1f}%",
            'Color': occupancy_color,
            'Estación': f"{state.current_stop_index}/{state.total_stops}",
            'Retrasos (m)': f"{state.total_delay_accumulated:.1f}",
            'Estado': "🔧 Averiad@" if state.is_broken else "✅ Normal"
        })
    
    bus_df = pd.DataFrame(bus_data)
    
    # Mostrar con colores
    def color_occupancy(val):
        colors = {
            'green': '#d4edda',
            'yellow': '#fff3cd',
            'orange': '#ffe0b2',
            'red': '#f8d7da'
        }
        color = colors.get(val, 'white')
        return f'background-color: {color}'
    
    st.dataframe(bus_df.drop('Color', axis=1), use_container_width=True)
    
    st.markdown("---")
    
    # Info estadísticas
    wait_stats = network.waiting_calculator.get_wait_time_percentiles()
    
    st.markdown("### 📈 Estadísticas de Tiempos de Espera")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("P50", f"{wait_stats['p50']:.1f}m", "Mediana")
    with col2:
        st.metric("P75", f"{wait_stats['p75']:.1f}m", "75%")
    with col3:
        st.metric("P95", f"{wait_stats['p95']:.1f}m", "95%")
    with col4:
        st.metric("P99", f"{wait_stats['p99']:.1f}m", "99%")
    with col5:
        st.metric("Máx", f"{wait_stats['max']:.1f}m", "Pico")

if __name__ == "__main__":
    main()
