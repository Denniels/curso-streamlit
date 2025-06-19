import streamlit as st

st.set_page_config(page_title="Modulo 1 - Hola Streamlit", layout="centered")

st.title("🎈 Modulo 1: ¡Hola, Streamlit!")

st.markdown("""
Explora cada pestaña para ver cómo construir tu primera app con Streamlit.  
Esta lección interactiva te permite ejecutar el código, ver el resultado y aprender su sintaxis.
Es la una forma entretenida y didactica para que peudas practicar, aprender streramlit, divertirte y mejorar tus habilidades con Python
""")

# Crear pestañas para simular "celdas"
tab1, tab2, tab3, tab4 = st.tabs([
    "👋 Título y texto",
    "📝 Markdown enriquecido",
    "🎛️ Botón interactivo",
    "📘 Créditos"
])

# ---- Celda 1 ----
with tab1:
    st.subheader("👋 Título y subtítulo")
    st.title("¡Hola, Streamlit!")
    st.write("Este es tu primer texto interactivo.")

    st.code("""
st.title("¡Hola, Streamlit!")
st.write("Este es tu primer texto interactivo.")
""", language="python")

# ---- Celda 2 ----
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

# ---- Celda 3 ----
with tab3:
    st.subheader("🎛️ Botón interactivo")

    if st.button("Presiona para saludar"):
        st.success("¡Bienvenido al mundo Streamlit, soy tu Mentor Daniel Mardones! 🎉")

    st.code("""
if st.button("Presiona para saludar"):
    st.success("¡Bienvenido al mundo Streamlit, soy tu Mentor Daniel Mardones! 🎉")
""", language="python")

# ---- Celda 4 ----
with tab4:
    st.subheader("📘 Créditos")
    st.info("Curso creado por Daniel Mardones\nMentoría técnica en Python y DataScience 🤖✨")

    st.code("""
st.info("Curso creado por Daniel Mardones\\nMentoría técnica en Python y DataScience 🤖✨")
""", language="python")
