import streamlit as st
import subprocess
import os
import requests
import time
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import traceback
import logging
import json

def run():
    """Módulo de Despliegue - Streamlit Cloud y Configuración."""
    
    with st.container():
        st.title("☁️ Clase 1: Despliegue en Streamlit Cloud")
        st.markdown("""
        Aprende a desplegar tus aplicaciones de Streamlit en la nube de forma gratuita
        usando Streamlit Cloud, incluyendo mejores prácticas y configuración avanzada.
        """)
        
        # Pestañas del módulo
        tab1, tab2, tab3, tab4 = st.tabs([
            "🚀 Streamlit Cloud",
            "⚙️ Configuración",
            "🔐 Secretos y Variables",
            "📊 Monitoreo y Debug"
        ])
        
        with tab1:
            render_streamlit_cloud_setup()
        
        with tab2:
            render_configuracion_avanzada()
        
        with tab3:
            render_secretos_variables()
        
        with tab4:
            render_monitoreo_debug()

def render_streamlit_cloud_setup():
    """Renderiza la guía de setup para Streamlit Cloud."""
    st.subheader("🚀 Guía de Despliegue en Streamlit Cloud")
    
    # Checklist de requisitos
    st.markdown("### ✅ Checklist de Requisitos Previos")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Requisitos:**")
        requisitos = [
            ("Cuenta de GitHub", "github"),
            ("Repositorio público/privado", "repo"),
            ("Archivo requirements.txt", "req"),
            ("Aplicación Streamlit funcional", "app"),
            ("Cuenta Streamlit Cloud", "cloud")
        ]
        
        for req, key in requisitos:
            completado = st.checkbox(req, key=f"req_{key}")
            if not completado:
                st.warning(f"⚠️ Pendiente: {req}")
    
    with col2:
        st.markdown("**Estructura de Proyecto Recomendada:**")
        st.code("""
📁 mi-proyecto-streamlit/
├── 📄 app.py                 # Aplicación principal
├── 📄 requirements.txt       # Dependencias
├── 📄 README.md             # Documentación
├── 📁 .streamlit/           # Configuración
│   ├── config.toml          # Config general
│   └── secrets.toml         # Secretos (NO subir a git)
├── 📁 data/                 # Datos
├── 📁 assets/               # Imágenes, CSS, etc.
└── 📄 .gitignore           # Archivos a ignorar
        """, language="text")
    
    # Pasos de despliegue
    st.markdown("---")
    st.markdown("### 📋 Pasos para el Despliegue")
    
    pasos = [
        {
            "titulo": "1. Preparar el Repositorio",
            "descripcion": "Sube tu código a GitHub con la estructura correcta",
            "codigo": """# Comandos Git básicos
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/usuario/repo.git
git push -u origin main""",
            "tips": [
                "Asegúrate de que app.py esté en la raíz",
                "Incluye todas las dependencias en requirements.txt",
                "Agrega .streamlit/secrets.toml al .gitignore"
            ]
        },
        {
            "titulo": "2. Crear requirements.txt",
            "descripcion": "Lista todas las dependencias de tu proyecto",
            "codigo": """# Ejemplo de requirements.txt
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.24.0
plotly>=5.15.0
requests>=2.28.0

# Para generar automáticamente:
# pip freeze > requirements.txt""",
            "tips": [
                "Especifica versiones para evitar conflictos",
                "Incluye solo las librerías que realmente usas",
                "Prueba la instalación en un entorno limpio"
            ]
        },
        {
            "titulo": "3. Configurar Streamlit Cloud",
            "descripcion": "Conecta tu repositorio con Streamlit Cloud",
            "codigo": """# URL de Streamlit Cloud
https://share.streamlit.io/

# Pasos:
1. Inicia sesión con GitHub
2. Click en "New app"
3. Selecciona tu repositorio
4. Especifica la rama (main)
5. Archivo principal (app.py)
6. Click "Deploy!" """,
            "tips": [
                "El primer despliegue puede tomar 5-10 minutos",
                "Cada push a GitHub actualiza automáticamente",
                "Puedes ver logs en tiempo real"
            ]
        }
    ]
    
    for i, paso in enumerate(pasos):
        with st.expander(f"{paso['titulo']}", expanded=i==0):
            st.markdown(paso['descripcion'])
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.code(paso['codigo'], language="bash" if "git" in paso['codigo'] else "python")
            
            with col2:
                st.markdown("**💡 Tips:**")
                for tip in paso['tips']:
                    st.markdown(f"• {tip}")

def render_configuracion_avanzada():
    """Renderiza configuración avanzada de Streamlit."""
    st.subheader("⚙️ Configuración Avanzada")
    
    st.markdown("""
    Personaliza el comportamiento de tu aplicación con archivos de configuración.
    """)
    
    # Pestañas de configuración
    config_tab1, config_tab2, config_tab3 = st.tabs([
        "🔧 config.toml",
        "🎨 CSS Personalizado", 
        "📱 Responsive Design"
    ])
    
    with config_tab1:
        st.markdown("### 🔧 Archivo config.toml")
        st.markdown("Ubicación: `.streamlit/config.toml`")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Configuración Básica:**")
            st.code("""
[global]
# Configuración general
developmentMode = false
logLevel = "info"

[server]
# Configuración del servidor
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200
enableWebsocketCompression = true

[browser]
# Configuración del navegador
gatherUsageStats = false
serverAddress = "localhost"
serverPort = 8501

[theme]
# Tema de la aplicación
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
            """, language="toml")
        
        with col2:
            st.markdown("**Configuración de Performance:**")
            st.code("""
[global]
# Configuración de caché y performance
dataFrameSerialization = "arrow"
showWarningOnDirectExecution = false

[server]
# Optimización del servidor
maxMessageSize = 200
runOnSave = true
allowRunOnSave = true

# Configuración experimental
[experimental]
# Características experimentales
allowWidgetMutability = true
hideDataFrameControls = false
rerunOnConfigChange = true

[client]
# Configuración del cliente
caching = true
showErrorDetails = true
            """, language="toml")

def render_secretos_variables():
    """Renderiza la gestión de secretos y variables."""
    st.subheader("🔐 Gestión de Secretos y Variables de Entorno")
    
    st.markdown("""
    Aprende a manejar de forma segura API keys, tokens y otras credenciales.
    """)
    
    # Pestañas de secretos
    secret_tab1, secret_tab2, secret_tab3 = st.tabs([
        "🔑 secrets.toml",
        "🌍 Variables de Entorno",
        "🛡️ Mejores Prácticas"
    ])
    
    with secret_tab1:
        st.markdown("### 🔑 Archivo secrets.toml")
        st.markdown("Ubicación: `.streamlit/secrets.toml` (⚠️ NO subir a git)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Ejemplo de secrets.toml:**")
            st.code("""
# API Keys
openai_api_key = "sk-your-openai-key-here"
google_api_key = "your-google-api-key"
mapbox_token = "pk.your-mapbox-token"

# Database credentials
[database]
host = "localhost"
port = 5432
username = "myuser"
password = "mypassword"
database = "mydb"

# AWS credentials
[aws]
access_key_id = "AKIAIOSFODNN7EXAMPLE"
secret_access_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
region = "us-west-2"
            """, language="toml")
        
        with col2:
            st.markdown("**Cómo usar en código:**")
            st.code("""
import streamlit as st

# Acceder a secretos simples
api_key = st.secrets["openai_api_key"]

# Acceder a secciones
db_host = st.secrets["database"]["host"]
db_port = st.secrets["database"]["port"]

# Verificar si existe
if "openai_api_key" in st.secrets:
    api_key = st.secrets["openai_api_key"]
else:
    st.error("API key no encontrada")

# Múltiples secretos
aws_credentials = {
    "access_key": st.secrets["aws"]["access_key_id"],
    "secret_key": st.secrets["aws"]["secret_access_key"],
    "region": st.secrets["aws"]["region"]
}
            """, language="python")

def render_monitoreo_debug():
    """Renderiza herramientas de monitoreo y debug."""
    st.subheader("📊 Monitoreo y Debug")
    
    st.markdown("""
    Herramientas para monitorear el rendimiento y debuggear problemas en producción.
    """)
    
    # Pestañas de monitoreo
    monitor_tab1, monitor_tab2, monitor_tab3 = st.tabs([
        "🔍 Debug Tools",
        "📈 Performance",
        "🚨 Error Handling"
    ])
    
    with monitor_tab1:
        st.markdown("### 🔍 Herramientas de Debug")
        
        # Debug info actual
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Información de la Sesión:**")
            debug_info = {
                "Streamlit Version": st.__version__,
                "Session ID": st.session_state.get('session_id', 'N/A'),
                "Cache Status": "Enabled"
            }
            
            for key, value in debug_info.items():
                st.write(f"**{key}:** {value}")
        
        with col2:
            st.markdown("**Variables de Session State:**")
            if st.session_state:
                for key, value in st.session_state.items():
                    if not key.startswith('_'):  # Ocultar variables internas
                        st.write(f"**{key}:** {str(value)[:50]}...")
            else:
                st.write("No hay variables en session state")
        
        # Debug utilities
        st.markdown("---")
        st.markdown("### 🛠️ Utilidades de Debug")
        
        debug_util_col1, debug_util_col2 = st.columns(2)
        
        with debug_util_col1:
            if st.button("🔄 Limpiar Cache"):
                st.cache_data.clear()
                st.cache_resource.clear()
                st.success("✅ Cache limpiado")
            
            if st.button("📋 Mostrar Session State"):
                st.json(dict(st.session_state))
            
            if st.button("🧹 Limpiar Session State"):
                for key in list(st.session_state.keys()):
                    if not key.startswith('_'):
                        del st.session_state[key]
                st.success("✅ Session State limpiado")
                st.rerun()
        
        with debug_util_col2:
            # Simulador de errores para testing
            st.markdown("**Simulador de Errores:**")
            error_type = st.selectbox(
                "Tipo de error:",
                ["None", "ValueError", "KeyError", "ConnectionError", "TimeoutError"]
            )
            
            if st.button("🧨 Simular Error") and error_type != "None":
                try:
                    if error_type == "ValueError":
                        raise ValueError("Error simulado: Valor inválido")
                    elif error_type == "KeyError":
                        raise KeyError("Error simulado: Clave no encontrada")
                    elif error_type == "ConnectionError":
                        raise ConnectionError("Error simulado: Conexión fallida")
                    elif error_type == "TimeoutError":
                        raise TimeoutError("Error simulado: Timeout")
                except Exception as e:
                    st.exception(e)
    
    with monitor_tab2:
        st.markdown("### 📈 Monitoreo de Performance")
        
        # Métricas simuladas pero realistas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            load_time = random.uniform(0.8, 2.5)
            delta_load = random.uniform(-0.5, 0.3)
            st.metric("Tiempo de Carga", f"{load_time:.2f}s", delta=f"{delta_load:.2f}s")
        
        with col2:
            memory_usage = random.randint(35, 65)
            delta_memory = random.randint(-10, 15)
            st.metric("Uso de Memoria", f"{memory_usage}%", delta=f"{delta_memory}%")
        
        with col3:
            active_users = random.randint(15, 50)
            delta_users = random.randint(-5, 8)
            st.metric("Usuarios Activos", active_users, delta=delta_users)
        
        with col4:
            error_rate = random.uniform(0.1, 2.0)
            delta_error = random.uniform(-0.5, 0.3)
            st.metric("Tasa de Error", f"{error_rate:.1f}%", delta=f"{delta_error:.1f}%")
        
        # Ejemplo de código de monitoreo
        st.markdown("---")
        st.markdown("### 📊 Código de Monitoreo")
        
        st.code("""
import time
import psutil
import streamlit as st

class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()
    
    def get_metrics(self):
        return {
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'memory_percent': psutil.virtual_memory().percent,
            'uptime': time.time() - self.start_time
        }
    
    def display_metrics(self):
        metrics = self.get_metrics()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("CPU", f"{metrics['cpu_percent']:.1f}%")
        with col2:
            st.metric("Memoria", f"{metrics['memory_percent']:.1f}%")
        with col3:
            st.metric("Uptime", f"{metrics['uptime']:.0f}s")

# Uso
monitor = PerformanceMonitor()
monitor.display_metrics()
        """, language="python")
    
    with monitor_tab3:
        st.markdown("### 🚨 Manejo de Errores")
        
        st.markdown("**Ejemplo de Error Handling:**")
        
        st.code("""
import streamlit as st
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_operation():
    try:
        # Operación que puede fallar
        result = risky_function()
        logger.info("Operación exitosa")
        return result
        
    except ValueError as e:
        st.error(f"❌ Error de valor: {e}")
        logger.error(f"ValueError: {e}")
        
    except Exception as e:
        st.error(f"❌ Error inesperado: {e}")
        logger.exception("Error inesperado")
        
    return None

def main():
    st.title("Mi App")
    
    if st.button("Ejecutar Operación"):
        result = safe_operation()
        if result:
            st.success(f"✅ Resultado: {result}")
        """, language="python")
        
        # Demo de error handling
        st.markdown("---")
        st.markdown("### 🧪 Demo de Error Handling")
        
        if st.button("🚨 Simular Error de Demostración", key="demo_error"):
            try:
                raise ValueError("Este es un error de ejemplo para mostrar el manejo")
            except Exception as e:
                st.error(f"❌ Error capturado: {str(e)}")
                st.info("💡 En una app real, este error se registraría en logs")
        
        # Checklist de error handling
        st.markdown("---")
        st.markdown("### ✅ Checklist de Error Handling")
        
        error_checklist = [
            "Manejo de errores de conexión/timeout",
            "Validación de entrada de usuarios",
            "Manejo de archivos corruptos/inválidos",
            "Fallbacks para APIs que fallan",
            "Mensajes de error user-friendly",
            "Logging de errores para debug",
            "Graceful degradation de funciones",
            "Testing de casos edge"
        ]
        
        for i, item in enumerate(error_checklist):
            st.checkbox(item, key=f"error_check_{i}_{hash(item) % 10000}")

if __name__ == "__main__":
    run()
