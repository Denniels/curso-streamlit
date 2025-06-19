"""
Versión simplificada para debug en vivo
"""

import streamlit as st
import sys
import os

# Agregar el directorio de módulos al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modulo_01_fundamentos'))

# Configuración de página
st.set_page_config(
    page_title="Debug Navegación",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Debug de Navegación - Versión Simplificada")

# Importar módulos
try:
    import hello_world
    import widgets_basicos
    import sidebar_layout
    st.success("✅ Todos los módulos importados correctamente")
except ImportError as e:
    st.error(f"❌ Error importando módulos: {e}")
    st.stop()

# Sidebar navegación
with st.sidebar:
    st.markdown("# 🧭 Navegación Debug")
    
    selected_module = st.selectbox(
        "Módulo",
        ["Módulo 1: Fundamentos"],
        key="debug_module"
    )
    
    selected_class = st.radio(
        "Clase",
        [
            "Clase 1: Hello, Streamlit",
            "Clase 2: Widgets básicos", 
            "Clase 3: Sidebar y layout"
        ],
        key="debug_class"
    )

# Mostrar información de debug
st.markdown("### 🔍 Información de Debug")
col1, col2 = st.columns(2)

with col1:
    st.metric("Módulo seleccionado", selected_module)
    st.metric("Clase seleccionada", selected_class)

with col2:
    st.write("**Estado de session_state:**")
    st.json({
        "debug_module": st.session_state.get("debug_module", "No definido"),
        "debug_class": st.session_state.get("debug_class", "No definido")
    })

# Renderizar contenido basado en selección
st.markdown("### 📝 Contenido Renderizado")

# Mapeo de clases a módulos
class_mapping = {
    "Clase 1: Hello, Streamlit": hello_world,
    "Clase 2: Widgets básicos": widgets_basicos,
    "Clase 3: Sidebar y layout": sidebar_layout
}

if selected_class in class_mapping:
    try:
        st.info(f"🎯 Renderizando: {selected_class}")
        
        # Contenedor para el módulo
        with st.container():
            current_module = class_mapping[selected_class]
            st.write(f"**Módulo a ejecutar:** {current_module.__name__}")
            
            # Separador visual
            st.divider()
            
            # Ejecutar el módulo
            current_module.run()
            
    except Exception as e:
        st.error(f"❌ Error ejecutando módulo: {e}")
        st.exception(e)
else:
    st.warning("⚠️ Clase no encontrada en mapeo")

# Footer debug
st.markdown("---")
st.markdown("**🔧 Debug Info:**")
st.write(f"- Módulos disponibles: {list(class_mapping.keys())}")
st.write(f"- Clase actual: {selected_class}")
st.write(f"- Módulo mapeado: {class_mapping.get(selected_class, 'No encontrado')}")
