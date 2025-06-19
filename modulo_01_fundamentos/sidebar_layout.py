import streamlit as st
import pandas as pd
import numpy as np

def run():
    """Módulo Sidebar Layout con keys completamente estáticos."""
    
    with st.container():
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
            
            # ✅ Widgets con keys completamente estáticos
            with st.sidebar:
                st.markdown("### 👤 Perfil de Usuario")
                user_name = st.text_input("Escribe tu nombre:", key="sidebar_username_static")
                edad = st.slider("Tu edad:", 18, 99, 25, key="sidebar_edad_static")

            if user_name:
                st.success(f"Bienvenido, {user_name} 👋 (Edad: {edad})")

            st.code("""
# En el sidebar
user_name = st.sidebar.text_input("Escribe tu nombre:")
edad = st.sidebar.slider("Tu edad:", 18, 99, 25)

# En el main
if user_name:
    st.success(f"Bienvenido, {user_name} 👋 (Edad: {edad})")
""", language="python")

        with tab2:
            st.subheader("📊 Parámetros dinámicos (Ejemplo con gráfico)")

            # ✅ Widgets con keys completamente estáticos
            with st.sidebar:
                st.markdown("### ⚙️ Configuración del Gráfico")
                puntos = st.slider("N° de puntos", 10, 500, 100, key="sidebar_puntos_static")
                ruido = st.slider("Nivel de ruido", 0.0, 1.0, 0.1, key="sidebar_ruido_static")

            # Generar gráfico
            x = np.linspace(0, 10, puntos)
            y = np.sin(x) + np.random.normal(scale=ruido, size=puntos)
            df = pd.DataFrame({"x": x, "y": y})

            st.line_chart(df.set_index("x"))

            st.code("""
# En el sidebar
puntos = st.sidebar.slider("N° de puntos", 10, 500, 100)
ruido = st.sidebar.slider("Nivel de ruido", 0.0, 1.0, 0.1)

# Generar datos
x = np.linspace(0, 10, puntos)
y = np.sin(x) + np.random.normal(scale=ruido, size=puntos)
df = pd.DataFrame({"x": x, "y": y})

# Mostrar gráfico
st.line_chart(df.set_index("x"))
""", language="python")

        with tab3:
            st.subheader("🧠 ¿Por qué usar sidebar?")
            st.markdown("""
- Separa la entrada de parámetros del contenido visual  
- Mejora la experiencia de usuario  
- Ideal para dashboards y simuladores
            """)

            st.subheader("🧰 ¿Qué aprendiste en esta clase?")
            st.markdown("""
- A usar `st.sidebar` como contenedor alternativo para widgets  
- Cómo crear interfaces limpias e intuitivas  

¡Prepárate para dashboards más complejos y modulares!
            """)