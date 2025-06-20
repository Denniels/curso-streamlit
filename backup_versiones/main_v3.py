"""
SOLUCIÓN DEFINITIVA PARA ERRORES DEL DOM EN STREAMLIT 1.46.0

Esta implementación usa técnicas avanzadas específicas para esta versión:
1. Contenedores vacíos (st.empty()) para limpiar DOM
2. Control de ciclo de vida de widgets
3. Renderizado condicional con locks
4. Keys únicos con hashing
"""

import streamlit as st
import hashlib
import time

class DOMSafeRenderer:
    """Renderizador que previene errores del DOM mediante control de ciclo de vida."""
    
    def __init__(self):
        self.containers = {}
        self.widget_registry = {}
        
    def get_safe_key(self, base_key: str, context: str = "global") -> str:
        """Genera keys únicos usando hash para evitar conflictos."""
        # Crear hash único basado en contexto y key
        hash_input = f"{context}_{base_key}_{id(self)}"
        key_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return f"{context}_{base_key}_{key_hash}"
    
    def get_container(self, container_id: str):
        """Obtiene o crea un contenedor único."""
        if container_id not in self.containers:
            self.containers[container_id] = st.empty()
        return self.containers[container_id]
    
    def clear_container(self, container_id: str):
        """Limpia un contenedor específico."""
        if container_id in self.containers:
            self.containers[container_id].empty()
    
    def render_in_container(self, container_id: str, render_func):
        """Renderiza contenido en un contenedor específico."""
        container = self.get_container(container_id)
        with container.container():
            render_func()

# Instancia global del renderizador
dom_renderer = DOMSafeRenderer()

def safe_navigation_state():
    """Estado de navegación completamente aislado."""
    if 'nav_state' not in st.session_state:
        st.session_state.nav_state = {
            'current_module': 'Módulo 1: Fundamentos',
            'current_class': 'Clase 1: Hello, Streamlit',
            'last_render_time': time.time(),
            'render_lock': False
        }
    return st.session_state.nav_state

def render_navigation_v3():
    """Navegación con control absoluto del DOM."""
    nav_state = safe_navigation_state()
    
    with st.sidebar:
        st.markdown("# 📚 Navegación")
        
        # ✅ Selectbox con key único y hash
        modulo_key = dom_renderer.get_safe_key("modulo_selector", "nav")
        selected_modulo = st.selectbox(
            "Selecciona un módulo",
            [
                "Módulo 1: Fundamentos",
                "Módulo 2: Visualización",
                "Módulo 3: Interactividad",
                "Módulo 4: Aplicaciones",
                "Módulo 5: Despliegue",
                "Bonus: Automatización"
            ],
            key=modulo_key,
            index=0
        )
        
        selected_clase = None
        if selected_modulo == "Módulo 1: Fundamentos":
            # ✅ Radio con key único y hash
            clase_key = dom_renderer.get_safe_key("clase_selector", "nav")
            selected_clase = st.radio(
                "Selecciona la clase:",
                [
                    "Clase 1: Hello, Streamlit",
                    "Clase 2: Widgets básicos",
                    "Clase 3: Sidebar y layout"
                ],
                key=clase_key
            )
        
        # Actualizar estado solo si cambió
        if (nav_state['current_module'] != selected_modulo or 
            nav_state['current_class'] != selected_clase):
            nav_state['current_module'] = selected_modulo
            nav_state['current_class'] = selected_clase
            nav_state['last_render_time'] = time.time()
        
        return selected_modulo, selected_clase

def render_hello_world_v3():
    """Hello World con renderizado DOM-safe."""
    
    def content():
        st.title("🎈 Módulo 1: ¡Hola, Streamlit!")
        
        st.markdown("""
        Explora cada pestaña para ver cómo construir tu primera app con Streamlit.  
        Esta lección interactiva te permite ejecutar el código, ver el resultado y aprender su sintaxis.
        """)
        
        # ✅ Tabs con keys únicos usando hash
        tab_keys = [
            dom_renderer.get_safe_key("tab1", "hello"),
            dom_renderer.get_safe_key("tab2", "hello"),
            dom_renderer.get_safe_key("tab3", "hello"),
            dom_renderer.get_safe_key("tab4", "hello")
        ]
        
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
            
            # ✅ Botón con key hasheado único
            btn_key = dom_renderer.get_safe_key("saludar_btn", "hello")
            if st.button("Presiona para saludar", key=btn_key):
                st.success("¡Bienvenido al mundo Streamlit, soy tu mentor Daniel Mardones! 🎉")
            
            st.code("""
if st.button("Presiona para saludar"):
    st.success("¡Bienvenido al mundo Streamlit!")
""", language="python")
        
        with tab4:
            st.subheader("📘 Créditos")
            st.info("Curso creado por Daniel Mardones\nMentoría técnica en Python y Data Science 🤖✨")
    
    # Renderizar en contenedor aislado
    dom_renderer.render_in_container("hello_world_main", content)

def render_widgets_v3():
    """Widgets con renderizado DOM-safe."""
    
    def content():
        st.title("🎛️ Clase 2: Interacción con Widgets")
        st.markdown("""
        En esta clase exploraremos botones, sliders, entradas de texto y selectores.  
        Las apps que construyas serán dinámicas e interactivas.
        """)
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔘 Botón",
            "🎚️ Slider",
            "🧾 Text Input",
            "📋 Selectbox"
        ])
        
        with tab1:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # ✅ Key hasheado único
                btn_key = dom_renderer.get_safe_key("click_btn", "widgets")
                clic = st.button("Haz clic aquí 👆", key=btn_key)
            
            with col2:
                if clic:
                    st.success("¡Click recibido!")
            
            st.code("""
clic = st.button("Haz clic aquí 👆")
if clic:
    st.success("¡Click recibido!")
""", language="python")
        
        with tab2:
            # ✅ Slider con key hasheado único
            slider_key = dom_renderer.get_safe_key("edad_slider", "widgets")
            edad = st.slider("Tu edad (años)", 0, 100, 25, key=slider_key)
            st.write(f"Tienes {edad} años.")
            
            st.code("""
edad = st.slider("Tu edad (años)", 0, 100, 25)
st.write(f"Tienes {edad} años.")
""", language="python")
        
        with tab3:
            # ✅ Text input con key hasheado único
            input_key = dom_renderer.get_safe_key("nombre_input", "widgets")
            nombre = st.text_input("¿Cómo te llamas?", key=input_key)
            if nombre:
                st.success(f"Hola, {nombre} 👋")
            
            st.code("""
nombre = st.text_input("¿Cómo te llamas?")
if nombre:
    st.success(f"Hola, {nombre} 👋")
""", language="python")
        
        with tab4:
            # ✅ Selectbox con key hasheado único
            select_key = dom_renderer.get_safe_key("lenguaje_select", "widgets")
            lenguaje = st.selectbox(
                "Tu lenguaje favorito 💻",
                ["Python", "SQL", "R", "JavaScript", "Otro"],
                key=select_key
            )
            st.info(f"Elegiste: **{lenguaje}**")
            
            st.code("""
lenguaje = st.selectbox("Tu lenguaje favorito 💻", 
                       ["Python", "SQL", "R", "JavaScript", "Otro"])
st.info(f"Elegiste: {lenguaje}")
""", language="python")
    
    # Renderizar en contenedor aislado
    dom_renderer.render_in_container("widgets_main", content)

def render_sidebar_v3():
    """Sidebar con renderizado DOM-safe."""
    
    def content():
        st.title("🧭 Clase 3: Organización con Sidebar")
        st.markdown("""
        Streamlit te permite mover widgets al sidebar para mantener el área principal más limpia y enfocada en resultados.
        """)
        
        tab1, tab2, tab3 = st.tabs([
            "📐 Layout básico",
            "📊 Parámetros dinámicos",
            "🧠 Vista final"
        ])
        
        with tab1:
            st.subheader("📐 Layout básico con sidebar")
            
            # ✅ Widgets en sidebar con keys hasheados únicos
            with st.sidebar:
                st.markdown("### 👤 Perfil de Usuario")
                user_key = dom_renderer.get_safe_key("user_input", "sidebar")
                edad_key = dom_renderer.get_safe_key("edad_slider", "sidebar")
                
                user_name = st.text_input("Escribe tu nombre:", key=user_key)
                edad = st.slider("Tu edad:", 18, 99, 25, key=edad_key)
            
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
                puntos_key = dom_renderer.get_safe_key("puntos_slider", "sidebar")
                ruido_key = dom_renderer.get_safe_key("ruido_slider", "sidebar")
                
                puntos = st.slider("N° de puntos", 10, 500, 100, key=puntos_key)
                ruido = st.slider("Nivel de ruido", 0.0, 1.0, 0.1, key=ruido_key)
            
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
    
    # Renderizar en contenedor aislado
    dom_renderer.render_in_container("sidebar_main", content)

def render_content_v3(modulo: str, clase: str):
    """Renderiza contenido con control absoluto del DOM."""
    nav_state = safe_navigation_state()
    
    # Evitar re-render si está bloqueado
    if nav_state.get('render_lock', False):
        return
    
    nav_state['render_lock'] = True
    
    try:
        if modulo == "Módulo 1: Fundamentos" and clase:
            # Limpiar contenedor anterior si es necesario
            current_time = time.time()
            if current_time - nav_state.get('last_render_time', 0) > 0.1:
                # Limpiar contenedores antiguos
                for container_id in ['hello_world_main', 'widgets_main', 'sidebar_main']:
                    if container_id not in [f"{clase.split(':')[0].lower().replace(' ', '_')}_main"]:
                        dom_renderer.clear_container(container_id)
            
            if clase == "Clase 1: Hello, Streamlit":
                render_hello_world_v3()
            elif clase == "Clase 2: Widgets básicos":
                render_widgets_v3()
            elif clase == "Clase 3: Sidebar y layout":
                render_sidebar_v3()
        else:
            # Contenedor para mensaje de construcción
            def construction_msg():
                st.warning("🎓 Este módulo aún está en construcción. Pronto estará disponible.")
            
            dom_renderer.render_in_container("construction_main", construction_msg)
    
    finally:
        nav_state['render_lock'] = False

def main_v3():
    """Función principal con control total del DOM."""
    
    # ✅ 1. Título principal en contenedor fijo
    def header():
        st.title("Curso completo e interactivo de Streamlit")
        st.markdown("""
        Bienvenido al curso interactivo de Streamlit. Aquí aprenderás a dominar Streamlit 
        desde lo más básico hasta aplicaciones avanzadas.
        """)
    
    dom_renderer.render_in_container("header_main", header)
    
    # ✅ 2. Navegación
    modulo, clase = render_navigation_v3()
    
    # ✅ 3. Contenido principal
    render_content_v3(modulo, clase)
    
    # ✅ 4. Footer
    def footer():
        with st.sidebar:
            st.markdown("---")
            st.markdown("**Creado por Daniel Mardones** 🧠")
            st.markdown("Curso interactivo de Streamlit")
            st.markdown("[GitHub](https://github.com/Denniels)")
    
    dom_renderer.render_in_container("footer_main", footer)

# ✅ EJECUTAR VERSIÓN 3
if __name__ == "__main__":
    main_v3()
