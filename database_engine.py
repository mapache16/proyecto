"""
💾 DATABASE ENGINE
Sistema de persistencia para guardar y cargar escenarios de simulación
Permite guardar estados complejos rápidamente para sustentación
"""

import sqlite3
import json
import pickle
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import os

# ============================================================================
# 📋 DATABASE SCHEMA & MODELS
# ============================================================================

@dataclass
class ScenarioSnapshot:
    """Una fotografía de un escenario de simulación"""
    scenario_id: int
    name: str
    description: str
    created_at: str
    modified_at: str
    
    # Estado del entorno
    current_time: str  # HH:MM
    weather: str  # sunny, rain, storm, fog
    temperature: float
    demand_multiplier: float
    
    # Configuración de buses
    num_buses: int
    buses_data: str  # JSON serializado
    
    # Incidentes activos
    active_incidents: str  # JSON serializado
    
    # Botlenecks habilitados/deshabilitados
    bottlenecks_config: str  # JSON serializado
    
    # Etiquetas
    tags: str  # comma-separated
    
    # Métricas snapshot
    avg_occupancy: float
    total_passengers: int
    active_incident_count: int

@dataclass
class ScenarioTemplate:
    """Template predefinido para escenarios comunes"""
    template_id: int
    name: str
    description: str
    scenario_data: str  # JSON de configuración
    difficulty: str  # easy, medium, hard
    expected_duration: int  # minutos

# ============================================================================
# 💾 DATABASE MANAGER
# ============================================================================

class DatabaseManager:
    """Gestor de base de datos para escenarios"""
    
    def __init__(self, db_path: str = "bus_simulator.db"):
        self.db_path = db_path
        self.connection = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Crea las tablas si no existen"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        cursor = self.connection.cursor()
        
        # Tabla de escenarios guardados
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scenarios (
                scenario_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP NOT NULL,
                modified_at TIMESTAMP NOT NULL,
                current_time TEXT NOT NULL,
                weather TEXT NOT NULL,
                temperature REAL NOT NULL,
                demand_multiplier REAL NOT NULL,
                num_buses INTEGER NOT NULL,
                buses_data TEXT NOT NULL,
                active_incidents TEXT NOT NULL,
                bottlenecks_config TEXT NOT NULL,
                tags TEXT,
                avg_occupancy REAL,
                total_passengers INTEGER,
                active_incident_count INTEGER,
                simulation_step INTEGER DEFAULT 0
            )
        """)
        
        # Tabla de templates predefinidos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scenario_templates (
                template_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                scenario_data TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                expected_duration INTEGER NOT NULL,
                created_at TIMESTAMP NOT NULL
            )
        """)
        
        # Tabla de histórico (para auditoría)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scenario_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                scenario_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                details TEXT,
                FOREIGN KEY(scenario_id) REFERENCES scenarios(scenario_id)
            )
        """)
        
        self.connection.commit()
    
    def save_scenario(self,
                     name: str,
                     description: str,
                     environment_state: Dict,
                     buses_state: List[Dict],
                     incidents: List[Dict],
                     bottlenecks_config: Dict,
                     tags: List[str] = None) -> int:
        """Guarda un escenario completo"""
        
        cursor = self.connection.cursor()
        now = datetime.now().isoformat()
        tags_str = ",".join(tags) if tags else ""
        
        try:
            cursor.execute("""
                INSERT INTO scenarios (
                    name, description, created_at, modified_at,
                    current_time, weather, temperature, demand_multiplier,
                    num_buses, buses_data, active_incidents, bottlenecks_config,
                    tags, avg_occupancy, total_passengers, active_incident_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name, description, now, now,
                environment_state.get('time', '12:00'),
                environment_state.get('weather', 'sunny'),
                environment_state.get('temperature', 22.0),
                environment_state.get('demand_multiplier', 1.0),
                len(buses_state),
                json.dumps(buses_state),
                json.dumps(incidents),
                json.dumps(bottlenecks_config),
                tags_str,
                environment_state.get('avg_occupancy', 0.5),
                environment_state.get('total_passengers', 0),
                len(incidents)
            ))
            
            self.connection.commit()
            scenario_id = cursor.lastrowid
            
            # Registrar en histórico
            self._record_history(scenario_id, 'CREATE', 'Escenario creado')
            
            return scenario_id
        
        except sqlite3.IntegrityError:
            raise ValueError(f"Escenario con nombre '{name}' ya existe")
    
    def update_scenario(self,
                       scenario_id: int,
                       environment_state: Dict,
                       buses_state: List[Dict],
                       incidents: List[Dict]) -> bool:
        """Actualiza un escenario existente"""
        
        cursor = self.connection.cursor()
        now = datetime.now().isoformat()
        
        cursor.execute("""
            UPDATE scenarios SET
                modified_at = ?,
                current_time = ?,
                weather = ?,
                temperature = ?,
                demand_multiplier = ?,
                buses_data = ?,
                active_incidents = ?,
                avg_occupancy = ?,
                total_passengers = ?,
                active_incident_count = ?
            WHERE scenario_id = ?
        """, (
            now,
            environment_state.get('time', '12:00'),
            environment_state.get('weather', 'sunny'),
            environment_state.get('temperature', 22.0),
            environment_state.get('demand_multiplier', 1.0),
            json.dumps(buses_state),
            json.dumps(incidents),
            environment_state.get('avg_occupancy', 0.5),
            environment_state.get('total_passengers', 0),
            len(incidents),
            scenario_id
        ))
        
        self.connection.commit()
        self._record_history(scenario_id, 'UPDATE', 'Escenario actualizado')
        
        return cursor.rowcount > 0
    
    def load_scenario(self, scenario_id: int) -> Optional[Dict]:
        """Carga un escenario por ID"""
        
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM scenarios WHERE scenario_id = ?
        """, (scenario_id,))
        
        row = cursor.fetchone()
        
        if not row:
            return None
        
        return {
            'scenario_id': row['scenario_id'],
            'name': row['name'],
            'description': row['description'],
            'created_at': row['created_at'],
            'modified_at': row['modified_at'],
            'environment_state': {
                'time': row['current_time'],
                'weather': row['weather'],
                'temperature': row['temperature'],
                'demand_multiplier': row['demand_multiplier'],
                'avg_occupancy': row['avg_occupancy'],
                'total_passengers': row['total_passengers'],
            },
            'buses_state': json.loads(row['buses_data']),
            'incidents': json.loads(row['active_incidents']),
            'bottlenecks_config': json.loads(row['bottlenecks_config']),
            'tags': row['tags'].split(',') if row['tags'] else [],
        }
    
    def load_scenario_by_name(self, name: str) -> Optional[Dict]:
        """Carga un escenario por nombre"""
        
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT scenario_id FROM scenarios WHERE name = ?
        """, (name,))
        
        row = cursor.fetchone()
        
        if not row:
            return None
        
        return self.load_scenario(row['scenario_id'])
    
    def list_scenarios(self, tags: List[str] = None) -> List[Dict]:
        """Lista todos los escenarios guardados"""
        
        cursor = self.connection.cursor()
        
        if tags:
            # Buscar escenarios con los tags especificados
            placeholders = ','.join(['?' for _ in tags])
            cursor.execute(f"""
                SELECT scenario_id, name, description, created_at, modified_at,
                       tags, avg_occupancy, total_passengers
                FROM scenarios
                WHERE tags LIKE '%' || ? || '%'
                ORDER BY modified_at DESC
            """, (tags[0],))
        else:
            cursor.execute("""
                SELECT scenario_id, name, description, created_at, modified_at,
                       tags, avg_occupancy, total_passengers
                FROM scenarios
                ORDER BY modified_at DESC
            """)
        
        scenarios = []
        for row in cursor.fetchall():
            scenarios.append({
                'scenario_id': row['scenario_id'],
                'name': row['name'],
                'description': row['description'],
                'created_at': row['created_at'],
                'modified_at': row['modified_at'],
                'tags': row['tags'].split(',') if row['tags'] else [],
                'avg_occupancy': row['avg_occupancy'],
                'total_passengers': row['total_passengers'],
            })
        
        return scenarios
    
    def delete_scenario(self, scenario_id: int) -> bool:
        """Elimina un escenario"""
        
        cursor = self.connection.cursor()
        
        # Eliminar histórico primero
        cursor.execute("""
            DELETE FROM scenario_history WHERE scenario_id = ?
        """, (scenario_id,))
        
        # Luego eliminar escenario
        cursor.execute("""
            DELETE FROM scenarios WHERE scenario_id = ?
        """, (scenario_id,))
        
        self.connection.commit()
        
        return cursor.rowcount > 0
    
    def search_scenarios(self, query: str) -> List[Dict]:
        """Busca escenarios por nombre o descripción"""
        
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT scenario_id, name, description, created_at, modified_at,
                   tags, avg_occupancy, total_passengers
            FROM scenarios
            WHERE name LIKE ? OR description LIKE ?
            ORDER BY modified_at DESC
        """, (f'%{query}%', f'%{query}%'))
        
        scenarios = []
        for row in cursor.fetchall():
            scenarios.append({
                'scenario_id': row['scenario_id'],
                'name': row['name'],
                'description': row['description'],
                'created_at': row['created_at'],
                'modified_at': row['modified_at'],
                'tags': row['tags'].split(',') if row['tags'] else [],
                'avg_occupancy': row['avg_occupancy'],
                'total_passengers': row['total_passengers'],
            })
        
        return scenarios
    
    def _record_history(self, scenario_id: int, action: str, details: str):
        """Registra una acción en el histórico"""
        
        cursor = self.connection.cursor()
        now = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO scenario_history (scenario_id, action, timestamp, details)
            VALUES (?, ?, ?, ?)
        """, (scenario_id, action, now, details))
        
        self.connection.commit()
    
    def get_scenario_history(self, scenario_id: int) -> List[Dict]:
        """Obtiene el histórico de cambios de un escenario"""
        
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM scenario_history
            WHERE scenario_id = ?
            ORDER BY timestamp DESC
        """, (scenario_id,))
        
        history = []
        for row in cursor.fetchall():
            history.append({
                'action': row['action'],
                'timestamp': row['timestamp'],
                'details': row['details'],
            })
        
        return history
    
    def save_template(self,
                     name: str,
                     description: str,
                     scenario_data: Dict,
                     difficulty: str = 'medium',
                     expected_duration: int = 30) -> int:
        """Guarda un template de escenario"""
        
        cursor = self.connection.cursor()
        now = datetime.now().isoformat()
        
        try:
            cursor.execute("""
                INSERT INTO scenario_templates (
                    name, description, scenario_data, difficulty,
                    expected_duration, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name, description, json.dumps(scenario_data),
                difficulty, expected_duration, now
            ))
            
            self.connection.commit()
            return cursor.lastrowid
        
        except sqlite3.IntegrityError:
            raise ValueError(f"Template con nombre '{name}' ya existe")
    
    def list_templates(self, difficulty: str = None) -> List[Dict]:
        """Lista los templates disponibles"""
        
        cursor = self.connection.cursor()
        
        if difficulty:
            cursor.execute("""
                SELECT * FROM scenario_templates
                WHERE difficulty = ?
                ORDER BY created_at DESC
            """, (difficulty,))
        else:
            cursor.execute("""
                SELECT * FROM scenario_templates
                ORDER BY created_at DESC
            """)
        
        templates = []
        for row in cursor.fetchall():
            templates.append({
                'template_id': row['template_id'],
                'name': row['name'],
                'description': row['description'],
                'difficulty': row['difficulty'],
                'expected_duration': row['expected_duration'],
                'scenario_data': json.loads(row['scenario_data']),
            })
        
        return templates
    
    def load_template(self, template_id: int) -> Optional[Dict]:
        """Carga un template"""
        
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM scenario_templates WHERE template_id = ?
        """, (template_id,))
        
        row = cursor.fetchone()
        
        if not row:
            return None
        
        return {
            'template_id': row['template_id'],
            'name': row['name'],
            'description': row['description'],
            'difficulty': row['difficulty'],
            'expected_duration': row['expected_duration'],
            'scenario_data': json.loads(row['scenario_data']),
        }
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if self.connection:
            self.connection.close()

# ============================================================================
# 📊 SCENARIO BUILDER
# ============================================================================

class ScenarioBuilder:
    """Constructor de escenarios para simplificar la creación"""
    
    def __init__(self):
        self.scenario_data = {
            'name': '',
            'description': '',
            'environment_state': {
                'time': '12:00',
                'weather': 'sunny',
                'temperature': 22.0,
                'demand_multiplier': 1.0,
                'avg_occupancy': 0.5,
                'total_passengers': 0,
            },
            'buses_state': [],
            'incidents': [],
            'bottlenecks_config': {},
            'tags': [],
        }
    
    def set_name(self, name: str):
        self.scenario_data['name'] = name
        return self
    
    def set_description(self, description: str):
        self.scenario_data['description'] = description
        return self
    
    def set_time(self, hour: int, minute: int = 0):
        self.scenario_data['environment_state']['time'] = f"{hour:02d}:{minute:02d}"
        return self
    
    def set_weather(self, weather: str):
        self.scenario_data['environment_state']['weather'] = weather
        return self
    
    def set_demand(self, multiplier: float):
        self.scenario_data['environment_state']['demand_multiplier'] = multiplier
        return self
    
    def add_incident(self, incident_type: str, lat: float, lon: float, severity: float):
        self.scenario_data['incidents'].append({
            'type': incident_type,
            'location': [lat, lon],
            'severity': severity,
        })
        return self
    
    def add_tag(self, tag: str):
        if tag not in self.scenario_data['tags']:
            self.scenario_data['tags'].append(tag)
        return self
    
    def disable_bottleneck(self, bottleneck_name: str):
        self.scenario_data['bottlenecks_config'][bottleneck_name] = False
        return self
    
    def build(self) -> Dict:
        return self.scenario_data

# ============================================================================
# 🎮 PRESET SCENARIOS
# ============================================================================

PRESET_SCENARIOS = {
    'normal': {
        'name': 'Sistema Normal',
        'description': 'Operación regular sin eventos especiales',
        'time': '12:00',
        'weather': 'sunny',
        'demand': 1.0,
        'incidents': [],
        'difficulty': 'easy',
    },
    'peak_hour': {
        'name': 'Hora Pico Mañana',
        'description': 'Máxima demanda en horario de entrada (8 AM)',
        'time': '08:00',
        'weather': 'sunny',
        'demand': 3.0,  # Triplicada
        'incidents': [],
        'difficulty': 'medium',
    },
    'rainy_peak': {
        'name': 'Lluvia + Hora Pico',
        'description': 'Lluvia durante hora pico - situación caótica',
        'time': '08:00',
        'weather': 'rain',
        'demand': 3.0,
        'incidents': [],
        'difficulty': 'hard',
    },
    'accident_viaduct': {
        'name': 'Accidente en El Viaducto',
        'description': 'Accidente en cuello de botella crítico',
        'time': '14:00',
        'weather': 'sunny',
        'demand': 1.5,
        'incidents': [{
            'type': 'accident',
            'location': [4.72, -74.08],
            'severity': 0.9,
        }],
        'difficulty': 'medium',
    },
    'manifestation': {
        'name': 'Manifestación en Centro',
        'description': 'Protesta que cierra vías principales',
        'time': '15:00',
        'weather': 'sunny',
        'demand': 2.0,
        'incidents': [{
            'type': 'manifestation',
            'location': [4.71, -74.07],
            'severity': 1.0,
        }],
        'difficulty': 'hard',
    },
    'nighttime': {
        'name': 'Servicio Nocturno',
        'description': 'Operación de madrugada (baja demanda)',
        'time': '02:00',
        'weather': 'sunny',
        'demand': 0.2,
        'incidents': [],
        'difficulty': 'easy',
    },
}
