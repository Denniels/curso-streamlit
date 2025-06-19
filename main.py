import streamlit as st
import time
from typing import Dict, Any

# ✅ CONFIGURACIÓN ÚNICA Y CRÍTICA PARA STREAMLIT 1.46.0
st.set_page_config(
    page_title="Curso Streamlit Interactivo",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ SOLUCIÓN RADICAL: Sistema de páginas completamente aisladas
class StreamlitPageManager:
    """Gestor de páginas que previene completamente los errores del DOM."""
    
    def __init__(self):
        self.initialize_state()
    
    def initialize_state(self):
        """Inicialización única y segura del estado."""
        if 'page_manager_initialized' not in st.session_state:
            st.session_state.page_manager_initialized = True
            st.session_state.current_page_id = "home"
            st.session_state.navigation_lock = False
            st.session_state.page_cache = {}
    
    def safe_navigation(self, page_id: str):
        """Navegación segura que previene conflictos del DOM."""
        if st.session_state.navigation_lock:
            return st.session_state.current_page_id
        
        if st.session_state.current_page_id != page_id:
            st.session_state.navigation_lock = True
            st.session_state.current_page_id = page_id
            # Forzar rerun limpio
            st.rerun()
        
        return page_id
    
    def unlock_navigation(self):
        """Desbloquea la navegación después del renderizado."""
        st.session_state.navigation_lock = False

# Instancia global del gestor
page_manager = StreamlitPageManager()

def render_navigation():
    """Sistema de navegación completamente rediseñado."""
    
    with st.sidebar:
        st.markdown("# 📚 Navegación")
        
        # ✅ Selectbox con manejo de estado propio
        modulo_options = [
            "Módulo 1: Fundamentos",
            "Módulo 2: Visualización", 
            "Módulo 3: Interactividad",
            "Módulo 4: Aplicaciones",
            "Módulo 5: Despliegue",
            "Bonus: Automatización"
        ]
        
        # Key único y estático
        selected_modulo = st.selectbox(
            "Selecciona un módulo",
            modulo_options,
            key="main_modulo_selector_v2",
            index=0
        )
        
        selected_clase = None
        if selected_modulo == "Módulo 1: Fundamentos":
            clase_options = [
                "Clase 1: Hello, Streamlit",
                "Clase 2: Widgets básicos",
                "Clase 3: Sidebar y layout"
            ]
            
            selected_clase = st.radio(
                "Selecciona la clase:",
                clase_options,
                key="main_clase_selector_v2"
            )
        
        return selected_modulo, selected_clase

def render_hello_world_page():
    """Página Hello World completamente aislada."""
    
    # ✅ Contenedor único con ID específico
    page_container = st.container()
    
    with page_container:
        st.title("🎈 Módulo 1: ¡Hola, Streamlit!")
        
        st.markdown("""
        Explora cada pestaña para ver cómo construir tu primera app con Streamlit.  
        Esta lección interactiva te permite ejecutar el código, ver el resultado y aprender su sintaxis.
        """)
        
        # ✅ Tabs con keys únicos y estáticos
        tab1, tab2, tab3, tab4 = st.tabs([
            "👋 Título y texto",
            "📝 Markdown enriquecido",
            "🎛️ Botón interactivo", 
            "📘 Créditos"
        ])
        
        with tab1:
            st.subheader("👋 Título y subtítulo")
            st.title("¡Hola, Streamlit!")
            st.write("Este es tu primer texto interactivo.")
            
            st.code("""
st.title("¡Hola, Streamlit!")
st.write("Este es tu primer texto interactivo.")
""", language="python")
        
        with tab2:
            st.subheader("📝 Markdown enriquecido")
            st.markdown("""
### ¿Qué puedes hacer con Streamlit?

- Crear apps web desde Python puro  
- Usar Markdown como este para dar formato  
- Incluir enlaces: [Visitar Streamlit](https://streamlit.io)
""")
            
            st.code("""
st.markdown(\"\"\"
### ¿Qué puedes hacer con Streamlit?

- Crear apps web desde Python puro  
- Usar Markdown como este para dar formato  
- Incluir enlaces: [Visitar Streamlit](https://streamlit.io)
\"\"\")
""", language="python")
        
        with tab3:
            st.subheader("🎛️ Botón interactivo")
            
            # ✅ Key completamente único para evitar conflictos
            if st.button("Presiona para saludar", key="hello_world_btn_unique_v2"):
                st.success("¡Bienvenido al mundo Streamlit, soy tu mentor Daniel Mardones! 🎉")
            
            st.code("""
if st.button("Presiona para saludar"):
    st.success("¡Bienvenido al mundo Streamlit!")
""", language="python")
        
        with tab4:
            st.subheader("📘 Créditos")
            st.info("Curso creado por Daniel Mardones\nMentoría técnica en Python y Data Science 🤖✨")

def render_widgets_page():
    """Página Widgets completamente aislada."""
    
    page_container = st.container()
    
    with page_container:
        st.title("🎛️ Clase 2: Interacción con Widgets")
        st.markdown("""
        En esta clase exploraremos botones, sliders, entradas de texto y selectores.  
        Las apps que construyas serán dinámicas e interactivas.
        """)
        
        # ✅ Tabs con keys únicos
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔘 Botón",
            "🎚️ Slider", 
            "🧾 Text Input",
            "📋 Selectbox"
        ])
        
        with tab1:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # ✅ Key único para evitar conflictos
                clic = st.button("Haz clic aquí 👆", key="widgets_btn_unique_v2")
            
            with col2:
                if clic:
                    st.success("¡Click recibido!")
            
            st.code("""
clic = st.button("Haz clic aquí 👆")
if clic:
    st.success("¡Click recibido!")
""", language="python")
        
        with tab2:
            # ✅ Key único para slider
            edad = st.slider("Tu edad (años)", 0, 100, 25, key="widgets_slider_unique_v2")
            st.write(f"Tienes {edad} años.")
            
            st.code("""
edad = st.slider("Tu edad (años)", 0, 100, 25)
st.write(f"Tienes {edad} años.")
""", language="python")
        
        with tab3:
            # ✅ Key único para text input
            nombre = st.text_input("¿Cómo te llamas?", key="widgets_input_unique_v2")
            if nombre:
                st.success(f"Hola, {nombre} 👋")
            
            st.code("""
nombre = st.text_input("¿Cómo te llamas?")
if nombre:
    st.success(f"Hola, {nombre} 👋")
""", language="python")
        
        with tab4:
            # ✅ Key único para selectbox
            lenguaje = st.selectbox(
                "Tu lenguaje favorito 💻",
                ["Python", "SQL", "R", "JavaScript", "Otro"],
                key="widgets_select_unique_v2"
            )
            st.info(f"Elegiste: **{lenguaje}**")
            
            st.code("""
lenguaje = st.selectbox("Tu lenguaje favorito 💻", 
                       ["Python", "SQL", "R", "JavaScript", "Otro"])
st.info(f"Elegiste: {lenguaje}")
""", language="python")

def render_sidebar_page():
    """Página Sidebar completamente aislada."""
    
    page_container = st.container()
    
    with page_container:
        st.title("🧭 Clase 3: Organización con Sidebar")
        st.markdown("""
        Streamlit te permite mover widgets al sidebar para mantener el área principal más limpia y enfocada en resultados.
        """)
        
        # ✅ Tabs con keys únicos
        tab1, tab2, tab3 = st.tabs([
            "📐 Layout básico",
            "📊 Parámetros dinámicos", 
            "🧠 Vista final"
        ])
        
        with tab1:
            st.subheader("📐 Layout básico con sidebar")
            
            # ✅ Widgets en sidebar con keys únicos
            with st.sidebar:
                st.markdown("### 👤 Perfil de Usuario")
                user_name = st.text_input("Escribe tu nombre:", key="sidebar_user_unique_v2")
                edad = st.slider("Tu edad:", 18, 99, 25, key="sidebar_edad_unique_v2")
            
            if user_name:
                st.success(f"Bienvenido, {user_name} 👋 (Edad: {edad})")
            
            st.code("""
# En el sidebar
user_name = st.sidebar.text_input("Escribe tu nombre:")
edad = st.sidebar.slider("Tu edad:", 18, 99, 25)
""", language="python")
        
        with tab2:
            st.subheader("📊 Parámetros dinámicos (Ejemplo con gráfico)")
            
            with st.sidebar:
                st.markdown("### ⚙️ Configuración del Gráfico")
                puntos = st.slider("N° de puntos", 10, 500, 100, key="sidebar_puntos_unique_v2")
                ruido = st.slider("Nivel de ruido", 0.0, 1.0, 0.1, key="sidebar_ruido_unique_v2")
            
            # Generar gráfico
            import numpy as np
            import pandas as pd
            
            x = np.linspace(0, 10, puntos)
            y = np.sin(x) + np.random.normal(scale=ruido, size=puntos)
            df = pd.DataFrame({"x": x, "y": y})
            
            st.line_chart(df.set_index("x"))
            
            st.code("""
puntos = st.sidebar.slider("N° de puntos", 10, 500, 100)
ruido = st.sidebar.slider("Nivel de ruido", 0.0, 1.0, 0.1)

x = np.linspace(0, 10, puntos)
y = np.sin(x) + np.random.normal(scale=ruido, size=puntos)
df = pd.DataFrame({"x": x, "y": y})
st.line_chart(df.set_index("x"))
""", language="python")
        
        with tab3:
            st.subheader("🧠 ¿Por qué usar sidebar?")
            st.markdown("""
- Separa la entrada de parámetros del contenido visual  
- Mejora la experiencia de usuario  
- Ideal para dashboards y simuladores
            """)

def render_main_content(modulo: str, clase: str):
    """Renderiza el contenido principal con control absoluto."""
    
    # ✅ Determinar qué página mostrar
    if modulo == "Módulo 1: Fundamentos" and clase:
        if clase == "Clase 1: Hello, Streamlit":
            page_id = page_manager.safe_navigation("hello_world")
            if page_id == "hello_world":
                render_hello_world_page()
        
        elif clase == "Clase 2: Widgets básicos":
            page_id = page_manager.safe_navigation("widgets")
            if page_id == "widgets":
                render_widgets_page()
        
        elif clase == "Clase 3: Sidebar y layout":
            page_id = page_manager.safe_navigation("sidebar")
            if page_id == "sidebar":
                render_sidebar_page()
    
    else:
        st.warning("🎓 Este módulo aún está en construcción. Pronto estará disponible.")
    
    # ✅ Desbloquear navegación después del renderizado
    page_manager.unlock_navigation()

def render_footer():
    """Footer estático."""
    with st.sidebar:
        st.markdown("---")
        st.markdown("**Creado por Daniel Mardones** 🧠")
        st.markdown("Curso interactivo de Streamlit")
        st.markdown("[GitHub](https://github.com/Denniels)")

def main():
    """Función principal con control absoluto del flujo de renderizado."""
    
    # ✅ 1. Inicializar gestor de páginas
    page_manager.initialize_state()
    
    # ✅ 2. Título principal (renderizado una sola vez)
    st.title("Curso completo e interactivo de Streamlit")
    st.markdown("""
    Bienvenido al curso interactivo de Streamlit. Aquí aprenderás a dominar Streamlit 
    desde lo más básico hasta aplicaciones avanzadas.
    """)
    
    # ✅ 3. Navegación estable
    modulo, clase = render_navigation()
    
    # ✅ 4. Contenido con control absoluto
    render_main_content(modulo, clase)
    
    # ✅ 5. Footer estático
    render_footer()

# ✅ EJECUTAR APLICACIÓN
if __name__ == "__main__":
    main()
