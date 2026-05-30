@echo off
REM Script de setup para Windows

echo 🚀 AMCO - Setup Inicial
echo ========================

REM Crear entorno virtual
echo.
echo 📦 Creando entorno virtual...
python -m venv venv
call venv\Scripts\activate.bat

REM Instalar dependencias
echo.
echo 📚 Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Crear directorios necesarios
echo.
echo 📁 Creando directorios...
if not exist backend\app\ml\models mkdir backend\app\ml\models
if not exist logs mkdir logs
if not exist tests mkdir tests

REM Copiar archivos de configuración
echo.
echo ⚙️  Configurando...
copy .env.example .env

REM Inicializar base de datos
echo.
echo 🗄️  Inicializando base de datos...
python seed.py

echo.
echo ✅ Setup completado!
echo.
echo 📋 Próximos pasos:
echo 1. Abre 3 PowerShells diferentes
echo 2. Terminal 1: python iot_simulator.py
echo 3. Terminal 2: python api.py
echo 4. Terminal 3: streamlit run dashboard_avanzado.py
echo.
echo 🎉 ¡Listo para ejecutar!
pause
