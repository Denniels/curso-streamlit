"""
SOLUCIÓN CORREGIDA PARA ERRORES DEL DOM EN STREAMLIT 1.46.0
VERSIÓN 4.1: INTEGRACIÓN SIMPLIFICADA Y FUNCIONAL

Esta implementación corrige los problemas de navegación de la v4.0
"""

import streamlit as st
import hashlib
import time
import sys
import os

# ✅ Configuración de página (SOLO UNA VEZ)
if 'page_configured' not in st.session_state:
    st.set_page_config(
        page_title="Curso Streamlit Interactivo",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.session_state.page_configured = True

# ✅ Agregar el directorio de módulos al path
current_dir = os.path.dirname(__file__)
module_dir = os.path.join(current_dir, 'modulo_01_fundamentos')
if module_dir not in sys.path:
    sys.path.insert(0, module_dir)

# ✅ Importar módulos existentes
@st.cache_resource
def import_modules():
    """Importa módulos con cache para optimizar."""
    try:
        import hello_world
        import widgets_basicos
        import sidebar_layout
        return {
            'hello_world': hello_world,
            'widgets_basicos': widgets_basicos,
            'sidebar_layout': sidebar_layout
        }
    except ImportError as e:
        st.error(f"❌ Error importando módulos: {e}")
        st.error(f"🔍 Directorio de módulos: {module_dir}")
        st.error(f"📁 Existe el directorio: {os.path.exists(module_dir)}")
        if os.path.exists(module_dir):
            files = os.listdir(module_dir)
            st.error(f"📋 Archivos encontrados: {files}")
        st.stop()
        return None

# ✅ Obtener módulos importados
modules = import_modules()

def generate_safe_key(base_key: str, context: str = "default") -> str:
    """Genera keys únicos y seguros."""
    combined = f"{context}_{base_key}_{time.time_ns()}"
    hash_obj = hashlib.md5(combined.encode())
    return f"{context}_{base_key}_{hash_obj.hexdigest()[:8]}"

def initialize_navigation_state():
    """Inicializa el estado de navegación."""
    if 'navigation' not in st.session_state:
        st.session_state.navigation = {
            'current_module': 'Módulo 1: Fundamentos',
            'current_class': 'Clase 1: Hello, Streamlit',
            'last_update': time.time()
        }
    return st.session_state.navigation

def render_sidebar_navigation():
    """Renderiza la navegación en el sidebar."""
    nav_state = initialize_navigation_state()
    
    with st.sidebar:
        st.markdown("# 📚 Curso Streamlit")
        st.markdown("*Por Daniel Mardones*")
        st.markdown("---")
        
        # ✅ Selector de módulo con key fijo
        selected_module = st.selectbox(
            "📖 Selecciona un módulo:",
            [
                "Módulo 1: Fundamentos",
                "Módulo 2: Visualización",
                "Módulo 3: Interactividad", 
                "Módulo 4: Aplicaciones",
                "Módulo 5: Despliegue",
                "Bonus: Automatización"
            ],
            index=0,
            key="module_selector_fixed"
        )
        
        # ✅ Selector de clase (solo para Módulo 1)
        selected_class = None
        if selected_module == "Módulo 1: Fundamentos":
            selected_class = st.radio(
                "📝 Selecciona la clase:",
                [
                    "Clase 1: Hello, Streamlit",
                    "Clase 2: Widgets básicos",
                    "Clase 3: Sidebar y layout"
                ],
                index=0,
                key="class_selector_fixed"
            )
        
        # ✅ Información de estado
        st.markdown("---")
        st.markdown("### 📊 Estado Actual")
        st.write(f"**Módulo:** {selected_module}")
        if selected_class:
            st.write(f"**Clase:** {selected_class}")
        
        # ✅ Actualizar estado solo si cambió
        if (nav_state['current_module'] != selected_module or 
            nav_state['current_class'] != selected_class):
            
            nav_state['current_module'] = selected_module
            nav_state['current_class'] = selected_class
            nav_state['last_update'] = time.time()
            
            # ✅ Forzar rerun para actualizar contenido
            st.rerun()
        
        return selected_module, selected_class

def render_main_content(selected_module: str, selected_class: str):
    """Renderiza el contenido principal."""
    
    # ✅ Header principal
    st.title("🎓 Curso Completo e Interactivo de Streamlit")
    st.markdown("""
    **Bienvenido al curso interactivo de Streamlit por Daniel Mardones**
    
    Aprende Streamlit desde lo básico hasta aplicaciones avanzadas con lecciones interactivas.
    """)
    
    # ✅ Información de versión
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.info("🔧 **Versión 4.1**: Navegación corregida + DOM-safe")
    with col2:
        st.metric("Streamlit", st.__version__)
    with col3:
        st.metric("Módulos", "3 disponibles")
    
    st.markdown("---")
    
    # ✅ Renderizar contenido basado en selección
    if selected_module == "Módulo 1: Fundamentos" and selected_class:
        
        # ✅ Mapeo directo de clases a módulos
        class_to_module = {
            "Clase 1: Hello, Streamlit": modules['hello_world'],
            "Clase 2: Widgets básicos": modules['widgets_basicos'],
            "Clase 3: Sidebar y layout": modules['sidebar_layout']
        }
        
        if selected_class in class_to_module:
            try:
                # ✅ Mostrar información de la clase actual
                st.markdown(f"### 🎯 {selected_class}")
                st.markdown(f"**Módulo:** {selected_module}")
                
                # ✅ Contenedor para el módulo
                module_container = st.container()
                
                with module_container:
                    # ✅ Ejecutar el módulo correspondiente
                    current_module = class_to_module[selected_class]
                    
                    # ✅ Debug info
                    with st.expander("🔍 Información de Debug", expanded=False):
                        st.write(f"**Módulo ejecutado:** {current_module.__name__}")
                        st.write(f"**Función run disponible:** {hasattr(current_module, 'run')}")
                        st.write(f"**Timestamp:** {time.strftime('%H:%M:%S')}")
                    
                    # ✅ Ejecutar función run del módulo
                    if hasattr(current_module, 'run'):
                        current_module.run()
                    else:
                        st.error(f"❌ El módulo {current_module.__name__} no tiene función 'run()'")
                        
            except Exception as e:
                st.error(f"❌ Error ejecutando la clase: {str(e)}")
                with st.expander("🔍 Detalles del error"):
                    st.exception(e)
        else:
            st.warning(f"⚠️ La clase '{selected_class}' no está disponible aún.")
    
    else:
        # ✅ Contenido para módulos en construcción
        st.warning("🚧 Este módulo está en construcción")
        st.markdown("""
        ### Módulos Disponibles:
        - ✅ **Módulo 1: Fundamentos** (3 clases disponibles)
        - 🚧 **Módulo 2: Visualización** (Próximamente)
        - 🚧 **Módulo 3: Interactividad** (Próximamente)
        - 🚧 **Módulo 4: Aplicaciones** (Próximamente)
        - 🚧 **Módulo 5: Despliegue** (Próximamente)
        - 🚧 **Bonus: Automatización** (Próximamente)
        """)

def main():
    """Función principal corregida."""
    try:
        # ✅ 1. Navegación en sidebar
        selected_module, selected_class = render_sidebar_navigation()
        
        # ✅ 2. Contenido principal
        render_main_content(selected_module, selected_class)
        
        # ✅ 3. Footer en sidebar
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 👨‍💻 Autor")
            st.markdown("**Daniel Mardones**")
            st.markdown("🧠 Mentor en Python & Data Science")
            st.markdown("[🔗 GitHub](https://github.com/Denniels)")
            
    except Exception as e:
        st.error(f"❌ Error en la aplicación principal: {str(e)}")
        with st.expander("🔍 Detalles del error"):
            st.exception(e)

# ✅ Ejecutar aplicación
if __name__ == "__main__":
    main()
