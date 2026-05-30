# 🚌 ADVANCED BUS SIMULATOR 2.0 - GUÍA COMPLETA

## 🎯 ¿Qué es lo nuevo?

Esta es la **versión mejorada y mucho más realista** del simulador. Ahora incluye:

### 🌍 1. FLUCTUACIONES DEL ENTORNO (El Caos de la Ciudad)

#### Horas Pico vs. Valle
```
⏰ HORA PICO (6-9 AM, 5-8 PM):
   📈 Demanda → SE TRIPLICA (3.0x)
   📉 Velocidad → Se reduce 20-30%
   👥 Ocupación → Sube a 75-90%
   ⏱️ Delays → Aumentan significativamente

⏰ HORA VALLE (Madrugada):
   📉 Demanda → Baja a 0.2x
   📈 Velocidad → Máxima
   👥 Ocupación → 20-30%
   ⏱️ Delays → Mínimos
```

#### 🌤️ Clima (El Botón de "Lluvia")
Cuando activas lluvia:
- 🚗 **Velocidad**: Baja 20-30% (los buses van más lento)
- ⏱️ **Tiempo de frenado**: Aumenta proporcionalmente
- 👥 **Demanda de pasajeros**: SUBE (+40%)
  - *¿Por qué?* Porque la gente no quiere caminar o ir en moto con lluvia

**Opciones climáticas disponibles:**
- ☀️ **Sunny**: Condiciones normales
- 🌧️ **Rain**: Lluvia moderada (20-30% velocidad reducida)
- ⛈️ **Storm**: Tormenta severa (50-65% velocidad reducida)
- 🌫️ **Fog**: Niebla (40% visibilidad reducida)

#### 🗺️ Cuellos de Botella Locales (Geografía de la Ciudad)
El simulador incluye 5 cuellos de botella reales:

| Cuello de Botella | Coordenadas | Impacto | Puedes Activar/Desactivar |
|------------------|-------------|--------|--------------------------|
| **El Viaducto** | (4.72, -74.08) | -60% velocidad | ✅ Sí |
| **Gobernación** | (4.71, -74.06) | -50% velocidad | ✅ Sí |
| **Instituto de Movilidad** | (4.70, -74.07) | -55% velocidad | ✅ Sí |
| **Puente Sur** | (4.65, -74.08) | -65% velocidad | ✅ Sí |
| **Centro Comercial** | (4.75, -74.09) | -50% velocidad | ✅ Sí |

Cuando un bus pasa por estas coordenadas, **automáticamente reduce su velocidad**.

---

### 🚌 2. FLUCTUACIONES OPERATIVAS (El Comportamiento Real del Bus)

Un bus NO es un punto que se mueve a velocidad constante. Tiene comportamiento realista:

#### 📦 Capacidad Máxima (El Bus va "a Reventar")
```
Capacidad: 80 personas

Escenario:
- Bus lleno (80/80) llega a parada
- Esperan 25 personas
- Bus SOLO puede recoger a 0
- Las 25 personas se quedan esperando ❌
- El sistema lo registra en "Pasajeros Rechazados"
```

**Impacto en el sistema:**
- Esos pasajeros esperan más tiempo
- El "tiempo de espera promedio" sube
- Se ve en el gráfico de "Tiempo de Espera"

#### ⏱️ Tiempos Variables de Abordaje
```
Tiempo en parada = (Pasajeros bajando × 3 seg) + (Pasajeros subiendo × 5 seg)

Ejemplo:
- 10 personas bajan: 10 × 3 = 30 segundos
- 15 personas suben: 15 × 5 = 75 segundos
- Total en parada: 105 segundos (1.75 minutos)

Si esto ocurre en 20 paradas:
- Delay acumulado: ~35 minutos
```

#### 🔧 Averías Mecánicas (Eventos Aleatorios)
Presiona el botón **"🔧 Fallo Mecánico"** para:
- Dañar un bus al azar
- Bus se queda **quieto en el mapa**
- Los buses detrás se atracan
- Ves cómo afecta al resto del sistema

**Estado visible en tabla:**
```
ID  Ruta  Pasajeros  Estado
5   2     45/80      🔧 Averiad@
```

---

### 🚗 3. INTERFAZ INTERACTIVA (Los "Juguetes" para la Demostración)

#### Sliders (Deslizadores) de Demanda
```
📊 Demanda de Pasajeros: 0.5x → 2.0x

- 0.5x = Sistema vacío, muy poco movimiento
- 1.0x = Demanda normal
- 1.5x = Bastante ocupado
- 2.0x = Caótico, buses llenos
```

#### Botones de "Inyectar Caos"

**🚗 Accidente**
- Reduce velocidad en 50%
- Dura 30 minutos
- Impacto: Los buses se atracan, ocupación sube

**🛑 Manifestación**
- Reduce velocidad en 60%
- Dura 60 minutos (más tiempo que accidente)
- Impacto: Severísimo, muchos pasajeros rechazados

**🔧 Fallo Mecánico**
- Deja un bus sin movimiento
- Efecto cascada en buses de atrás
- Ver en tiempo real cómo se propaga

**🚔 Control Policial**
- Reduce velocidad en 40%
- Dura 20 minutos
- Impacto: Moderado

#### ⏰ Control del Tiempo (Acelerador de Simulación)
```
⏱️ Velocidad de Simulación: 0.5x → 10.0x

- 1.0x = Tiempo real
- 2.0x = El doble de rápido
- 5.0x = 5 veces más rápido
- 10.0x = Ultra-rápido

No tienes que esperar 20 minutos reales para ver
un embotellamiento de 20 minutos simulados.
```

#### 🗓️ Control de Hora del Día
Cambia la hora manualmente:
- Mueve el slider de horas (0-23)
- Mueve el slider de minutos (0-59)
- El sistema automáticamente ajusta:
  - Demanda de pasajeros
  - Velocidad del tráfico
  - Todas las fluctuaciones

---

### 📊 4. MÉTRICAS DE IMPACTO (Datos que Reaccionan)

Los gráficos **cambian en tiempo real** cuando haces cambios:

#### 📈 Gráfico 1: Ocupación Promedio
```
Qué ves: Una línea que sube/baja según demanda
Reacción:
- Aumentas demanda → La línea sube
- Activas accidente → Pico en la línea
- Se recupera lentamente → Baja gradualmente
```

#### ⏱️ Gráfico 2: Tiempo Promedio de Espera
```
Qué ves: Cuánto esperan los pasajeros en paradas
Impacto:
- Inyectas caos → ⬆️ Sube drásticamente
- Bus se llena → Más gente espera
- Sistema se recupera → Baja lentamente
```

#### 👥 Gráfico 3: Pasajeros Totales en Sistema
```
Qué ves: Cuánta gente hay en buses en cada momento
Lógica:
- Hora pico → Suben rápido
- Accidente → Se quedan más tiempo (delays)
- Demanda baja → Bajan gradualmente
```

#### 🚌 Gráfico 4: Efecto Acordeón (Bus Bunching)
```
FENÓMENO REAL: Cuando hay congestión, un bus se retrasa
y el bus de atrás lo alcanza. Luego llegan JUNTOS a la
siguiente parada, sin separación entre ellos.

Qué ves en el gráfico:
- Si no hay problemas → 0 buses agrupados
- Si hay accidente → ⬆️ Picos de agrupamiento
- Cuando se recupera → Vuelve a 0

ALERTA AUTOMÁTICA:
"🚌 EFECTO ACORDEÓN DETECTADO
 3 buses agrupados en 2 grupos"
```

---

## 🎮 CÓMO JUGAR CON EL SIMULADOR

### Escenario 1: "Hora Pico Normal"
```
1. Abre RUN_SIMULATOR.md para instrucciones
2. Ejecuta: streamlit run interactive_simulator_v2.py
3. En el Sidebar:
   - Pon hora en 8:00 AM (hora pico mañana)
   - Demanda: 1.5x
   - Clima: Sunny
4. Presiona PLAY
5. Observa:
   - Ocupación sube a 60-70%
   - Tiempo espera aumenta
   - Demanda multiplier = 3.0
```

### Escenario 2: "Caos Total"
```
1. Comienzas en estado normal
2. PLAY para que corra 2 minutos
3. Presiona "🚗 Accidente"
4. Inmediatamente presiona "🛑 Manifestación"
5. Pon velocidad simulación a 5.0x para ver rápido
6. Observa:
   - Ocupación → Máxima (85%+)
   - Delays → Aumentan severamente
   - Pasajeros rechazados → Números crecen
   - Bus bunching → Múltiples grupos de buses agrupados
   - Tiempo espera → Gráfico dispara hacia arriba
```

### Escenario 3: "Lluvia Sorpresa"
```
1. Simulación corriendo en estado normal
2. Cambia clima de "sunny" a "rain"
3. Observa inmediatamente:
   - Velocidad de buses baja
   - Demanda de pasajeros SUBE (+40%)
   - Ocupación aumenta aunque demanda sea 1.0x
   - Tiempos de espera aumentan
```

### Escenario 4: "Desactivar Cuellos de Botella"
```
1. Simulación corriendo
2. En sidebar, busca "🗺️ Cuellos de Botella"
3. Haz clic en "El Viaducto" para desactivarlo
4. Luego desactiva "Gobernación"
5. Observa:
   - Ocupación baja
   - Delays disminuyen
   - Los buses van más rápido (no hay congestión geográfica)
```

---

## 📊 INTERPRETANDO LAS MÉTRICAS

### Ocupación (👥)
```
🟢 < 50%: Buses semivacíos, sistema con capacidad
🟡 50-70%: Normal, sistema funcionando bien
🟠 70-85%: Congestionado, difícil subirse
🔴 > 85%: CRÍTICO, pasajeros rechazados
```

### Tiempo de Espera (⏱️)
```
🟢 < 5 min: Muy bien, pasajeros felices
🟡 5-10 min: Aceptable
🟠 10-15 min: Molesto, pasajeros frustrados
🔴 > 15 min: INACEPTABLE, afecta el sistema
```

### Congestión (🚗)
```
🟢 < 40%: Flujo libre
🟡 40-60%: Moderado
🟠 60-80%: Alto
🔴 > 80%: SEVERO, sistema saturado
```

### Demanda Multiplicadora
```
Shown in "⏰ Hora Simulada" card

1.0x = Demanda base
3.0x = Hora pico (demanda triplicada)
0.2x = Madrugada (casi nadie)

Esta es la métrica base de todo lo que pasa
en el simulador.
```

---

## 🚀 COMANDOS PARA EJECUTAR

### Instalar dependencias
```bash
pip install streamlit plotly pandas numpy
```

### Ejecutar Simulador v2 (VERSIÓN MEJORADA)
```bash
streamlit run interactive_simulator_v2.py
```

### Ejecutar Simulador v1 (Original, más simple)
```bash
streamlit run interactive_simulator.py
```

---

## 🎓 LO QUE DEMUESTRA ESTE SIMULADOR

✅ **Sistemas Complejos**
- Interacción de múltiples variables
- Efectos cascada (un problema causa más problemas)

✅ **Realismo**
- Datos coherentes y lógicos
- Comportamientos observables en la vida real

✅ **Toma de Decisiones**
- Qué pasa si aumentas demanda
- Qué pasa si hay caos
- Cómo se recupera el sistema

✅ **Optimización**
- Identificar cuellos de botella
- Ver el impacto de mitigaciones
- Mejorar el sistema

---

## 🐛 TROUBLESHOOTING

### "ModuleNotFoundError: No module named 'fluctuations_engine'"
**Solución:** Los archivos `fluctuations_engine.py` e `interactive_simulator_v2.py` deben estar en la misma carpeta.

### Simulador muy lento
**Solución:** Aumenta "Velocidad de Simulación" a 5.0x o más en el sidebar.

### Los números no cambian
**Solución:** Asegúrate de presionar el botón ▶️ PLAY.

### Quiero números iniciales diferentes
**Solución:** Presiona 🔄 RESET para reiniciar todo.

---

## 📈 PRÓXIMAS MEJORAS FUTURAS

- [ ] Mapa interactivo 3D con ubicación real de buses
- [ ] Visualización de rutas geográficas
- [ ] Predicción de demanda con ML
- [ ] Optimización automática de rutas
- [ ] Sistema de alertas push
- [ ] Exportación a PDF de reportes
- [ ] Integración con datos GPS reales
- [ ] Sistema multiusuario

---

## 🎯 CONCLUSIÓN

Este simulador te permite **demostrar de manera interactiva**:
1. Cómo funciona un sistema de transporte urbano real
2. Cómo variables del entorno impactan el servicio
3. Cómo resolver problemas de congestión
4. La complejidad de la gestión de tráfico

¡Diviértete experimentando! 🎮
