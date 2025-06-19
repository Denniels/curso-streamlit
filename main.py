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

# Cargar archivo correspondiente (esto se irá actualizando)
if modulo == "Módulo 1: Fundamentos":
    exec(open("Modulo_01_fundamentos/01_hello_world.py", encoding="utf-8").read())

# El resto se irá añadiendo a medida que avancemos
st.sidebar.markdown("---")
st.sidebar.markdown("Creado por **Daniel Mardones** 🧠")
st.sidebar.markdown("Curso interactivo de Streamlit")
st.sidebar.markdown("Daniel Mardones - [GitHub](https://github.com/Denniels")