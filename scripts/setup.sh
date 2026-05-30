#!/bin/bash

# Script de setup para Linux/Mac

echo "🚀 AMCO - Setup Inicial"
echo "========================\n"

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "\n📚 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear directorios necesarios
echo "\n📁 Creando directorios..."
mkdir -p backend/app/ml/models
mkdir -p logs
mkdir -p tests

# Copiar archivos de configuración
echo "\n⚙️  Configurando..."
cp .env.example .env

# Inicializar base de datos
echo "\n🗄️  Inicializando base de datos..."
python seed.py

echo "\n✅ Setup completado!"
echo "\n📋 Próximos pasos:"
echo "1. Abre 3 terminales diferentes"
echo "2. Terminal 1: python iot_simulator.py"
echo "3. Terminal 2: python api.py"
echo "4. Terminal 3: streamlit run dashboard_avanzado.py"
echo "\n🎉 ¡Listo para ejecutar!"
