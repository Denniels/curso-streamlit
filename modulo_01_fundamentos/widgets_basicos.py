import streamlit as st

def run():
    """Módulo Widgets Básicos con keys completamente estáticos."""
    
    with st.container():
        st.title("🎛️ Clase 2: Interacción con Widgets")
        st.markdown("""
        En esta clase exploraremos botones, sliders, entradas de texto y selectores.  
        Las apps que construyas serán dinámicas e interactivas.
        """)
        
        # ✅ Pestañas con contenido estático
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔘 Botón", 
            "🎚️ Slider", 
            "🧾 Text Input", 
            "📋 Selectbox"
        ])
        
        with tab1:
            col1, col2 = st.columns([1, 2])
            with col1:
                # ✅ Key completamente estático
                clic = st.button("Haz clic aquí 👆", key="widgets_boton_principal_static")
            with col2:
                if clic:
                    st.success("¡Click recibido!")

            st.code("""
clic = st.button("Haz clic aquí 👆")
if clic:
    st.success("¡Click recibido!")
""", language="python")

        with tab2:
            # ✅ Key completamente estático
            edad = st.slider("Tu edad (años)", 0, 100, 25, key="widgets_edad_slider_static")
            st.write(f"Tienes {edad} años.")

            st.code("""
edad = st.slider("Tu edad (años)", 0, 100, 25)
st.write(f"Tienes {edad} años.")
""", language="python")

        with tab3:
            # ✅ Key completamente estático
            nombre = st.text_input("¿Cómo te llamas?", key="widgets_nombre_input_static")
            if nombre:
                st.success(f"Hola, {nombre} 👋")

            st.code("""
nombre = st.text_input("¿Cómo te llamas?")
if nombre:
    st.success(f"Hola, {nombre} 👋")
""", language="python")

        with tab4:
            # ✅ Key completamente estático
            lenguaje = st.selectbox("Tu lenguaje favorito 💻", 
                                  ["Python", "SQL", "R", "JavaScript", "Otro"], 
                                  key="widgets_lenguaje_select_static")
            st.info(f"Elegiste: **{lenguaje}**")

            st.code("""
lenguaje = st.selectbox("Tu lenguaje favorito 💻", 
                       ["Python", "SQL", "R", "JavaScript", "Otro"])
st.info(f"Elegiste: {lenguaje}")
""", language="python")
