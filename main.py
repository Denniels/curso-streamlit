import streamlit as st
import os

st.set_page_config(page_title="Curso Streamlit", layout="wide")

st.title("Curso completo he interactivo de streamlit")
st.markdown("""
Bienvenido al curso interactivo de Streamlit. Aquí aprenderás a dominar Streamlit desde lo mas basico asta aplicaiones avanzadas.
Puedes usar el menu lateral para explorar los diferetnes modulos del curso.
""")

# Menu lateral para seleccion de modulos
modulo = st.sidebar.selectbox("Selecciona un módulo", (
    "Módulo 1: Fundamentos",
    "Módulo 2: Visualización de Datos",
    "Módulo 3: Interactividad Avanzada",
    "Módulo 4: Aplicaciones Especializadas",
    "Módulo 5: Despliegue y Optimización",
    "Bonus: Automatización CI/CD"
))

# Submenús por módulo
if modulo == "Módulo 1: Fundamentos":
    clase = st.sidebar.radio("Selecciona la clase:", [
        "Clase 1: Hello, Streamlit",
        "Clase 2: Widgets básicos",
        "Clase 3: Sidebar y layout"
    ])
    
    if clase == "Clase 1: Hello, Streamlit":
        exec(open("modulo_01_fundamentos/01_hello_world.py", encoding="utf-8").read())
    elif clase == "Clase 2: Widgets básicos":
        exec(open("modulo_01_fundamentos/02_widgets_basicos.py", encoding="utf-8").read())
    elif clase == "Clase 3: Sidebar y layout":
        exec(open("modulo_01_fundamentos/03_sidebar_layout.py", encoding="utf-8").read())

# Aquí dejaremos los demás módulos en blanco hasta que los construyamos
else:
    st.warning("🎓 Este módulo aún está en construcción. Pronto estará disponible.")



# El resto se irá añadiendo a medida que avancemos
st.sidebar.markdown("---")
st.sidebar.markdown("Creado por **Daniel Mardones** 🧠")
st.sidebar.markdown("Curso interactivo de Streamlit")
st.sidebar.markdown("Daniel Mardones - [GitHub](https://github.com/Denniels")