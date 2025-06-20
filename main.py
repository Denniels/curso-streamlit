"""
CURSO INTERACTIVO DE STREAMLIT
Por Daniel Mardones

Curso completo e interactivo para aprender Streamlit desde lo básico 
hasta aplicaciones avanzadas con navegación DOM-safe.
Asegurate que el modulo este cargado correctamente en informacion de debug.
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

# ✅ Agregar los directorios de módulos al path
current_dir = os.path.dirname(__file__)
for modulo in ['modulo_01_fundamentos', 'modulo_02_visualizacion', 'modulo_03_interactividad', 
               'modulo_04_aplicaciones', 'modulo_05_despliegue', 'modulo_06_bonus_automatizacion',
               'modulo_07_evaluacion']:
    module_dir = os.path.join(current_dir, modulo)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)

# ✅ Importar módulos existentes
@st.cache_resource
def import_modules():
    """Importa módulos con cache para optimizar."""
    try:
        # Módulo 1: Fundamentos
        import hello_world
        import widgets_basicos
        import sidebar_layout
        
        # Módulo 2: Visualización
        import graficos_basicos
        import dashboards_interactivos
        
        # Módulo 3: Interactividad
        import manejo_datos
        
        # Módulo 4: Aplicaciones
        import calculadora_financiera
        import sistema_inventario
        
        # Módulo 5: Despliegue
        import streamlit_cloud
          # Módulo 6: Bonus Automatización
        import github_actions
        
        # Módulo 7: Evaluación
        import test_interactivo
        
        return {
            # Módulo 1
            'hello_world': hello_world,
            'widgets_basicos': widgets_basicos,
            'sidebar_layout': sidebar_layout,
            # Módulo 2
            'graficos_basicos': graficos_basicos,
            'dashboards_interactivos': dashboards_interactivos,
            # Módulo 3
            'manejo_datos': manejo_datos,
            # Módulo 4
            'calculadora_financiera': calculadora_financiera,
            'sistema_inventario': sistema_inventario,            # Módulo 5
            'streamlit_cloud': streamlit_cloud,
            # Módulo 6
            'github_actions': github_actions,
            # Módulo 7
            'test_interactivo': test_interactivo
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
            "📖 Selecciona un módulo:",            [
                "Módulo 1: Fundamentos",
                "Módulo 2: Visualización",
                "Módulo 3: Interactividad", 
                "Módulo 4: Aplicaciones",
                "Módulo 5: Despliegue",
                "Bonus: Automatización",
                "Módulo 7: Evaluación"
            ],
            index=0,
            key="module_selector_fixed"
        )
        
        # ✅ Selector de clase según el módulo seleccionado
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
                key="class_selector_modulo1"
            )
        elif selected_module == "Módulo 2: Visualización":
            selected_class = st.radio(
                "📊 Selecciona la clase:",
                [
                    "Clase 1: Gráficos básicos",
                    "Clase 2: Dashboards interactivos"
                ],
                index=0,
                key="class_selector_modulo2"
            )
        elif selected_module == "Módulo 3: Interactividad":
            selected_class = st.radio(
                "🔄 Selecciona la clase:",
                [
                    "Clase 1: Manejo de datos"
                ],
                index=0,
                key="class_selector_modulo3"
            )
        elif selected_module == "Módulo 4: Aplicaciones":
            selected_class = st.radio(
                "🏗️ Selecciona la clase:",
                [
                    "Clase 1: Calculadora financiera",
                    "Clase 2: Sistema de inventario"
                ],
                index=0,
                key="class_selector_modulo4"
            )
        elif selected_module == "Módulo 5: Despliegue":
            selected_class = st.radio(
                "☁️ Selecciona la clase:",                [
                    "Clase 1: Streamlit Cloud"
                ],
                index=0,
                key="class_selector_modulo5"
            )
        elif selected_module == "Bonus: Automatización":
            selected_class = st.radio(
                "🤖 Selecciona la clase:",
                [
                    "Clase 1: GitHub Actions"
                ],
                index=0,
                key="class_selector_modulo6"
            )
        elif selected_module == "Módulo 7: Evaluación":
            selected_class = st.radio(
                "🎯 Selecciona la clase:",
                [
                    "Clase 1: Test Interactivo"
                ],
                index=0,
                key="class_selector_modulo7"
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
            
            # ✅ Limpiar cache de módulos para evitar conflictos DOM
            if hasattr(st, 'cache_resource'):
                st.cache_resource.clear()
            
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
    
    Asegurate que el modulo este cargado correctamente en informacion de debug.
    """)
      # ✅ Información de versión
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.info("🎓 **Curso Streamlit Interactivo**: Navegación optimizada + DOM-safe")
    with col2:
        st.metric("Streamlit", st.__version__)
    with col3:
        st.metric("Módulos", "11 clases totales")
    
    st.markdown("---")
    
    # ✅ Renderizar contenido basado en selección
    if selected_class:  # Si hay una clase seleccionada
        
        # ✅ Mapeo completo de clases a módulos
        class_to_module = {
            # Módulo 1: Fundamentos
            "Clase 1: Hello, Streamlit": modules['hello_world'],
            "Clase 2: Widgets básicos": modules['widgets_basicos'],
            "Clase 3: Sidebar y layout": modules['sidebar_layout'],
            # Módulo 2: Visualización  
            "Clase 1: Gráficos básicos": modules['graficos_basicos'],
            "Clase 2: Dashboards interactivos": modules['dashboards_interactivos'],
            # Módulo 3: Interactividad
            "Clase 1: Manejo de datos": modules['manejo_datos'],
            # Módulo 4: Aplicaciones
            "Clase 1: Calculadora financiera": modules['calculadora_financiera'],
            "Clase 2: Sistema de inventario": modules['sistema_inventario'],            # Módulo 5: Despliegue
            "Clase 1: Streamlit Cloud": modules['streamlit_cloud'],
            # Módulo 6: Bonus Automatización
            "Clase 1: GitHub Actions": modules['github_actions'],
            # Módulo 7: Evaluación
            "Clase 1: Test Interactivo": modules['test_interactivo']
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
                    
                    # ✅ Ejecutar función run del módulo con protección DOM
                    try:
                        if hasattr(current_module, 'run'):
                            # Crear contenedor único para cada módulo
                            with st.container():
                                current_module.run()
                        else:
                            st.error(f"❌ El módulo {current_module.__name__} no tiene función 'run()'")
                    except Exception as module_error:
                        st.error(f"❌ Error específico del módulo {current_module.__name__}: {str(module_error)}")
                        with st.expander("🔍 Detalles del error del módulo"):
                            st.exception(module_error)
                        
            except Exception as e:
                st.error(f"❌ Error ejecutando la clase: {str(e)}")
                with st.expander("🔍 Detalles del error"):
                    st.exception(e)
        else:
            st.warning(f"⚠️ La clase '{selected_class}' no está disponible aún.")
    
    else:
        # ✅ Contenido para módulos en construcción o sin clase seleccionada
        st.warning("🚧 Selecciona una clase del módulo para ver el contenido")
        st.markdown("""        ### 📚 Estado de Módulos:
        - ✅ **Módulo 1: Fundamentos** (3 clases disponibles)
        - ✅ **Módulo 2: Visualización** (2 clases disponibles)
        - ✅ **Módulo 3: Interactividad** (1 clase disponible)
        - ✅ **Módulo 4: Aplicaciones** (2 clases disponibles)
        - ✅ **Módulo 5: Despliegue** (1 clase disponible)
        - ✅ **Bonus: Automatización** (1 clase disponible)
        - ✅ **Módulo 7: Evaluación** (1 clase disponible)
        
        ### 🎯 Cómo usar el curso:
        1. **Selecciona un módulo** en el menú lateral
        2. **Elige una clase** del módulo seleccionado
        3. **Interactúa** con las lecciones y ejemplos
        4. **Practica** modificando los parámetros
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
            st.markdown("🧠 Especialista en Python & Data Science")
            st.markdown("[🔗 GitHub](https://github.com/Denniels)")
            
    except Exception as e:
        st.error(f"❌ Error en la aplicación principal: {str(e)}")
        with st.expander("🔍 Detalles del error"):
            st.exception(e)

# ✅ Ejecutar aplicación
if __name__ == "__main__":
    main()
