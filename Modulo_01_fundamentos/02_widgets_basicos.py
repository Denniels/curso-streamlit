import streamlit as st

st.set_page_config(page_title="Clase 2 - Widgets básicos", layout="centered")

st.title("🎛️ Clase 2: Interacción con Widgets")
st.markdown("""
Los widgets permiten que los usuarios interactúen con tu app.  
En esta clase exploraremos botones, sliders, cajas de texto y menús desplegables.
Tus apps serán más dinámicas y personalizadas,
permitiendo a los usuarios ingresar datos he interactuar de foram agil con tu app.
""")

tab1, tab2, tab3, tab4 = st.tabs([
    "🔘 Botón",
    "🎚️ Slider",
    "🧾 Text Input",
    "📋 Selectbox"
])

# ---- Botón ----
with tab1:
    st.subheader("🔘 Botón interactivo")
    if st.button("Haz clic aquí"):
        st.success("¡Click recibido!")

    st.code("""
if st.button("Haz clic aquí"):
    st.success("¡Click recibido!")
""", language="python")

# ---- Slider ----
with tab2:
    st.subheader("🎚️ Deslizador de rango numérico")
    edad = st.slider("¿Cuál es tu edad?", 0, 100, 25)
    st.write(f"Tienes {edad} años.")

    st.code("""
edad = st.slider("¿Cuál es tu edad?", 0, 100, 25)
st.write(f"Tienes {edad} años.")
""", language="python")

# ---- Text Input ----
with tab3:
    st.subheader("🧾 Entrada de texto")
    nombre = st.text_input("Escribe tu nombre")
    if nombre:
        st.success(f"Hola, {nombre} 👋")

    st.code("""
nombre = st.text_input("Escribe tu nombre")
if nombre:
    st.success(f"Hola, {nombre} 👋")
""", language="python")

# ---- Selectbox ----
with tab4:
    st.subheader("📋 Selectbox")
    lenguaje = st.selectbox("Lenguaje favorito", ["Python", "SQL", "R", "kotlin", "javascript"])
    st.write(f"Has seleccionado: {lenguaje}")

    st.code("""
lenguaje = st.selectbox("Lenguaje favorito", ["Python", "SQL", "R", "kotlin", "javascript"])
st.write(f"Has seleccionado: {lenguaje}")
""", language="python")
