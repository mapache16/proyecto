"""
🚌 EJECUTOR GRÁFICO - Sin Línea de Comandos
==============================================

Interfaz simple con botones para ejecutar el sistema.

Ejecución: python ejecutor_gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from mini_bus import SistemaBuses, Visor, Matematica, Parada, Bus

class EjecutorGUI:
    """Interfaz gráfica para ejecutar simulaciones"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🚌 SISTEMA DE TRANSPORTE - EJECUTOR")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        self.sistema = None
        self.visor = None
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea los elementos de la interfaz"""
        
        # Título
        titulo = tk.Label(
            self.root,
            text="🚌 SISTEMA COMPACTO DE TRANSPORTE",
            font=("Arial", 16, "bold"),
            bg='#f0f0f0'
        )
        titulo.pack(pady=15)
        
        # Frame de opciones
        frame_opciones = ttk.Frame(self.root)
        frame_opciones.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Opción 1: Crear sistema
        btn1 = tk.Button(
            frame_opciones,
            text="🐄 1. CREAR SISTEMA\n(Paradas + Buses)",
            font=("Arial", 11, "bold"),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=15,
            command=self.crear_sistema,
            relief='raised',
            bd=2
        )
        btn1.pack(pady=10, fill='x')
        
        # Opción 2: Simular
        btn2 = tk.Button(
            frame_opciones,
            text="🔄 2. EJECUTAR SIMULACIÓN\n(50 pasos)",
            font=("Arial", 11, "bold"),
            bg='#2196F3',
            fg='white',
            padx=20,
            pady=15,
            command=self.ejecutar_simulacion,
            relief='raised',
            bd=2
        )
        btn2.pack(pady=10, fill='x')
        
        # Opción 3: Ver gráficos
        btn3 = tk.Button(
            frame_opciones,
            text="📊 3. VER GRÁFICOS\n(Mapa, Ocupación, Congestión)",
            font=("Arial", 11, "bold"),
            bg='#FF9800',
            fg='white',
            padx=20,
            pady=15,
            command=self.ver_graficos,
            relief='raised',
            bd=2
        )
        btn3.pack(pady=10, fill='x')
        
        # Opción 4: Ver estadísticas
        btn4 = tk.Button(
            frame_opciones,
            text="📊 4. VER ESTADÍSTICAS\n(Datos en consola)",
            font=("Arial", 11, "bold"),
            bg='#9C27B0',
            fg='white',
            padx=20,
            pady=15,
            command=self.ver_estadisticas,
            relief='raised',
            bd=2
        )
        btn4.pack(pady=10, fill='x')
        
        # Opción 5: Todo automático
        btn5 = tk.Button(
            frame_opciones,
            text="⚡ 5. EJECUTAR TODO\n(1→2→3→4 automático)",
            font=("Arial", 11, "bold"),
            bg='#F44336',
            fg='white',
            padx=20,
            pady=15,
            command=self.ejecutar_todo,
            relief='raised',
            bd=2
        )
        btn5.pack(pady=10, fill='x')
        
        # Frame de estado
        frame_estado = ttk.LabelFrame(self.root, text="Estado", padding=10)
        frame_estado.pack(pady=10, padx=20, fill='x')
        
        self.etiqueta_estado = tk.Label(
            frame_estado,
            text="Estado: Sistema no inicializado",
            font=("Arial", 10),
            fg='#666'
        )
        self.etiqueta_estado.pack()
    
    def crear_sistema(self):
        """Crea el sistema de transporte"""
        try:
            self.sistema = SistemaBuses()
            
            # Paradas
            self.sistema.agregar_parada(1, "Centro", 4.8135, -75.6942)
            self.sistema.agregar_parada(2, "Sur", 4.8050, -75.6950)
            self.sistema.agregar_parada(3, "Norte", 4.8250, -75.6900)
            self.sistema.agregar_parada(4, "Este", 4.8100, -75.6850)
            
            # Buses
            self.sistema.agregar_bus(1, "Bus-001", [1, 2, 1])
            self.sistema.agregar_bus(2, "Bus-002", [1, 3, 4, 1])
            self.sistema.agregar_bus(3, "Bus-003", [2, 4, 3, 2])
            
            self.visor = Visor(self.sistema)
            
            self.etiqueta_estado.config(
                text=f"✅ Sistema creado: {len(self.sistema.paradas)} paradas, {len(self.sistema.buses)} buses",
                fg='#4CAF50'
            )
            messagebox.showinfo("Éxito", 
                f"✅ Sistema creado\n\n"
                f"{len(self.sistema.paradas)} paradas\n"
                f"{len(self.sistema.buses)} buses\n\n"
                f"Ahora ejecuta la simulación (paso 2)")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear sistema: {e}")
    
    def ejecutar_simulacion(self):
        """Ejecuta la simulación"""
        if not self.sistema:
            messagebox.showwarning("Advertencia", "Primero debes crear el sistema (paso 1)")
            return
        
        try:
            self.etiqueta_estado.config(text="⏳ Ejecutando simulación...", fg='#FF9800')
            self.root.update()
            
            self.sistema.simular(pasos=50)
            
            self.etiqueta_estado.config(
                text="✅ Simulación completada (50 pasos)",
                fg='#4CAF50'
            )
            messagebox.showinfo("Éxito", "✅ Simulación completada\n\nAhora puedes ver gráficos (paso 3)")
        except Exception as e:
            messagebox.showerror("Error", f"Error en simulación: {e}")
    
    def ver_graficos(self):
        """Muestra los gráficos"""
        if not self.sistema or not self.sistema.historial:
            messagebox.showwarning("Advertencia", 
                "Primero debes ejecutar la simulación (paso 2)")
            return
        
        try:
            self.etiqueta_estado.config(text="📊 Mostrando gráficos...", fg='#2196F3')
            self.root.update()
            self.visor.mostrar_todo()
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar gráficos: {e}")
    
    def ver_estadisticas(self):
        """Muestra estadísticas en consola"""
        if not self.sistema:
            messagebox.showwarning("Advertencia", "Primero debes crear el sistema (paso 1)")
            return
        
        try:
            self.visor.estadisticas()
            messagebox.showinfo("Éxito", 
                "✅ Estadísticas mostradas en consola\n\n"
                "Revisa la terminal/consola de Python")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
    
    def ejecutar_todo(self):
        """Ejecuta todos los pasos automáticamente"""
        try:
            self.etiqueta_estado.config(text="⚡ Ejecutando proceso completo...", fg='#F44336')
            self.root.update()
            
            # Paso 1
            self.crear_sistema()
            self.root.update()
            
            # Paso 2
            self.sistema.simular(pasos=50)
            self.root.update()
            
            # Paso 3
            self.visor.estadisticas()
            self.root.update()
            
            # Paso 4
            self.visor.mostrar_todo()
            
            self.etiqueta_estado.config(
                text="✅ Proceso completo finalizado",
                fg='#4CAF50'
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EjecutorGUI(root)
    root.mainloop()
