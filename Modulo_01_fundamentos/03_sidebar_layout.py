import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Clase 3 - Sidebar layout", layout="wide")

st.title("🧭 Clase 3: Organización con Sidebar")
st.markdown("""
Streamlit te permite mover widgets al sidebar para mantener el área principal más limpia y enfocada en resultados.
""")

tab1, tab2, tab3 = st.tabs(["📐 Layout básico", "📊 Parámetros dinámicos", "🧠 Vista final"])

# ---- Celda 1: Sidebar con texto y slider ----
with tab1:
    st.subheader("📐 Layout básico con sidebar")
    st.sidebar.title("Controles del usuario")
    user_name = st.sidebar.text_input("Escribe tu nombre:")
    edad = st.sidebar.slider("Tu edad:", 18, 99, 25)

    if user_name:
        st.success(f"Bienvenido, {user_name} 👋 (Edad: {edad})")

    st.code("""
st.sidebar.title("Controles del usuario")
user_name = st.sidebar.text_input("Escribe tu nombre:")
edad = st.sidebar.slider("Tu edad:", 18, 99, 25)
""", language="python")

# ---- Celda 2: Parámetros para gráfico dinámico ----
with tab2:
    st.subheader("📊 Parámetros dinámicos (Ejemplo con gráfico)")

    import numpy as np
    import pandas as pd

    puntos = st.sidebar.slider("N° de puntos", 10, 500, 100)
    ruido = st.sidebar.slider("Nivel de ruido", 0.0, 1.0, 0.1)

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

# ---- Celda 3: Cierre reflexivo ----
with tab3:
    st.subheader("🧠 ¿Por qué usar sidebar?")
    st.markdown("""
- Separa la entrada de parámetros del contenido visual
- Mejora la experiencia de usuario
- Ideal para dashboards y simuladores

¡Ya puedes crear apps más limpias y profesionales!
    """)

