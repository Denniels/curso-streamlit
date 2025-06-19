"""
SOLUCIÓN DEFINITIVA PARA ERRORES DEL DOM EN STREAMLIT 1.46.0
VERSIÓN 4: INTEGRACIÓN CON MÓDULOS EXISTENTES

Esta implementación combina:
1. La arquitectura DOM-safe de main_v3.py
2. Los módulos existentes (hello_world.py, widgets_basicos.py, sidebar_layout.py)
3. Control completo del ciclo de vida del DOM
"""

import streamlit as st
import hashlib
import time
import sys
import os

# Agregar el directorio de módulos al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modulo_01_fundamentos'))

# Importar módulos existentes
try:
    import hello_world
    import widgets_basicos
    import sidebar_layout
except ImportError as e:
    st.error(f"Error importando módulos: {e}")
    st.stop()

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
    
    def clear_all_except(self, keep_containers: list):
        """Limpia todos los contenedores excepto los especificados."""
        for container_id in list(self.containers.keys()):
            if container_id not in keep_containers:
                self.clear_container(container_id)
    
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
            'render_lock': False,
            'last_container': None
        }
    return st.session_state.nav_state

def render_navigation_v4():
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
                key=clase_key,
                index=0
            )
        
        # Actualizar estado solo si cambió
        if (nav_state['current_module'] != selected_modulo or 
            nav_state['current_class'] != selected_clase):
            nav_state['current_module'] = selected_modulo
            nav_state['current_class'] = selected_clase
            nav_state['last_render_time'] = time.time()
        
        return selected_modulo, selected_clase

def render_content_v4(modulo: str, clase: str):
    """Renderiza contenido usando los módulos existentes con control DOM-safe."""
    nav_state = safe_navigation_state()
    
    # Evitar re-render si está bloqueado
    if nav_state.get('render_lock', False):
        return
    
    nav_state['render_lock'] = True
    
    try:
        if modulo == "Módulo 1: Fundamentos" and clase:
            # Mapear clases a containers y módulos
            class_mapping = {
                "Clase 1: Hello, Streamlit": {
                    "container": "hello_world_main",
                    "module": hello_world
                },
                "Clase 2: Widgets básicos": {
                    "container": "widgets_main", 
                    "module": widgets_basicos
                },
                "Clase 3: Sidebar y layout": {
                    "container": "sidebar_main",
                    "module": sidebar_layout
                }
            }
            
            if clase in class_mapping:
                current_container = class_mapping[clase]["container"]
                current_module = class_mapping[clase]["module"]
                
                # Limpiar contenedores antiguos
                keep_containers = ["header_main", "footer_main", current_container]
                dom_renderer.clear_all_except(keep_containers)
                
                # Renderizar el módulo actual en su contenedor
                def module_wrapper():
                    try:
                        current_module.run()
                    except Exception as e:
                        st.error(f"Error ejecutando módulo: {e}")
                        st.exception(e)
                
                dom_renderer.render_in_container(current_container, module_wrapper)
                nav_state['last_container'] = current_container
            else:
                # Contenedor para mensaje de construcción
                def construction_msg():
                    st.warning("🎓 Esta clase aún está en construcción. Pronto estará disponible.")
                
                dom_renderer.render_in_container("construction_main", construction_msg)
        else:
            # Contenedor para módulos en construcción
            def construction_msg():
                st.warning("🎓 Este módulo aún está en construcción. Pronto estará disponible.")
            
            dom_renderer.render_in_container("construction_main", construction_msg)
    
    except Exception as e:
        st.error(f"Error en renderizado: {e}")
        st.exception(e)
    finally:
        nav_state['render_lock'] = False

def main_v4():
    """Función principal con integración de módulos existentes."""
    
    # ✅ 1. Configuración de página (solo una vez)
    if 'page_config_set' not in st.session_state:
        st.set_page_config(
            page_title="Curso Streamlit Interactivo",
            page_icon="🎓",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        st.session_state.page_config_set = True
    
    # ✅ 2. Título principal en contenedor fijo
    def header():
        st.title("🎓 Curso Completo e Interactivo de Streamlit")
        st.markdown("""
        **Bienvenido al curso interactivo de Streamlit por Daniel Mardones**
        
        Aquí aprenderás a dominar Streamlit desde lo más básico hasta aplicaciones avanzadas.
        Cada lección es interactiva y te permite ejecutar código en tiempo real.
        """)
        
        # Información de la versión
        st.info("🔧 **Versión 4**: Integración completa con módulos existentes + DOM-safe architecture")
    
    dom_renderer.render_in_container("header_main", header)
    
    # ✅ 3. Navegación
    modulo, clase = render_navigation_v4()
    
    # ✅ 4. Contenido principal usando módulos existentes
    render_content_v4(modulo, clase)
    
    # ✅ 5. Footer
    def footer():
        with st.sidebar:
            st.markdown("---")
            st.markdown("**Creado por Daniel Mardones** 🧠")
            st.markdown("📧 Curso interactivo de Streamlit")
            st.markdown("🔗 [GitHub](https://github.com/Denniels)")
            st.markdown("---")
            st.markdown("**🚀 Versión 4**")
            st.markdown("✅ DOM-safe + Módulos integrados")
    
    dom_renderer.render_in_container("footer_main", footer)

# ✅ EJECUTAR VERSIÓN 4
if __name__ == "__main__":
    main_v4()
