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
            "descripcion": "Conecta tu repositorio con Streamlit Cloud",            "codigo": """# URL de Streamlit Cloud
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
    
    # Ejemplo de app simple para despliegue
    st.markdown("---")
    st.markdown("### 🎯 Ejemplo de App Lista para Despliegue")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**app.py:**")
        st.code("""
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Mi App",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Mi Primera App en la Nube")

# Datos de ejemplo
data = {
    'Mes': ['Ene', 'Feb', 'Mar', 'Abr'],
    'Ventas': [100, 150, 120, 180]
}
df = pd.DataFrame(data)

# Gráfico
fig = px.bar(df, x='Mes', y='Ventas')
st.plotly_chart(fig, use_container_width=True)

st.success("¡App desplegada exitosamente!")
        """, language="python")
    
    with col2:
        st.markdown("**requirements.txt:**")
        st.code("""
streamlit==1.46.0
pandas==2.0.3
plotly==5.15.0
        """, language="text")
        
        st.markdown("**.gitignore:**")
        st.code("""
__pycache__/
*.pyc
.env
.streamlit/secrets.toml
.DS_Store
*.log
        """, language="text")
    
    # Simulador de URL
    st.markdown("---")
    st.markdown("### 🌐 Simulador de URL de Despliegue")
    
    col1, col2 = st.columns(2)
    
    with col1:
        usuario_github = st.text_input("Usuario de GitHub", value="mi-usuario", key="sim_usuario")
        repo_nombre = st.text_input("Nombre del repositorio", value="mi-app-streamlit", key="sim_repo")
        rama = st.selectbox("Rama", ["main", "master", "develop"], key="sim_rama")
        archivo_principal = st.text_input("Archivo principal", value="app.py", key="sim_archivo")
    
    with col2:
        st.markdown("**URL resultante:**")
        url_generada = f"https://{usuario_github}-{repo_nombre}-{archivo_principal.replace('.py', '')}-{rama}.streamlit.app"
        st.code(url_generada, language="text")
        
        st.markdown("**URL alternativa (nueva):**")
        url_nueva = f"https://{repo_nombre.replace('-', '')}.streamlit.app"
        st.code(url_nueva, language="text")
        
        if st.button("🔗 Simular Visita"):
            st.info("✅ URL válida para Streamlit Cloud")
            st.balloons()

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
        st.markdown("###   🔧 Archivo config.toml")
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
            
            st.markdown("**💡 Explicación del Código:**")
            st.info("""
            **developmentMode**: Activa/desactiva el modo desarrollo
            **logLevel**: Nivel de logging (debug, info, warning, error)
            **maxUploadSize**: Tamaño máximo de archivos (MB)
            **primaryColor**: Color principal de la interfaz
            **enableCORS**: Permite peticiones cross-origin
            """)
        
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
            
            st.markdown("**🚀 Demo Interactiva de Configuración:**")
            
            # Demo interactiva
            demo_theme = st.selectbox(
                "Elige un tema:", 
                ["Claro", "Oscuro", "Personalizado"],
                key="demo_theme_select"
            )
            
            if demo_theme == "Personalizado":
                primary_color = st.color_picker("Color Primario", "#FF6B6B")
                bg_color = st.color_picker("Color de Fondo", "#FFFFFF")
                
                st.markdown(f"""
                **Config generado:**
                ```toml
                [theme]
                primaryColor = "{primary_color}"
                backgroundColor = "{bg_color}"
                secondaryBackgroundColor = "#F0F2F6"
                textColor = "#262730"
                ```
                """)
        
        # Sección adicional: Configuración por ambiente
        st.markdown("---")
        st.markdown("### 🌍 Configuración por Ambiente")
        
        env_tab1, env_tab2, env_tab3 = st.tabs(["🏠 Desarrollo", "🧪 Testing", "🚀 Producción"])
        
        with env_tab1:
            st.markdown("**config.toml para Desarrollo:**")
            st.code("""
[global]
developmentMode = true
logLevel = "debug"
showWarningOnDirectExecution = true

[server]
runOnSave = true
allowRunOnSave = true
port = 8501

[client]
showErrorDetails = true
caching = false  # Deshabilitar cache para desarrollo

# Hot reload más rápido
[experimental]
rerunOnConfigChange = true
            """, language="toml")
            
            st.markdown("**🔧 Script de desarrollo (`dev.py`):**")
            st.code("""
import streamlit as st
import os
import sys

# Configuración de desarrollo
if 'STREAMLIT_ENV' not in os.environ:
    os.environ['STREAMLIT_ENV'] = 'development'

# Auto-reload para archivos Python
if st.secrets.get("auto_reload", True):
    import importlib
    import sys
    
    # Recargar módulos automáticamente
    for module_name in list(sys.modules.keys()):
        if module_name.startswith('modulo_'):
            try:
                importlib.reload(sys.modules[module_name])
            except:
                pass

def development_utils():
    \"\"\"Utilidades solo para desarrollo.\"\"\"
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 Dev Utils")
    
    if st.sidebar.button("🔄 Clear All Cache"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("Cache cleared!")
    
    if st.sidebar.button("📊 Show Session State"):
        st.sidebar.json(dict(st.session_state))
    
    # Mostrar variables de entorno
    if st.sidebar.checkbox("Show Environment"):
        env_vars = {k: v for k, v in os.environ.items() 
                   if not k.startswith('_')}
        st.sidebar.json(env_vars)

# Usar en tu app principal
if os.environ.get('STREAMLIT_ENV') == 'development':
    development_utils()
            """, language="python")
        
        with env_tab2:
            st.markdown("**config.toml para Testing:**")
            st.code("""
[global]
developmentMode = false
logLevel = "warning"

[server]
runOnSave = false
port = 8502  # Puerto diferente

[client]
showErrorDetails = false
caching = true

# Configuración específica para tests
[testing]
timeout = 30
headless = true
            """, language="toml")
            
            st.markdown("**🧪 Framework de Testing (`test_app.py`):**")
            st.code("""
import streamlit as st
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class StreamlitTester:
    def __init__(self, app_url="http://localhost:8502"):
        self.app_url = app_url
        self.driver = None
    
    def setup(self):
        \"\"\"Configura el entorno de testing.\"\"\"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=options)
    
    def teardown(self):
        \"\"\"Limpia después de los tests.\"\"\"
        if self.driver:
            self.driver.quit()
    
    def test_app_loads(self):
        \"\"\"Test básico: la app carga correctamente.\"\"\"
        self.driver.get(self.app_url)
        time.sleep(3)  # Esperar a que cargue
        
        # Verificar que el título esté presente
        title = self.driver.find_element(By.TAG_NAME, "h1")
        assert title is not None
        
        # Verificar que no hay errores visibles
        error_elements = self.driver.find_elements(
            By.CLASS_NAME, "alert-error"
        )
        assert len(error_elements) == 0
    
    def test_widget_interactions(self):
        \"\"\"Test: interacciones con widgets.\"\"\"
        self.driver.get(self.app_url)
        time.sleep(2)
        
        # Buscar y hacer click en un botón
        button = self.driver.find_element(
            By.XPATH, "//button[contains(text(), 'Calcular')]"
        )
        button.click()
        time.sleep(1)
        
        # Verificar que aparece algún resultado
        results = self.driver.find_elements(
            By.CLASS_NAME, "metric-container"
        )
        assert len(results) > 0

# Ejecutar tests
if __name__ == "__main__":
    tester = StreamlitTester()
    tester.setup()
    try:
        tester.test_app_loads()
        tester.test_widget_interactions()
        print("✅ Todos los tests pasaron!")
    except Exception as e:
        print(f"❌ Test falló: {e}")
    finally:
        tester.teardown()
            """, language="python")
        
        with env_tab3:
            st.markdown("**config.toml para Producción:**")
            st.code("""
[global]
developmentMode = false
logLevel = "error"
showWarningOnDirectExecution = false

[server]
runOnSave = false
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 50  # Más restrictivo

[client]
showErrorDetails = false
caching = true
gatherUsageStats = true  # Para analytics

[theme]
# Tema optimizado para producción
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
            """, language="toml")
            
            st.markdown("**🚀 Optimizaciones de Producción (`prod.py`):**")
            st.code("""
import streamlit as st
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

# Configurar logging para producción
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/streamlit/app.log'),
        logging.StreamHandler()
    ]
)

# Configurar Sentry para error tracking
if 'sentry_dsn' in st.secrets:
    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR
    )
    sentry_sdk.init(
        dsn=st.secrets['sentry_dsn'],
        integrations=[sentry_logging]
    )

class ProductionOptimizer:
    @staticmethod
    @st.cache_data(ttl=3600)  # Cache por 1 hora
    def load_critical_data():
        \"\"\"Carga datos críticos con cache agresivo.\"\"\"
        # Tu lógica de carga de datos
        pass
    
    @staticmethod
    def setup_page_config():
        \"\"\"Configuración optimizada para producción.\"\"\"
        st.set_page_config(
            page_title="Mi App",
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="collapsed",  # Más espacio
            menu_items={
                'Get Help': 'https://mi-empresa.com/soporte',
                'Report a bug': 'https://mi-empresa.com/bugs',
                'About': "Mi App v1.0.0"
            }
        )
    
    @staticmethod
    def add_analytics():
        \"\"\"Agregar Google Analytics.\"\"\"
        ga_tracking_id = st.secrets.get('google_analytics_id')
        if ga_tracking_id:
            st.markdown(f'''
            <script async src="https://www.googletagmanager.com/gtag/js?id={ga_tracking_id}"></script>
            <script>
                window.dataLayer = window.dataLayer || [];
                function gtag(){{dataLayer.push(arguments);}}
                gtag('js', new Date());
                gtag('config', '{ga_tracking_id}');
            </script>
            ''', unsafe_allow_html=True)

# Usar en producción
if not st.secrets.get('debug_mode', False):
    ProductionOptimizer.setup_page_config()
    ProductionOptimizer.add_analytics()
            """, language="python")
    
    with config_tab2:
        st.markdown("### 🎨 CSS Personalizado")
        
        # Demostración de CSS personalizado
        st.markdown("**Ejemplo de CSS personalizado:**")
        
        css_example = """
/* Ocultar el menú de Streamlit */
#MainMenu {visibility: hidden;}

/* Ocultar el footer */
footer {visibility: hidden;}

/* Ocultar el header */
header {visibility: hidden;}

/* Personalizar el sidebar */
.css-1d391kg {
    background-color: #1E3A8A;
}

/* Personalizar métricas */
[data-testid="metric-container"] {
    background-color: #F0F8FF;
    border: 1px solid #E6F3FF;
    padding: 5% 5% 5% 10%;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Botones personalizados */
.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 20px;
    border: none;
    transition: all 0.3s;
}

.stButton > button:hover {
    background-color: #45a049;
    transform: translateY(-2px);
}
"""
        
        st.code(css_example, language="css")
        
        # Aplicar CSS de demostración
        if st.checkbox("🎨 Aplicar CSS de demostración", key="apply_demo_css"):
            st.markdown(f"<style>{css_example}</style>", unsafe_allow_html=True)
            st.success("✅ CSS aplicado! Observa los cambios en la interfaz.")
        
        st.markdown("**Cómo aplicar CSS:**")
        st.code("""
import streamlit as st

# Método 1: CSS inline
st.markdown('''
<style>
.custom-class {
    color: red;
    font-size: 20px;
}
</style>
''', unsafe_allow_html=True)

# Método 2: Archivo CSS externo
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('style.css')
        """, language="python")
    
    with config_tab3:
        st.markdown("### 📱 Responsive Design")
        
        st.markdown("""
        Haz que tu aplicación se vea bien en dispositivos móviles y tablets.
        """)
        
        # Demostración responsive
        device_type = st.selectbox(
            "🔍 Simular dispositivo:",
            ["Desktop", "Tablet", "Mobile"],
            key="device_simulator"
        )
        
        if device_type == "Desktop":
            cols = st.columns([1, 2, 1])
            with cols[1]:
                st.info("💻 Vista Desktop - Layout completo")
                
        elif device_type == "Tablet":
            cols = st.columns([0.2, 1, 0.2])
            with cols[1]:
                st.info("📱 Vista Tablet - Layout adaptado")
                
        else:  # Mobile
            st.info("📲 Vista Mobile - Layout compacto")
        
        st.markdown("**CSS Responsive:**")
        st.code("""
/* Media queries para responsive design */
@media (max-width: 768px) {
    /* Estilos para móviles */
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Ocultar sidebar en móviles */
    .css-1d391kg {
        display: none;
    }
    
    /* Ajustar tamaño de fuente */
    .stMarkdown h1 {
        font-size: 1.5rem;
    }
}

@media (max-width: 1024px) and (min-width: 769px) {
    /* Estilos para tablets */
    .main .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
    }
}
        """, language="css")
        
        st.markdown("**Tips para Responsive Design:**")
        tips_responsive = [
            "Usa `use_container_width=True` en gráficos",
            "Evita anchos fijos, usa columnas flexibles",
            "Prueba en diferentes tamaños de pantalla",
            "Considera la orientación del dispositivo",
            "Usa viewport meta tag si embebido",
            "Optimiza imágenes para diferentes resoluciones"
        ]
        
        for tip in tips_responsive:
            st.markdown(f"• {tip}")

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

# Social media
[social]
twitter_bearer_token = "your-twitter-token"
linkedin_client_id = "your-linkedin-id"
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
        
        # Simulador de secretos
        st.markdown("---")
        st.markdown("### 🧪 Simulador de Secretos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Configurar secreto de prueba:**")
            secret_name = st.text_input("Nombre del secreto", value="api_key")
            secret_value = st.text_input("Valor del secreto", value="demo-key-123", type="password")
            
            if st.button("💾 Simular Guardar"):
                st.session_state[f"secret_{secret_name}"] = secret_value
                st.success(f"✅ Secreto '{secret_name}' guardado")
        
        with col2:
            st.markdown("**Leer secreto:**")
            if st.button("🔍 Leer Secreto"):
                if f"secret_{secret_name}" in st.session_state:
                    value = st.session_state[f"secret_{secret_name}"]
                    st.success(f"🔑 Secreto encontrado: `{value}`")
                else:
                    st.error(f"❌ Secreto '{secret_name}' no encontrado")
    
    with secret_tab2:
        st.markdown("### 🌍 Variables de Entorno")
        
        st.markdown("**Configuración en Streamlit Cloud:**")
        st.image("https://via.placeholder.com/600x300/E8F5E8/4CAF50?text=Streamlit+Cloud+Secrets+Manager", 
                 caption="Panel de secretos en Streamlit Cloud")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**En desarrollo local:**")
            st.code("""
# .env file
OPENAI_API_KEY=sk-your-key-here
DATABASE_URL=postgresql://user:pass@localhost/db
DEBUG=True

# Cargar en Python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
debug = os.getenv("DEBUG", "False") == "True"
            """, language="python")
        
        with col2:
            st.markdown("**En Streamlit Cloud:**")
            st.code("""
# Se configuran en el dashboard web
# App settings -> Secrets

# Acceso en código:
import streamlit as st

api_key = st.secrets.get("OPENAI_API_KEY")
db_url = st.secrets.get("DATABASE_URL")

# Con fallback
debug = st.secrets.get("DEBUG", "False") == "True"
            """, language="python")
        
        # Ejemplo práctico
        st.markdown("---")
        st.markdown("### 🚀 Ejemplo Práctico: API Weather")
        
        with st.expander("Ver código completo", expanded=False):
            st.code("""
import streamlit as st
import requests

def get_weather(city, api_key):
    \"\"\"Obtiene datos del clima usando OpenWeatherMap API.\"\"\"
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error obteniendo datos: {e}")
        return None

def main():
    st.title("🌤️ App del Clima")
    
    # Verificar API key
    if "weather_api_key" not in st.secrets:
        st.error("❌ API key no configurada en secrets")
        st.info("Configura 'weather_api_key' en .streamlit/secrets.toml")
        return
    
    api_key = st.secrets["weather_api_key"]
    
    # Input de ciudad
    city = st.text_input("🏙️ Ciudad:", value="Santiago")
    
    if st.button("🔍 Obtener Clima"):
        if city:
            weather_data = get_weather(city, api_key)
            if weather_data:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Temperatura", f"{weather_data['main']['temp']}°C")
                with col2:
                    st.metric("Humedad", f"{weather_data['main']['humidity']}%")
                with col3:
                    st.metric("Presión", f"{weather_data['main']['pressure']} hPa")

if __name__ == "__main__":
    main()
            """, language="python")
    
    with secret_tab3:
        st.markdown("### 🛡️ Mejores Prácticas de Seguridad")
        
        practicas = [
            {
                "titulo": "❌ NO hagas esto",
                "items": [
                    "Hardcodear API keys en el código",
                    "Subir secrets.toml a git",
                    "Compartir credenciales en chat/email",
                    "Usar la misma key para dev y prod",
                    "Dejar logs con información sensible"
                ],
                "color": "red"
            },
            {
                "titulo": "✅ SÍ hagas esto",
                "items": [
                    "Usar secrets.toml para desarrollo",
                    "Configurar secretos en Streamlit Cloud",
                    "Rotar API keys regularmente",
                    "Usar diferentes keys por ambiente",
                    "Validar existencia de secretos antes de usar"
                ],
                "color": "green"
            }
        ]
        
        col1, col2 = st.columns(2)
        
        for i, practica in enumerate(practicas):
            with [col1, col2][i]:
                if practica["color"] == "red":
                    st.error(f"**{practica['titulo']}**")
                else:
                    st.success(f"**{practica['titulo']}**")
                
                for item in practica["items"]:
                    st.markdown(f"• {item}")
        
        st.markdown("---")
        st.markdown("### 🔒 Checklist de Seguridad")
        
        security_checklist = [
            "secrets.toml está en .gitignore",
            "No hay API keys hardcodeadas",
            "Secretos configurados en Streamlit Cloud",
            "Keys diferentes para dev/prod",
            "Validación de secretos en código",
            "Logs limpios (sin secretos)",            "Permisos mínimos necesarios",
            "Monitoreo de uso de APIs"
        ]
        
        for i, item in enumerate(security_checklist):
            checked = st.checkbox(item, key=f"security_check_{i}_{hash(item) % 10000}")
            if not checked:
                st.warning(f"⚠️ Pendiente: {item}")

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
                "User Agent": st.context.headers.get("user-agent", "N/A") if hasattr(st, 'context') else "N/A",
                "Cache Status": "Enabled"  # Simplificado para evitar errores de configuración
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
        
        # Logging example
        st.markdown("---")
        st.markdown("### 📝 Logging Personalizado")
        
        st.code("""
import logging
import streamlit as st

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    st.title("Mi App")
    
    try:
        # Tu código aquí
        logger.info("Usuario accedió a la página principal")
        
        # Ejemplo de operación        result = some_operation()
        logger.info(f"Operación exitosa: {result}")
        
    except Exception as e:
        logger.error(f"Error en aplicación: {str(e)}", exc_info=True)
        st.error("Ocurrió un error. Revisa los logs.")
        """, language="python")
    
    with monitor_tab2:
        st.markdown("### 📈 Monitoreo de Performance")
        
        st.markdown("**🔍 Sistema de Métricas en Tiempo Real:**")
        
        # Métricas simuladas pero realistas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Simular tiempo de carga con variación realista
            import random
            load_time = st.session_state.get('load_time', random.uniform(0.8, 2.5))
            delta_load = random.uniform(-0.5, 0.3)
            st.metric("Tiempo de Carga", f"{load_time:.2f}s", delta=f"{delta_load:.2f}s")
        
        with col2:
            # Simular memoria con fluctuación
            memory_usage = st.session_state.get('memory_usage', random.randint(35, 65))
            delta_memory = random.randint(-10, 15)
            st.metric("Uso de Memoria", f"{memory_usage}%", delta=f"{delta_memory}%")
        
        with col3:
            # Simular usuarios activos
            active_users = st.session_state.get('active_users', random.randint(15, 50))
            delta_users = random.randint(-5, 8)
            st.metric("Usuarios Activos", active_users, delta=delta_users)
        
        with col4:
            # Simular tasa de error
            error_rate = st.session_state.get('error_rate', random.uniform(0.1, 2.0))
            delta_error = random.uniform(-0.5, 0.3)
            st.metric("Tasa de Error", f"{error_rate:.1f}%", delta=f"{delta_error:.1f}%")
        
        # Sistema de monitoreo real
        st.markdown("---")
        st.markdown("### 🏗️ Implementación de Sistema de Monitoreo")
        
        monitoring_tab1, monitoring_tab2, monitoring_tab3 = st.tabs([
            "📊 Performance Monitor", "🚨 Error Tracking", "📈 Analytics Dashboard"
        ])
        
        with monitoring_tab1:
            st.markdown("**Sistema de Monitoreo de Performance (`monitor.py`):**")
            st.code("""
import time
import psutil
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import json

class PerformanceMonitor:
    def __init__(self):
        self.metrics_history = []
        self.start_time = time.time()
        
        # Inicializar métricas en session state
        if 'performance_metrics' not in st.session_state:
            st.session_state.performance_metrics = []
    
    def collect_metrics(self):
        \"\"\"Recolecta métricas del sistema en tiempo real.\"\"\"
        try:
            # Métricas del sistema
            process = psutil.Process()
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory_info = process.memory_info()
            memory_percent = process.memory_percent()
            
            # Métricas de Streamlit
            session_count = len(st.session_state)
            cache_size = self._get_cache_size()
              metrics = {
                'timestamp': datetime.now(),
                'cpu_percent': cpu_percent,
                'memory_mb': memory_info.rss / 1024 / 1024,
                'memory_percent': memory_percent,
                'session_count': session_count,
                'cache_size': cache_size,
                'uptime_seconds': time.time() - self.start_time
            }
            
            # Guardar en historial
            st.session_state.performance_metrics.append(metrics)
            
            # Mantener solo los últimos 100 registros
            if len(st.session_state.performance_metrics) > 100:
                st.session_state.performance_metrics = st.session_state.performance_metrics[-100:]
            
            return metrics
            
        except Exception as e:
            st.error(f"Error recolectando métricas: {e}")
            return None
    
    def _get_cache_size(self):
        \"\"\"Estima el tamaño del cache.\"\"\"
        try:
            # Esto es una estimación simplificada
            cache_info = st.cache_data.get_stats()
            return len(cache_info) if cache_info else 0
        except:
            return 0
    
    def render_dashboard(self):
        \"\"\"Renderiza dashboard de performance en tiempo real.\"\"\"
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico de performance en tiempo real
            if st.session_state.performance_metrics:
                df_metrics = pd.DataFrame(st.session_state.performance_metrics)
                
                # Gráfico de CPU y Memoria
                fig = px.line(df_metrics, x='timestamp', 
                             y=['cpu_percent', 'memory_percent'],
                             title='CPU y Memoria en Tiempo Real',
                             labels={'value': 'Porcentaje (%)', 'variable': 'Métrica'})
                st.plotly_chart(fig, use_container_width=True)
                
                # Gráfico de memoria absoluta
                fig_mem = px.area(df_metrics, x='timestamp', y='memory_mb',
                                 title='Uso de Memoria (MB)')
                st.plotly_chart(fig_mem, use_container_width=True)
        
        with col2:
            # Métricas actuales
            if st.button("🔄 Actualizar Métricas", key="refresh_metrics"):
                current_metrics = self.collect_metrics()
                if current_metrics:
                    st.metric("CPU", f"{current_metrics['cpu_percent']:.1f}%")
                    st.metric("Memoria", f"{current_metrics['memory_mb']:.1f} MB")
                    st.metric("Sesiones", current_metrics['session_count'])
                    st.metric("Uptime", f"{current_metrics['uptime_seconds']:.0f}s")
            
            # Alertas automáticas
            if st.session_state.performance_metrics:
                latest = st.session_state.performance_metrics[-1]
                
                if latest['cpu_percent'] > 80:
                    st.warning("⚠️ CPU alto!")
                if latest['memory_percent'] > 80:
                    st.warning("⚠️ Memoria alta!")
                if latest['memory_mb'] > 500:
                    st.error("🚨 Uso excesivo de memoria!")
    
    def export_metrics(self):
        \"\"\"Exporta métricas a CSV.\"\"\"
        if st.session_state.performance_metrics:
            df = pd.DataFrame(st.session_state.performance_metrics)
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar Métricas CSV",
                data=csv,
                file_name=f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

# Uso del monitor
monitor = PerformanceMonitor()

def main():
    st.title("📊 Dashboard de Performance")
    
    # Auto-recolectar métricas cada 30 segundos
    if 'last_metric_time' not in st.session_state:
        st.session_state.last_metric_time = time.time()
    
    if time.time() - st.session_state.last_metric_time > 30:
        monitor.collect_metrics()
        st.session_state.last_metric_time = time.time()
    
    # Renderizar dashboard
    monitor.render_dashboard()
    monitor.export_metrics()

if __name__ == "__main__":
    main()
            """, language="python")
        
        with monitoring_tab2:
            st.markdown("**Sistema de Error Tracking (`error_tracker.py`):**")
            st.code("""
import streamlit as st
import traceback
import logging
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

class ErrorTracker:
    def __init__(self):
        self.setup_logging()
        self.setup_sentry()
        
        # Inicializar error log en session state
        if 'error_log' not in st.session_state:
            st.session_state.error_log = []
    
    def setup_logging(self):
        \"\"\"Configura el sistema de logging.\"\"\"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('streamlit_errors.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_sentry(self):
        \"\"\"Configura Sentry para error tracking en producción.\"\"\"
        if 'sentry_dsn' in st.secrets:
            sentry_logging = LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR
            )
            sentry_sdk.init(
                dsn=st.secrets['sentry_dsn'],
                integrations=[sentry_logging],
                traces_sample_rate=1.0,
                environment=st.secrets.get('environment', 'development')
            )
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        \"\"\"Registra un error con contexto completo.\"\"\"
        try:
            # Crear hash único del error
            error_signature = self._create_error_signature(error)
            
            error_data = {
                'timestamp': datetime.now().isoformat(),
                'error_type': type(error).__name__,
                'error_message': str(error),
                'error_signature': error_signature,
                'traceback': traceback.format_exc(),
                'context': context or {},
                'session_state': dict(st.session_state),
                'user_agent': self._get_user_agent()
            }
            
            # Agregar al log local
            st.session_state.error_log.append(error_data)
            
            # Log en archivo
            self.logger.error(f"Error logged: {error_data['error_type']} - {error_data['error_message']}")
            
            # Enviar a Sentry si está configurado
            if 'sentry_dsn' in st.secrets:
                with sentry_sdk.configure_scope() as scope:
                    scope.set_context("streamlit_context", context or {})
                    scope.set_tag("error_signature", error_signature)
                    sentry_sdk.capture_exception(error)
            
            return error_signature
            
        except Exception as logging_error:
            self.logger.error(f"Error logging error: {logging_error}")
            return None
    
    def _create_error_signature(self, error: Exception) -> str:
        \"\"\"Crea una firma única para el error.\"\"\"
        signature_data = f"{type(error).__name__}:{str(error)}"
        return hashlib.md5(signature_data.encode()).hexdigest()[:8]
    
    def _get_user_agent(self) -> str:
        \"\"\"Obtiene el user agent del navegador.\"\"\"
        try:
            return st.context.headers.get("user-agent", "Unknown")
        except:
            return "Unknown"
    
    def render_error_dashboard(self):
        \"\"\"Renderiza dashboard de errores.\"\"\"
        st.markdown("### 🚨 Dashboard de Errores")
        
        if not st.session_state.error_log:
            st.success("✅ No hay errores registrados")
            return
        
        # Estadísticas generales
        col1, col2, col3, col4 = st.columns(4)
        
        error_count = len(st.session_state.error_log)
        unique_errors = len(set(e['error_signature'] for e in st.session_state.error_log))
        recent_errors = len([e for e in st.session_state.error_log 
                           if (datetime.now() - datetime.fromisoformat(e['timestamp'])).seconds < 3600])
        
        with col1:
            st.metric("Total Errores", error_count)
        with col2:
            st.metric("Errores Únicos", unique_errors)
        with col3:
            st.metric("Última Hora", recent_errors)
        with col4:
            error_rate = (recent_errors / max(1, error_count)) * 100
            st.metric("Tasa Error", f"{error_rate:.1f}%")
        
        # Lista de errores recientes
        st.markdown("---")
        st.markdown("### 📋 Errores Recientes")
        
        for i, error in enumerate(reversed(st.session_state.error_log[-10:])):
            with st.expander(f"🚨 {error['error_type']}: {error['error_message'][:50]}..."):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.code(error['traceback'], language="python")
                
                with col2:
                    st.write(f"**Timestamp:** {error['timestamp']}")
                    st.write(f"**Signature:** `{error['error_signature']}`")
                    st.write(f"**User Agent:** {error['user_agent'][:30]}...")
                    
                    if error['context']:
                        st.json(error['context'])
    
    def clear_error_log(self):
        \"\"\"Limpia el log de errores.\"\"\"
        st.session_state.error_log = []
        self.logger.info("Error log cleared")

# Decorador para manejo automático de errores
def handle_errors(error_tracker: ErrorTracker):
    \"\"\"Decorador para manejar errores automáticamente.\"\"\"
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_tracker.log_error(e, {
                    'function_name': func.__name__,
                    'args': str(args)[:100],
                    'kwargs': str(kwargs)[:100]
                })
                st.error(f"❌ Error en {func.__name__}: {str(e)}")
                raise
        return wrapper
    return decorator

# Ejemplo de uso
error_tracker = ErrorTracker()

@handle_errors(error_tracker)
def risky_operation(data):
    \"\"\"Operación que puede fallar.\"\"\"
    if not data:
        raise ValueError("Data cannot be empty")
    return len(data) * 2

def main():
    st.title("🚨 Error Tracking Demo")
    
    # Botones para simular errores
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧨 Simular ValueError"):
            try:
                risky_operation(None)
            except:
                pass
    
    with col2:
        if st.button("🔥 Simular KeyError"):
            try:
                data = {}
                result = data['nonexistent_key']
            except Exception as e:
                error_tracker.log_error(e, {'operation': 'key_access'})
    
    with col3:
        if st.button("🧹 Limpiar Log"):
            error_tracker.clear_error_log()
            st.success("✅ Log limpiado")
    
    # Mostrar dashboard
    error_tracker.render_error_dashboard()

if __name__ == "__main__":
    main()
            """, language="python")
            
            # Demo de error tracking
            st.markdown("---")
            st.markdown("### 🧪 Demo de Error Tracking")
            
            # Simulador de errores
            demo_col1, demo_col2 = st.columns(2)
            
            with demo_col1:
                if st.button("🚨 Simular Error ValueError", key="demo_error_1"):
                    try:
                        raise ValueError("Este es un error de ejemplo")
                    except Exception as e:
                        # Simular logging del error
                        error_info = {
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'type': type(e).__name__,
                            'message': str(e),
                            'stack_trace': traceback.format_exc()
                        }
                        st.error(f"❌ Error capturado: {error_info['type']}")
                        with st.expander("Ver detalles del error"):
                            st.json(error_info)
                
                if st.button("🔍 Simular Error KeyError", key="demo_error_2"):
                    try:
                        data = {'a': 1, 'b': 2}
                        result = data['key_inexistente']
                    except Exception as e:
                        st.error(f"❌ Error de clave: {str(e)}")
                        st.info("💡 Este error sería enviado automáticamente a Sentry")
            
            with demo_col2:
                st.markdown("**Error Tracking en Producción:**")
                st.info("""
                🔧 **Herramientas recomendadas:**
                • Sentry (error tracking)
                • LogRocket (session replay)
                • Datadog (APM)
                • New Relic (performance)
                
                📊 **Métricas importantes:**
                • Error rate (%)
                • Time to detect (TTD)
                • Time to resolve (TTR)
                • Error frequency
                """)
        
        with monitoring_tab3:
            st.markdown("**Sistema de Analytics (`analytics.py`):**")
            st.code("""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import uuid

class StreamlitAnalytics:
    def __init__(self):
        # Inicializar analytics en session state
        if 'analytics_data' not in st.session_state:
            st.session_state.analytics_data = []
        
        # Generar session ID único
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())[:8]
    
    def track_event(self, event_name: str, properties: dict = None):
        \"\"\"Registra un evento de analytics.\"\"\"
        event_data = {
            'timestamp': datetime.now(),
            'session_id': st.session_state.session_id,
            'event_name': event_name,
            'properties': properties or {},
            'page_url': self._get_current_page(),
            'user_agent': self._get_user_agent()
        }
        
        st.session_state.analytics_data.append(event_data)
        
        # Mantener solo los últimos 1000 eventos
        if len(st.session_state.analytics_data) > 1000:
            st.session_state.analytics_data = st.session_state.analytics_data[-1000:]
    
    def track_page_view(self, page_name: str):
        \"\"\"Registra una vista de página.\"\"\"
        self.track_event('page_view', {'page_name': page_name})
    
    def track_button_click(self, button_name: str):
        \"\"\"Registra un click de botón.\"\"\"
        self.track_event('button_click', {'button_name': button_name})
    
    def track_widget_interaction(self, widget_type: str, widget_key: str, value):
        \"\"\"Registra interacción con widget.\"\"\"
        self.track_event('widget_interaction', {
            'widget_type': widget_type,
            'widget_key': widget_key,
            'value': str(value)[:100]  # Limitar longitud
        })
    
    def _get_current_page(self):
        \"\"\"Obtiene la página actual.\"\"\"
        try:
            return st.session_state.get('current_page', 'home')
        except:
            return 'unknown'
    
    def _get_user_agent(self):
        \"\"\"Obtiene el user agent.\"\"\"
        try:
            return st.context.headers.get('user-agent', 'Unknown')[:100]
        except:
            return 'Unknown'
    
    def render_dashboard(self):
        \"\"\"Renderiza dashboard de analytics.\"\"\"
        st.markdown("### 📈 Analytics Dashboard")
        
        if not st.session_state.analytics_data:
            st.info("📊 No hay datos de analytics aún. Interactúa con la app para generar datos.")
            return
        
        # Convertir a DataFrame
        df = pd.DataFrame(st.session_state.analytics_data)
        df['date'] = df['timestamp'].dt.date
        df['hour'] = df['timestamp'].dt.hour
        
        # Métricas generales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_events = len(df)
            st.metric("Total Eventos", total_events)
        
        with col2:
            unique_sessions = df['session_id'].nunique()
            st.metric("Sesiones Únicas", unique_sessions)
        
        with col3:
            page_views = len(df[df['event_name'] == 'page_view'])
            st.metric("Vistas de Página", page_views)
        
        with col4:
            button_clicks = len(df[df['event_name'] == 'button_click'])
            st.metric("Clicks de Botón", button_clicks)
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Eventos por tipo
            event_counts = df['event_name'].value_counts()
            fig_events = px.pie(
                values=event_counts.values,
                names=event_counts.index,
                title="Distribución de Eventos"
            )
            st.plotly_chart(fig_events, use_container_width=True)
        
        with col2:
            # Actividad por hora
            hourly_activity = df.groupby('hour').size().reset_index(name='count')
            fig_hourly = px.bar(
                hourly_activity,
                x='hour',
                y='count',
                title="Actividad por Hora"
            )
            st.plotly_chart(fig_hourly, use_container_width=True)
        
        # Timeline de eventos
        st.markdown("---")
        st.markdown("### ⏱️ Timeline de Eventos")
        
        # Últimos 20 eventos
        recent_events = df.tail(20).sort_values('timestamp', ascending=False)
        
        for _, event in recent_events.iterrows():
            timestamp_str = event['timestamp'].strftime('%H:%M:%S')
            
            with st.expander(f"🕐 {timestamp_str} - {event['event_name'].title()}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Session ID:** {event['session_id']}")
                    st.write(f"**Página:** {event.get('page_url', 'N/A')}")
                
                with col2:
                    if event['properties']:
                        st.json(event['properties'])
                    else:
                        st.write("Sin propiedades adicionales")
    
    def export_analytics_data(self):
        \"\"\"Exporta datos de analytics.\"\"\"
        if st.session_state.analytics_data:
            df = pd.DataFrame(st.session_state.analytics_data)
            csv = df.to_csv(index=False)
            
            st.download_button(
                label="📥 Descargar Datos Analytics",
                data=csv,
                file_name=f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

# Decorador para tracking automático
def track_function_call(analytics: StreamlitAnalytics):
    \"\"\"Decorador para trackear llamadas a funciones.\"\"\"
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            
            try:
                result = func(*args, **kwargs)
                duration = (datetime.now() - start_time).total_seconds()
                
                analytics.track_event('function_call', {
                    'function_name': func.__name__,
                    'duration_seconds': duration,
                    'success': True
                })
                
                return result
                
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                
                analytics.track_event('function_call', {
                    'function_name': func.__name__,
                    'duration_seconds': duration,
                    'success': False,
                    'error': str(e)
                })
                
                raise
        
        return wrapper
    return decorator

# Ejemplo de uso
analytics = StreamlitAnalytics()

@track_function_call(analytics)
def calculate_something(x, y):
    \"\"\"Función de ejemplo que se trackea automáticamente.\"\"\"
    time.sleep(0.1)  # Simular procesamiento
    return x * y + 42

def main():
    st.title("📈 Analytics Demo")
    analytics.track_page_view('analytics_demo')
    
    # Widgets con tracking
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔢 Calcular", key="calc_button"):
            analytics.track_button_click('calculate')
            result = calculate_something(5, 10)
            st.success(f"Resultado: {result}")
        
        number_val = st.number_input("Número", value=0, key="number_input")
        if number_val != 0:
            analytics.track_widget_interaction('number_input', 'number_input', number_val)
    
    with col2:
        select_val = st.selectbox("Opciones", ["A", "B", "C"], key="select_widget")
        analytics.track_widget_interaction('selectbox', 'select_widget', select_val)
        
        if st.button("📊 Ver Analytics"):
            analytics.track_button_click('view_analytics')
    
    # Mostrar dashboard
    analytics.render_dashboard()
    analytics.export_analytics_data()

if __name__ == "__main__":
    main()
            """, language="python")
            
            # Demo interactivo de analytics
            st.markdown("---")
            st.markdown("### 🎯 Demo Interactivo de Analytics")
            
            # Simular tracking
            if 'demo_analytics' not in st.session_state:
                st.session_state.demo_analytics = []
            
            demo_col1, demo_col2 = st.columns(2)
            
            with demo_col1:
                if st.button("🎯 Trackear Evento", key="track_demo_event"):
                    event = {
                        'timestamp': datetime.now().strftime('%H:%M:%S'),
                        'event': 'button_click',
                        'user_id': f"user_{hash('demo') % 1000}",
                        'page': 'analytics_demo'
                    }
                    st.session_state.demo_analytics.append(event)
                    st.success("✅ Evento trackeado!")
                
                if st.button("📄 Trackear Page View", key="track_page_view"):
                    event = {
                        'timestamp': datetime.now().strftime('%H:%M:%S'),
                        'event': 'page_view',
                        'user_id': f"user_{hash('demo') % 1000}",
                        'page': 'dashboard'
                    }
                    st.session_state.demo_analytics.append(event)
                    st.success("✅ Page view trackeado!")
            
            with demo_col2:
                st.markdown("**Eventos Recientes:**")
                if st.session_state.demo_analytics:
                    for event in st.session_state.demo_analytics[-5:]:
                        st.text(f"{event['timestamp']} - {event['event']} ({event['page']})")
                else:
                    st.text("No hay eventos aún")
                
                if st.button("🧹 Limpiar", key="clear_analytics"):
                    st.session_state.demo_analytics = []
                    st.success("✅ Analytics limpiados!")
    
    with monitor_tab3:
        st.markdown("### 🚨 Manejo de Errores")
        
        # Error handling patterns
        st.markdown("**Patrones de Manejo de Errores:**")
        
        error_patterns_tab1, error_patterns_tab2, error_patterns_tab3 = st.tabs([
            "🔧 Try-Catch", "🛡️ Validaciones", "🔄 Retry Logic"
        ])
        
        with error_patterns_tab1:
            st.markdown("**Patrón Try-Catch Básico:**")
            st.code("""
import streamlit as st
import logging

def safe_operation(data):
    \"\"\"Operación con manejo seguro de errores.\"\"\"
    try:
        # Operación que puede fallar
        result = complex_calculation(data)
        return result
        
    except ValueError as e:
        st.error(f"❌ Error de valor: {e}")
        logging.error(f"ValueError in safe_operation: {e}")
        return None
        
    except KeyError as e:
        st.error(f"❌ Clave no encontrada: {e}")
        logging.error(f"KeyError in safe_operation: {e}")
        return None
        
    except Exception as e:
        st.error(f"❌ Error inesperado: {e}")
        logging.exception("Unexpected error in safe_operation")
        return None
    
    finally:
        # Limpieza que siempre se ejecuta
        cleanup_resources()

def main():
    st.title("🛡️ Error Handling Demo")
    
    user_input = st.text_input("Ingresa datos:")
    
    if st.button("🚀 Procesar"):
        if not user_input:
            st.warning("⚠️ Por favor ingresa algunos datos")
            return
        
        with st.spinner("Procesando..."):
            result = safe_operation(user_input)
            
            if result is not None:
                st.success(f"✅ Resultado: {result}")
            else:
                st.info("ℹ️ No se pudo procesar. Revisa los logs.")
            """, language="python")
        
        with error_patterns_tab2:
            st.markdown("**Sistema de Validaciones:**")
            st.code("""
import streamlit as st
from typing import Union, List
import re

class Validator:
    @staticmethod
    def validate_email(email: str) -> bool:
        \"\"\"Valida formato de email.\"\"\"
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        \"\"\"Valida formato de teléfono.\"\"\"
        pattern = r'^\+?[1-9]\d{1,14}$'
        return re.match(pattern, phone.replace(' ', '').replace('-', '')) is not None
    
    @staticmethod
    def validate_number_range(value: float, min_val: float, max_val: float) -> bool:
        \"\"\"Valida que un número esté en un rango.\"\"\"
        return min_val <= value <= max_val
    
    @staticmethod
    def validate_required_fields(data: dict, required_fields: List[str]) -> List[str]:
        \"\"\"Valida campos requeridos.\"\"\"
        missing_fields = []
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        return missing_fields

def create_user_form():
    \"\"\"Formulario con validaciones en tiempo real.\"\"\"
    st.markdown("### 📝 Formulario con Validaciones")
    
    with st.form("user_form"):
        # Campos del formulario
        name = st.text_input("Nombre *")
        email = st.text_input("Email *")
        phone = st.text_input("Teléfono")
        age = st.number_input("Edad", min_value=0, max_value=120, value=25)
        
        submitted = st.form_submit_button("✅ Validar y Enviar")
        
        if submitted:
            # Validar campos requeridos
            data = {'name': name, 'email': email}
            missing = Validator.validate_required_fields(
                data, ['name', 'email']
            )
            
            if missing:
                st.error(f"❌ Campos requeridos faltantes: {', '.join(missing)}")
                return
            
            # Validar email
            if not Validator.validate_email(email):
                st.error("❌ Formato de email inválido")
                return
            
            # Validar teléfono (si se proporciona)
            if phone and not Validator.validate_phone(phone):
                st.error("❌ Formato de teléfono inválido")
                return
            
            # Validar edad
            if not Validator.validate_number_range(age, 0, 120):
                st.error("❌ Edad debe estar entre 0 y 120 años")
                return
            
            # Si todo está bien
            st.success("✅ Formulario válido!")
            st.balloons()
            
            # Mostrar datos validados
            validated_data = {
                'name': name,
                'email': email,
                'phone': phone or 'No proporcionado',
                'age': age
            }
            st.json(validated_data)

# Uso del validador
create_user_form()
            """, language="python")        
        with error_patterns_tab3:
            st.markdown("**Sistema de Retry con Backoff:**")
            st.code("""
import streamlit as st
import time
import random
from functools import wraps
import logging

class RetryHandler:
    @staticmethod
    def exponential_backoff(max_retries=3, base_delay=1, max_delay=60):
        \"\"\"Decorador con retry y exponential backoff.\"\"\"
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                
                for attempt in range(max_retries + 1):
                    try:
                        return func(*args, **kwargs)
                    
                    except Exception as e:
                        last_exception = e
                        
                        if attempt == max_retries:
                            # Último intento fallido
                            logging.error(f"Function {func.__name__} failed after {max_retries} retries: {e}")
                            raise e
                        
                        # Calcular delay con jitter
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        jitter = random.uniform(0.1, 0.5)
                        actual_delay = delay + jitter
                        
                        logging.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {actual_delay:.2f}s")
                        time.sleep(actual_delay)
                
                raise last_exception
            
            return wrapper
        return decorator
    
    @staticmethod
    def with_circuit_breaker(failure_threshold=5, recovery_timeout=60):
        \"\"\"Implementa patrón Circuit Breaker.\"\"\"
        def decorator(func):
            func._failures = 0
            func._last_failure_time = 0
            func._state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                now = time.time()
                
                # Si el circuito está abierto, verificar si es tiempo de probar
                if func._state == 'OPEN':
                    if now - func._last_failure_time < recovery_timeout:
                        raise Exception("Circuit breaker is OPEN")
                    else:
                        func._state = 'HALF_OPEN'
                
                try:
                    result = func(*args, **kwargs)
                    
                    # Éxito: resetear contador de fallos
                    if func._state == 'HALF_OPEN':
                        func._state = 'CLOSED'
                    func._failures = 0
                    
                    return result
                
                except Exception as e:
                    func._failures += 1
                    func._last_failure_time = now
                    
                    # Si excedemos el threshold, abrir el circuito
                    if func._failures >= failure_threshold:
                        func._state = 'OPEN'
                        logging.error(f"Circuit breaker OPENED for {func.__name__}")
                    
                    raise e
            
            return wrapper
        return decorator

# Ejemplos de uso
@RetryHandler.exponential_backoff(max_retries=3, base_delay=1)
def fetch_data_from_api(url):
    \"\"\"Función que puede fallar y necesita retry.\"\"\"
    response = requests.get(url, timeout=5)
    
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")
    
    return response.json()

@RetryHandler.with_circuit_breaker(failure_threshold=3)
def unreliable_service():
    \"\"\"Servicio poco confiable con circuit breaker.\"\"\"
    if random.random() < 0.7:  # 70% de probabilidad de fallo
        raise Exception("Service temporarily unavailable")
    
    return {"status": "success", "data": "important data"}

def demo_retry_system():
    \"\"\"Demo del sistema de retry.\"\"\"
    st.title("🔄 Demo Sistema de Retry")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Exponential Backoff")
        
        if st.button("🌐 Test API Call", key="test_api"):
            try:
                with st.spinner("Intentando llamada API..."):
                    # Simular API call
                    result = fetch_data_from_api("https://httpstat.us/500")
                    st.success(f"✅ API Success: {result}")
            except Exception as e:
                st.error(f"❌ API Failed: {e}")
        
        if st.button("📊 Fetch Analytics", key="test_analytics"):
            try:
                with st.spinner("Obteniendo analytics..."):
                    # Simular fallo intermitente
                    if random.random() < 0.5:
                        raise Exception("Analytics service timeout")
                    st.success("✅ Analytics data loaded")
            except Exception as e:
                st.error(f"❌ Analytics failed: {e}")
    
    with col2:
        st.markdown("### Circuit Breaker")
        
        if st.button("⚡ Test Service", key="test_service"):
            try:
                result = unreliable_service()
                st.success(f"✅ Service OK: {result['status']}")
            except Exception as e:
                st.error(f"❌ Service Error: {e}")
        
        # Mostrar estado del circuit breaker
        if hasattr(unreliable_service, '_state'):
            state = unreliable_service._state
            failures = unreliable_service._failures
            
            if state == 'CLOSED':
                st.success(f"🟢 Circuit: {state} (Failures: {failures})")
            elif state == 'HALF_OPEN':
                st.warning(f"🟡 Circuit: {state} (Testing...)")
            else:
                st.error(f"🔴 Circuit: {state} (Failures: {failures})")

if __name__ == "__main__":
    demo_retry_system()
            """, language="python")
        try:
            # Esta es una estimación, el cache real es interno
            return len(str(st.session_state)) / 1024 / 1024
        except:
            return 0
    
    def display_real_time_metrics(self):
        \"\"\"Muestra métricas en tiempo real.\"\"\"
        current_metrics = self.collect_metrics()
        
        if current_metrics:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "CPU Usage", 
                    f"{current_metrics['cpu_percent']:.1f}%",
                    delta=None
                )
            
            with col2:
                st.metric(
                    "Memory", 
                    f"{current_metrics['memory_mb']:.1f} MB",
                    delta=f"{current_metrics['memory_percent']:.1f}%"
                )
            
            with col3:
                st.metric(
                    "Session State", 
                    current_metrics['session_state_size'],
                    delta=None
                )
            
            with col4:
                st.metric(
                    "Cache Size", 
                    f"{current_metrics['cache_size_mb']:.2f} MB",
                    delta=None
                )
    
    def display_performance_charts(self):
        \"\"\"Muestra gráficos de performance histórica.\"\"\"
        if len(st.session_state.performance_metrics) < 2:
            st.info("Recolectando datos... Refresca la página para ver más métricas")
            return
        
        # Convertir a DataFrame
        df = pd.DataFrame(st.session_state.performance_metrics)
        
        # Gráfico de CPU y Memoria
        col1, col2 = st.columns(2)
        
        with col1:
            fig_cpu = px.line(
                df, x='timestamp', y='cpu_percent',
                title='CPU Usage Over Time',
                labels={'cpu_percent': 'CPU %', 'timestamp': 'Time'}
            )
            fig_cpu.update_layout(height=300)
            st.plotly_chart(fig_cpu, use_container_width=True)
        
        with col2:
            fig_memory = px.line(
                df, x='timestamp', y='memory_mb',
                title='Memory Usage Over Time',
                labels={'memory_mb': 'Memory (MB)', 'timestamp': 'Time'}
            )
            fig_memory.update_layout(height=300)
            st.plotly_chart(fig_memory, use_container_width=True)

# Uso del monitor
monitor = PerformanceMonitor()

def main():
    st.title("📊 Dashboard de Performance")
    
    # Auto-refresh cada 5 segundos
    if st.button("🔄 Refresh Metrics"):
        st.rerun()
    
    # Mostrar métricas en tiempo real
    monitor.display_real_time_metrics()
    
    st.markdown("---")
    
    # Mostrar gráficos históricos
    monitor.display_performance_charts()
    
    # Botón para limpiar historial
    if st.button("🧹 Clear Metrics History"):
        st.session_state.performance_metrics = []
        st.success("Historial limpiado!")
        st.rerun()

if __name__ == "__main__":
    main()
            """, language="python")
            
            st.markdown("**💡 Explicación del Código:**")
            st.info("""
            **psutil**: Librería para obtener métricas del sistema (CPU, memoria)
            **session_state**: Almacena el historial de métricas entre ejecuciones
            **plotly**: Crea gráficos interactivos de las métricas en tiempo real
            **datetime**: Maneja timestamps para el historial
            **auto-refresh**: Actualiza métricas automáticamente
            """)
        
        with monitoring_tab2:
            st.markdown("**Sistema de Error Tracking (`error_tracker.py`):**")
            st.code("""
import streamlit as st
import traceback
import logging
from datetime import datetime
import json
import smtplib
from email.mime.text import MimeText

class ErrorTracker:
    def __init__(self):
        # Configurar logging
        self.logger = self._setup_logger()
        
        # Inicializar error storage
        if 'error_log' not in st.session_state:
            st.session_state.error_log = []
    
    def _setup_logger(self):
        \"\"\"Configura el sistema de logging.\"\"\"
        logger = logging.getLogger('streamlit_app')
        logger.setLevel(logging.ERROR)
        
        # Handler para archivo
        file_handler = logging.FileHandler('app_errors.log')
        file_handler.setLevel(logging.ERROR)
        
        # Formato detallado
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def log_error(self, error, context="Unknown", user_action="Unknown"):
        \"\"\"Registra un error con contexto completo.\"\"\"
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'user_action': user_action,
            'stack_trace': traceback.format_exc(),
            'session_id': st.session_state.get('session_id', 'unknown'),
            'user_agent': self._get_user_agent()
        }
        
        # Agregar al log en memoria
        st.session_state.error_log.append(error_info)
        
        # Log a archivo
        self.logger.error(
            f"Error in {context}: {str(error)}", 
            extra=error_info
        )
        
        # Enviar alerta si es crítico
        if self._is_critical_error(error):
            self._send_alert(error_info)
        
        return error_info
    
    def _get_user_agent(self):
        \"\"\"Obtiene información del navegador del usuario.\"\"\"
        try:
            if hasattr(st, 'context') and hasattr(st.context, 'headers'):
                return st.context.headers.get('user-agent', 'Unknown')
        except:
            pass
        return 'Unknown'
    
    def _is_critical_error(self, error):
        \"\"\"Determina si un error es crítico.\"\"\"
        critical_errors = [
            ConnectionError,
            TimeoutError,
            MemoryError,
            KeyError  # Para datos faltantes críticos
        ]
        return any(isinstance(error, err_type) for err_type in critical_errors)
    
    def _send_alert(self, error_info):
        \"\"\"Envía alerta por email para errores críticos.\"\"\"
        try:
            if 'alert_email' in st.secrets:
                msg = MimeText(
                    f"Error crítico en la aplicación:\\n\\n"
                    f"Tipo: {error_info['error_type']}\\n"
                    f"Mensaje: {error_info['error_message']}\\n"
                    f"Contexto: {error_info['context']}\\n"
                    f"Timestamp: {error_info['timestamp']}"
                )
                msg['Subject'] = "🚨 Error Crítico en Streamlit App"
                msg['From'] = st.secrets['smtp_from']
                msg['To'] = st.secrets['alert_email']
                
                # Enviar email (configurar SMTP según tu proveedor)
                # with smtplib.SMTP(st.secrets['smtp_server']) as server:
                #     server.send_message(msg)
                
                st.error("🚨 Error crítico detectado. Administrador notificado.")
        except Exception as e:
            st.error(f"Error enviando alerta: {e}")
    
    def display_error_dashboard(self):
        \"\"\"Muestra dashboard de errores.\"\"\"
        st.markdown("### 🚨 Dashboard de Errores")
        
        if not st.session_state.error_log:
            st.success("✅ No hay errores registrados")
            return
        
        # Resumen de errores
        col1, col2, col3 = st.columns(3)
        
        total_errors = len(st.session_state.error_log)
        recent_errors = len([
            e for e in st.session_state.error_log
            if (datetime.now() - datetime.fromisoformat(e['timestamp'])).seconds < 3600
        ])
        
        error_types = {}
        for error in st.session_state.error_log:
            error_type = error['error_type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        with col1:
            st.metric("Total Errores", total_errors)
        with col2:
            st.metric("Última Hora", recent_errors)
        with col3:
            most_common = max(error_types.items(), key=lambda x: x[1])
            st.metric("Más Común", f"{most_common[0]} ({most_common[1]})")
        
        # Lista de errores recientes
        st.markdown("#### 📋 Errores Recientes")
        for i, error in enumerate(reversed(st.session_state.error_log[-10:])):
            with st.expander(
                f"❌ {error['error_type']} - {error['timestamp'][:19]}", 
                expanded=i==0
            ):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Contexto:** {error['context']}")
                    st.write(f"**Acción:** {error['user_action']}")
                    st.write(f"**Session ID:** {error['session_id']}")
                with col2:
                    st.write(f"**Mensaje:** {error['error_message']}")
                    st.code(error['stack_trace'], language="python")

# Context manager para captura automática de errores
class ErrorCatcher:
    def __init__(self, tracker, context, user_action="General"):
        self.tracker = tracker
        self.context = context
        self.user_action = user_action
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.tracker.log_error(exc_val, self.context, self.user_action)
            
            # Mostrar error amigable al usuario
            st.error(f"❌ Error en {self.context}: {str(exc_val)}")
            
            # En desarrollo, mostrar detalles
            if st.secrets.get('debug_mode', False):
                st.exception(exc_val)
            
            return True  # Suprimir el error

# Uso del error tracker
error_tracker = ErrorTracker()

def example_usage():
    st.title("🔍 Error Tracking Demo")
    
    # Uso básico
    with ErrorCatcher(error_tracker, "Data Loading", "User clicked load button"):
        # Tu código que puede fallar
        data = load_data_from_api()
        st.dataframe(data)
    
    # Mostrar dashboard de errores
    if st.checkbox("Mostrar Error Dashboard"):
        error_tracker.display_error_dashboard()
    
    # Simular errores para testing
    st.markdown("### 🧪 Simulador de Errores")
    if st.button("Simular Error de Conexión"):
        with ErrorCatcher(error_tracker, "API Connection", "Test button clicked"):
            raise ConnectionError("No se pudo conectar a la API")
    
    if st.button("Simular Error de Datos"):
        with ErrorCatcher(error_tracker, "Data Processing", "Process button clicked"):
            raise ValueError("Datos inválidos recibidos")
            """, language="python")
            
            st.markdown("**🛠️ Características del Error Tracker:**")
            features = [
                "📝 **Logging detallado**: Captura stack trace completo y contexto",
                "📧 **Alertas automáticas**: Notifica errores críticos por email",
                "📊 **Dashboard visual**: Muestra estadísticas y tendencias de errores",
                "🔍 **Context manager**: Captura errores automáticamente con contexto",
                "💾 **Persistencia**: Guarda errores en archivo y session state",
                "🎯 **Clasificación**: Distingue entre errores críticos y normales"
            ]
            
            for feature in features:
                st.markdown(f"• {feature}")
        
        with monitoring_tab3:
            st.markdown("**Analytics Dashboard (`analytics.py`):**")
            st.code("""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

class AnalyticsDashboard:
    def __init__(self):
        # Inicializar datos de analytics
        if 'analytics_data' not in st.session_state:
            st.session_state.analytics_data = {
                'page_views': [],
                'user_interactions': [],
                'feature_usage': {},
                'performance_metrics': []
            }
    
    def track_page_view(self, page_name):
        \"\"\"Registra una vista de página.\"\"\"
        st.session_state.analytics_data['page_views'].append({
            'timestamp': datetime.now(),
            'page': page_name,
            'session_id': st.session_state.get('session_id', 'anonymous')
        })
    
    def track_interaction(self, element_type, element_id, action):
        \"\"\"Registra una interacción del usuario.\"\"\"
        st.session_state.analytics_data['user_interactions'].append({
            'timestamp': datetime.now(),
            'element_type': element_type,
            'element_id': element_id,
            'action': action,
            'session_id': st.session_state.get('session_id', 'anonymous')
        })
    
    def track_feature_usage(self, feature_name):
        \"\"\"Registra el uso de una característica.\"\"\"
        if feature_name not in st.session_state.analytics_data['feature_usage']:
            st.session_state.analytics_data['feature_usage'][feature_name] = 0
        st.session_state.analytics_data['feature_usage'][feature_name] += 1
    
    def display_analytics_dashboard(self):
        \"\"\"Muestra el dashboard completo de analytics.\"\"\"
        st.markdown("### 📈 Analytics Dashboard")
        
        # KPIs principales
        self._display_kpis()
        
        st.markdown("---")
        
        # Gráficos detallados
        chart_tab1, chart_tab2, chart_tab3 = st.tabs([
            "📊 Usage Overview", "🎯 Feature Analytics", "⏱️ Time Series"
        ])
        
        with chart_tab1:
            self._display_usage_overview()
        
        with chart_tab2:
            self._display_feature_analytics()
        
        with chart_tab3:
            self._display_time_series()
    
    def _display_kpis(self):
        \"\"\"Muestra KPIs principales.\"\"\"
        col1, col2, col3, col4 = st.columns(4)
        
        # Total page views
        total_views = len(st.session_state.analytics_data['page_views'])
        
        # Unique sessions
        unique_sessions = len(set([
            view['session_id'] for view 
            in st.session_state.analytics_data['page_views']
        ]))
        
        # Total interactions
        total_interactions = len(st.session_state.analytics_data['user_interactions'])
        
        # Most used feature
        feature_usage = st.session_state.analytics_data['feature_usage']
        most_used_feature = max(feature_usage.items(), key=lambda x: x[1]) if feature_usage else ("None", 0)
        
        with col1:
            st.metric("Total Views", total_views)
        with col2:
            st.metric("Unique Sessions", unique_sessions)
        with col3:
            st.metric("Interactions", total_interactions)
        with col4:
            st.metric("Top Feature", f"{most_used_feature[0]} ({most_used_feature[1]})")
    
    def _display_usage_overview(self):
        \"\"\"Muestra overview de uso.\"\"\"
        # Page views por página
        if st.session_state.analytics_data['page_views']:
            df_views = pd.DataFrame(st.session_state.analytics_data['page_views'])
            page_counts = df_views['page'].value_counts()
            
            fig_pages = px.bar(
                x=page_counts.index,
                y=page_counts.values,
                title="Page Views por Página",
                labels={'x': 'Página', 'y': 'Views'}
            )
            st.plotly_chart(fig_pages, use_container_width=True)
        
        # Tipos de interacciones
        if st.session_state.analytics_data['user_interactions']:
            df_interactions = pd.DataFrame(st.session_state.analytics_data['user_interactions'])
            interaction_counts = df_interactions['element_type'].value_counts()
            
            fig_interactions = px.pie(
                values=interaction_counts.values,
                names=interaction_counts.index,
                title="Distribución de Interacciones"
            )
            st.plotly_chart(fig_interactions, use_container_width=True)
    
    def _display_feature_analytics(self):
        \"\"\"Muestra analytics de características.\"\"\"
        feature_usage = st.session_state.analytics_data['feature_usage']
        
        if feature_usage:
            # Gráfico de barras de uso de características
            fig_features = px.bar(
                x=list(feature_usage.keys()),
                y=list(feature_usage.values()),
                title="Uso de Características",
                labels={'x': 'Característica', 'y': 'Usos'}
            )
            fig_features.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig_features, use_container_width=True)
            
            # Tabla detallada
            st.markdown("#### 📋 Detalle de Uso de Características")
            df_features = pd.DataFrame([
                {'Característica': k, 'Usos': v, 'Porcentaje': f"{v/sum(feature_usage.values())*100:.1f}%"}
                for k, v in sorted(feature_usage.items(), key=lambda x: x[1], reverse=True)
            ])
            st.dataframe(df_features, use_container_width=True)
        else:
            st.info("No hay datos de uso de características aún")
    
    def _display_time_series(self):
        \"\"\"Muestra series temporales.\"\"\"
        if st.session_state.analytics_data['page_views']:
            df_views = pd.DataFrame(st.session_state.analytics_data['page_views'])
            df_views['hour'] = df_views['timestamp'].dt.hour
            
            # Views por hora
            hourly_views = df_views.groupby('hour').size()
            
            fig_hourly = px.line(
                x=hourly_views.index,
                y=hourly_views.values,
                title="Page Views por Hora",
                labels={'x': 'Hora del Día', 'y': 'Views'}
            )
            st.plotly_chart(fig_hourly, use_container_width=True)
            
            # Heatmap de actividad (simulado)
            activity_data = []
            for hour in range(24):
                for day in range(7):
                    activity_data.append({
                        'hour': hour,
                        'day': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'][day],
                        'activity': len([v for v in df_views.to_dict('records') 
                                       if v['timestamp'].hour == hour]) + day * 2
                    })
            
            df_heatmap = pd.DataFrame(activity_data)
            fig_heatmap = px.density_heatmap(
                df_heatmap, x='hour', y='day', z='activity',
                title="Heatmap de Actividad (Hora vs Día)"
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)

# Decorador para tracking automático
def track_usage(feature_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            analytics.track_feature_usage(feature_name)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Instancia global de analytics
analytics = AnalyticsDashboard()

# Ejemplo de uso
@track_usage("data_visualization")
def create_chart():
    # Tu función de creación de gráficos
    analytics.track_interaction("button", "create_chart", "click")
    return "Chart created"

def main():
    st.title("📊 Analytics Dashboard Demo")
    
    # Tracking automático de page view
    analytics.track_page_view("main_dashboard")
    
    # Botones de ejemplo
    if st.button("📈 Crear Gráfico"):
        create_chart()
        st.success("Gráfico creado!")
    
    if st.button("💾 Exportar Datos"):
        analytics.track_feature_usage("data_export")
        analytics.track_interaction("button", "export_data", "click")
        st.success("Datos exportados!")
    
    # Mostrar dashboard
    st.markdown("---")
    analytics.display_analytics_dashboard()

if __name__ == "__main__":
    main()
            """, language="python")
            
            st.markdown("**📊 Capacidades del Analytics Dashboard:**")
            capabilities = [
                "📈 **KPIs en tiempo real**: Views, sesiones únicas, interacciones",
                "🎯 **Tracking de características**: Qué funciones usan más los usuarios",
                "⏱️ **Análisis temporal**: Patrones de uso por hora y día",
                "🔍 **Interacciones detalladas**: Qué elementos tocan los usuarios",
                "📊 **Visualizaciones interactivas**: Gráficos con Plotly",
                "💾 **Persistencia de datos**: Mantiene historial entre sesiones"
            ]
            
            for capability in capabilities:
                st.markdown(f"• {capability}")

        # Performance tips actualizados
        st.markdown("---")
        st.markdown("### ⚡ Tips de Optimización Avanzados")
        
        performance_tips = [
            {
                "categoria": "🚀 Cache Estratégico",
                "tips": [
                    "Usa @st.cache_data(ttl=3600) para datos que cambian cada hora",
                    "Implementa @st.cache_resource para conexiones DB y modelos ML",
                    "Usa hash_funcs para objetos no serializables",
                    "Implementa cache warming en startup"
                ],
                "codigo": '''
@st.cache_data(ttl=3600, show_spinner="Cargando datos...")
def load_large_dataset():
    return pd.read_csv("large_file.csv")

@st.cache_resource
def get_database_connection():
    return psycopg2.connect(st.secrets["database_url"])

@st.cache_data(hash_funcs={pd.DataFrame: lambda x: x.shape})
def process_dataframe(df):
    return df.groupby("category").sum()
                '''
            },
            {
                "categoria": "🎯 UI/UX Optimizado",
                "tips": [
                    "Usa st.empty() para placeholders dinámicos",
                    "Implementa lazy loading con st.expander",
                    "Usa st.spinner() para operaciones lentas",
                    "Optimiza el layout con st.columns([1,2,1])"
                ],
                "codigo": '''
# Lazy loading de datos pesados
with st.expander("Ver datos detallados"):
    if st.button("Cargar datos"):
        with st.spinner("Procesando..."):
            data = expensive_operation()
            st.dataframe(data)

# Placeholder dinámico
placeholder = st.empty()
for i in range(100):
    placeholder.metric("Progreso", f"{i}%")
    time.sleep(0.1)
                '''
            },
            {
                "categoria": "💾 Gestión de Estado",
                "tips": [
                    "Usa session_state para datos temporales",
                    "Implementa cleanup de session_state",
                    "Evita objetos grandes en session_state",
                    "Usa keys únicos para widgets dinámicos"
                ],
                "codigo": '''
# Gestión eficiente de session state
def cleanup_old_data():
    for key in list(st.session_state.keys()):
        if key.startswith("temp_") and time.time() - st.session_state[f"{key}_timestamp"] > 3600:
            del st.session_state[key]

# Widget keys únicos
for i, item in enumerate(dynamic_list):
    st.text_input(f"Item {i}", key=f"item_{i}_{hash(item)}")
                '''
            }
        ]
        
        for tip_group in performance_tips:
            with st.expander(f"{tip_group['categoria']}", expanded=False):
                for tip in tip_group['tips']:
                    st.markdown(f"• {tip}")
                
                if 'codigo' in tip_group:
                    st.markdown("**💻 Código de ejemplo:**")
                    st.code(tip_group['codigo'], language="python")
    
    with monitor_tab3:
        st.markdown("### 🚨 Manejo de Errores")
        
        st.markdown("**Estrategias de Error Handling:**")
        
        # Ejemplos de manejo de errores
        error_examples = [
            {
                "titulo": "🔌 Errores de Conexión",
                "codigo": """
import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def make_request_with_retry(url, max_retries=3):
    session = requests.Session()
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("⏰ Timeout: La conexión tardó demasiado")
    except requests.exceptions.ConnectionError:
        st.error("🔌 Error de conexión: Verifica tu internet")
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ Error HTTP: {e.response.status_code}")
    except Exception as e:
        st.error(f"💥 Error inesperado: {str(e)}")
    
    return None
                """
            },
            {
                "titulo": "📊 Errores de Datos",
                "codigo": """
import pandas as pd
import streamlit as st

def safe_data_processing(data):
    try:
        # Validar que no esté vacío
        if data.empty:
            st.warning("⚠️ No hay datos para procesar")
            return None
        
        # Validar columnas requeridas
        required_cols = ['date', 'value']
        missing_cols = [col for col in required_cols if col not in data.columns]
        if missing_cols:
            st.error(f"❌ Columnas faltantes: {missing_cols}")
            return None
        
        # Procesar datos
        result = data.groupby('date')['value'].sum()
        
        # Validar resultado
        if result.isna().any():
            st.warning("⚠️ Se encontraron valores nulos en el resultado")
            result = result.fillna(0)
        
        return result
        
    except KeyError as e:
        st.error(f"🔑 Error de columna: {str(e)}")
    except ValueError as e:
        st.error(f"💢 Error de valor: {str(e)}")
    except Exception as e:
        st.error(f"💥 Error procesando datos: {str(e)}")
        st.exception(e)  # Mostrar stack trace en desarrollo
    
    return None
                """
            }
        ]
        
        for example in error_examples:
            with st.expander(example["titulo"], expanded=False):
                st.code(example["codigo"], language="python")
        
        # Error boundary pattern
        st.markdown("---")
        st.markdown("### 🛡️ Error Boundary Pattern")
        
        st.code("""
import streamlit as st
import traceback

class ErrorBoundary:
    def __init__(self, title="Error"):
        self.title = title
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            st.error(f"🚨 {self.title}")
            
            # En desarrollo: mostrar detalles
            if st.secrets.get("DEBUG", False):
                st.exception(exc_val)
                st.code(traceback.format_exc())
            else:
                st.error("Ocurrió un error inesperado. Contacta al administrador.")
            
            # Log del error
            logger.error(f"{self.title}: {str(exc_val)}", exc_info=True)
            
            # Evitar que el error se propague
            return True

# Uso
with ErrorBoundary("Error cargando datos"):
    data = load_potentially_failing_data()
    st.dataframe(data)

with ErrorBoundary("Error generando gráfico"):
    fig = create_complex_chart(data)
    st.plotly_chart(fig)
        """, language="python")
        
        # Checklist de error handling
        st.markdown("---")
        st.markdown("### ✅ Checklist de Error Handling")
        
        error_checklist = [
            "Manejo de errores de conexión/timeout",
            "Validación de entrada de usuarios",
            "Manejo de archivos corruptos/inválidos",            "Fallbacks para APIs que fallan",
            "Mensajes de error user-friendly",
            "Logging de errores para debug",
            "Graceful degradation de funciones",
            "Testing de casos edge"
        ]
        
        for i, item in enumerate(error_checklist):
            st.checkbox(item, key=f"error_check_{i}_{hash(item) % 10000}")

if __name__ == "__main__":
    run()
