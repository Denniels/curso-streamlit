import streamlit as st

def run():
    """Módulo Hello World con keys completamente estáticos."""
    
    # Contenedor principal fijo
    with st.container():
        st.title("🎈 Módulo 1: ¡Hola, Streamlit!")

        st.markdown("""
        Explora cada pestaña para ver cómo construir tu primera app con Streamlit.  
        Esta lección interactiva te permite ejecutar el código, ver el resultado y aprender su sintaxis.  
        Es una forma entretenida y didáctica para que puedas practicar, aprender Streamlit, divertirte y mejorar tus habilidades con Python.
        """)

        # ✅ Pestañas con keys estáticos únicos
        tab1, tab2, tab3, tab4 = st.tabs([
            "👋 Título y texto",
            "📝 Markdown enriquecido", 
            "🎛️ Botón interactivo",
            "📘 Créditos"
        ])

        with tab1:
            st.subheader("👋 Título y subtítulo")
            st.title("¡Hola, Streamlit!")
            st.write("Este es tu primer texto interactivo.")
            st.code("""
st.title("¡Hola, Streamlit!")
st.write("Este es tu primer texto interactivo.")
""", language="python")

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

        with tab3:
            st.subheader("🎛️ Botón interactivo")
            # ✅ Key completamente estático y único
            if st.button("Presiona para saludar", key="hello_world_saludar_btn_static"):
                st.success("¡Bienvenido al mundo Streamlit, desarrollado por Daniel Mardones! 🎉")
            st.code("""
if st.button("Presiona para saludar"):
    st.success("¡Bienvenido al mundo Streamlit, desarrollado por Daniel Mardones! 🎉")
""", language="python")

        with tab4:
            st.subheader("📘 Créditos")
            st.info("Curso creado por Daniel Mardones\nEspecialidad técnica en Python y Data Science 🤖✨")
            st.code("""
st.info("Curso creado por Daniel Mardones\\nEspecialidad técnica en Python y Data Science 🤖✨")
""", language="python")
