import streamlit as st
import json
import time
import random
import pandas as pd
import plotly.express as px
from datetime import datetime
from typing import Dict, List, Any

def run():
    """Módulo de Evaluación Interactiva - Tests y Ejercicios de Streamlit."""
    
    with st.container():
        st.title("🎯 Módulo 7: Evaluación Interactiva")
        st.markdown("""
        Pon a prueba tus conocimientos de Streamlit con preguntas interactivas,
        ejercicios de código y evaluaciones prácticas.
        """)
        
        # Pestañas del módulo
        tab1, tab2, tab3, tab4 = st.tabs([
            "📝 Quiz Teórico",
            "💻 Ejercicios de Código", 
            "🏗️ Proyectos Guiados",
            "📊 Resultados"
        ])
        
        with tab1:
            render_quiz_teorico()
        
        with tab2:
            render_ejercicios_codigo()
        
        with tab3:
            render_proyectos_guiados()
        
        with tab4:
            render_resultados()

def render_quiz_teorico():
    """Renderiza el quiz teórico con preguntas de opción múltiple."""
    st.subheader("📝 Quiz Teórico de Streamlit")
    
    st.markdown("""
    Responde las siguientes preguntas para evaluar tu comprensión de los conceptos de Streamlit.
    """)
    
    # Inicializar respuestas en session state
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    
    # Base de preguntas del quiz
    preguntas = [
        {
            "id": "q1",
            "pregunta": "¿Cuál es la función principal para crear un botón en Streamlit?",
            "opciones": ["st.button()", "st.create_button()", "st.make_button()", "st.btn()"],
            "respuesta_correcta": 0,
            "explicacion": "st.button() es la función estándar para crear botones en Streamlit."
        },
        {
            "id": "q2", 
            "pregunta": "¿Qué función permite mostrar DataFrames de pandas de manera interactiva?",
            "opciones": ["st.table()", "st.dataframe()", "st.data()", "st.show_df()"],
            "respuesta_correcta": 1,
            "explicacion": "st.dataframe() permite mostrar DataFrames con funciones interactivas como ordenar y filtrar."
        },
        {
            "id": "q3",
            "pregunta": "¿Cuál es la diferencia entre st.cache_data y st.cache_resource?",
            "opciones": [
                "No hay diferencia, son sinónimos",
                "cache_data para datos, cache_resource para objetos no serializables",
                "cache_resource es más rápido",
                "cache_data solo funciona con números"
            ],
            "respuesta_correcta": 1,
            "explicacion": "st.cache_data se usa para datos serializables, mientras que st.cache_resource es para objetos como conexiones de DB."
        },
        {
            "id": "q4",
            "pregunta": "¿Qué archivo se usa para configurar secretos localmente?",
            "opciones": [".env", "secrets.toml", ".streamlit/secrets.toml", "config.py"],
            "respuesta_correcta": 2,
            "explicacion": "Los secretos locales se guardan en .streamlit/secrets.toml"
        },
        {
            "id": "q5",
            "pregunta": "¿Cuál es la función correcta para crear un slider?",
            "opciones": ["st.slide()", "st.slider()", "st.range()", "st.input_slider()"],
            "respuesta_correcta": 1,
            "explicacion": "st.slider() es la función para crear controles deslizantes."
        },
        {
            "id": "q6",
            "pregunta": "¿Qué permite st.session_state?",
            "opciones": [
                "Configurar la sesión del usuario",
                "Mantener variables entre reruns",
                "Conectar con bases de datos",
                "Configurar el tema visual"
            ],
            "respuesta_correcta": 1,
            "explicacion": "st.session_state permite mantener variables persistentes entre reruns de la aplicación."
        },
        {
            "id": "q7",
            "pregunta": "¿Cuál es la forma correcta de crear columnas en Streamlit?",
            "opciones": [
                "st.columns([1, 2, 1])",
                "st.create_columns(3)",
                "st.layout.columns(3)",
                "st.grid(3)"
            ],
            "respuesta_correcta": 0,
            "explicacion": "st.columns() acepta una lista con las proporciones relativas de cada columna."
        },
        {
            "id": "q8",
            "pregunta": "¿Qué función se usa para mostrar métricas con delta?",
            "opciones": ["st.kpi()", "st.metric()", "st.indicator()", "st.stats()"],
            "respuesta_correcta": 1,
            "explicacion": "st.metric() muestra métricas con valores principales y deltas opcionales."
        }
    ]
    
    # Mostrar preguntas
    with st.form("quiz_form"):
        st.markdown("### 🎯 Preguntas del Quiz")
        
        for i, pregunta in enumerate(preguntas):
            st.markdown(f"**{i+1}. {pregunta['pregunta']}**")
            
            respuesta = st.radio(
                "Selecciona tu respuesta:",
                pregunta['opciones'],
                key=f"q_{pregunta['id']}",
                index=None
            )            
            if respuesta:
                st.session_state.quiz_answers[pregunta['id']] = {
                    'respuesta': pregunta['opciones'].index(respuesta),
                    'correcta': pregunta['opciones'].index(respuesta) == pregunta['respuesta_correcta']
                }
            
            st.markdown("---")
        
        submitted = st.form_submit_button("📊 Evaluar Quiz", type="primary")
        
        if submitted:
            evaluar_quiz(preguntas)
    
    # Botón para reiniciar fuera del formulario
    if st.session_state.quiz_answers:
        if st.button("🔄 Reiniciar Quiz"):
            reiniciar_quiz()

def evaluar_quiz(preguntas):
    """Evalúa las respuestas del quiz y muestra resultados."""
    if not st.session_state.quiz_answers:
        st.warning("⚠️ Debes responder al menos una pregunta.")
        return
    
    # Calcular resultados
    total_preguntas = len(preguntas)
    respuestas_correctas = sum(1 for answer in st.session_state.quiz_answers.values() if answer['correcta'])
    porcentaje = (respuestas_correctas / total_preguntas) * 100
    
    # Mostrar resultados generales
    st.markdown("### 📊 Resultados del Quiz")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Preguntas Correctas", f"{respuestas_correctas}/{total_preguntas}")
    
    with col2:
        st.metric("Porcentaje", f"{porcentaje:.1f}%")
    
    with col3:
        if porcentaje >= 80:
            st.success("🏆 ¡Excelente!")
        elif porcentaje >= 60:
            st.info("👍 Bien hecho")
        else:
            st.warning("📚 Sigue estudiando")
    
    # Mostrar barra de progreso
    st.progress(porcentaje / 100)
    
    # Detalles por pregunta
    st.markdown("### 📝 Detalles por Pregunta")
    
    for i, pregunta in enumerate(preguntas):
        pregunta_id = pregunta['id']
        
        if pregunta_id in st.session_state.quiz_answers:
            user_answer = st.session_state.quiz_answers[pregunta_id]
            es_correcta = user_answer['correcta']
            
            with st.expander(f"Pregunta {i+1}: {'✅' if es_correcta else '❌'} {pregunta['pregunta'][:50]}..."):
                st.markdown(f"**Pregunta:** {pregunta['pregunta']}")
                
                respuesta_usuario = pregunta['opciones'][user_answer['respuesta']]
                respuesta_correcta = pregunta['opciones'][pregunta['respuesta_correcta']]
                
                if es_correcta:
                    st.success(f"✅ Correcto: {respuesta_usuario}")
                else:
                    st.error(f"❌ Tu respuesta: {respuesta_usuario}")
                    st.info(f"✅ Respuesta correcta: {respuesta_correcta}")
                
                st.markdown(f"**Explicación:** {pregunta['explicacion']}")
      # Guardar resultado en historial
    if 'quiz_history' not in st.session_state:
        st.session_state.quiz_history = []
    
    resultado = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_preguntas': total_preguntas,
        'correctas': respuestas_correctas,
        'porcentaje': porcentaje
    }
    st.session_state.quiz_history.append(resultado)
    
    # El botón para reiniciar debe estar fuera del formulario
    # Se mueve fuera de la función evaluar_quiz

def reiniciar_quiz():
    """Función para reiniciar el quiz."""
    st.session_state.quiz_answers = {}
    st.rerun()

def render_ejercicios_codigo():
    """Renderiza ejercicios prácticos de código."""
    st.subheader("💻 Ejercicios de Código")
    
    st.markdown("""
    Resuelve ejercicios prácticos escribiendo código de Streamlit.
    """)
    
    # Seleccionar ejercicio
    ejercicios = [
        "Básico: Crear una calculadora simple",
        "Intermedio: Dashboard de datos",
        "Avanzado: Sistema de login",
        "Desafío: Análisis de sentimientos"
    ]
    
    ejercicio_seleccionado = st.selectbox(
        "Selecciona un ejercicio:",
        ejercicios,
        key="ejercicio_selector"
    )
    
    if ejercicio_seleccionado:
        nivel = ejercicio_seleccionado.split(":")[0]
        titulo = ejercicio_seleccionado.split(":")[1].strip()
        
        st.markdown(f"### {nivel}: {titulo}")
        
        if "Básico" in ejercicio_seleccionado:
            render_ejercicio_calculadora()
        elif "Intermedio" in ejercicio_seleccionado:
            render_ejercicio_dashboard()
        elif "Avanzado" in ejercicio_seleccionado:
            render_ejercicio_login()
        elif "Desafío" in ejercicio_seleccionado:
            render_ejercicio_sentimientos()

def render_ejercicio_calculadora():
    """Ejercicio básico: Crear una calculadora."""
    st.markdown("""
    **🎯 Objetivo:** Crear una calculadora simple con Streamlit
    
    **Requisitos:**
    1. Dos inputs numéricos para los operandos
    2. Un selectbox para elegir la operación (+, -, *, /)
    3. Un botón para calcular
    4. Mostrar el resultado
    5. Manejar errores (división por cero)
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Tu Código")
        
        codigo_usuario = st.text_area(
            "Escribe tu código aquí:",
            placeholder="""import streamlit as st

st.title("🧮 Calculadora")

# Tu código aquí...
""",
            height=300,
            key="calc_code"
        )
        
        if st.button("▶️ Ejecutar Código", key="run_calc"):
            ejecutar_codigo_seguro(codigo_usuario, "calculadora")
    
    with col2:
        st.markdown("### 💡 Solución Sugerida")
        
        with st.expander("Ver solución completa"):
            st.code("""
import streamlit as st

st.title("🧮 Calculadora")

# Inputs
col1, col2 = st.columns(2)

with col1:
    num1 = st.number_input("Primer número", value=0.0)

with col2:
    num2 = st.number_input("Segundo número", value=0.0)

# Operación
operacion = st.selectbox(
    "Selecciona la operación:",
    ["+", "-", "*", "/"]
)

# Botón calcular
if st.button("🔢 Calcular"):
    try:
        if operacion == "+":
            resultado = num1 + num2
        elif operacion == "-":
            resultado = num1 - num2
        elif operacion == "*":
            resultado = num1 * num2
        elif operacion == "/":
            if num2 == 0:
                st.error("❌ Error: División por cero")
            else:
                resultado = num1 / num2
        
        if 'resultado' in locals():
            st.success(f"✅ Resultado: {resultado}")
            
    except Exception as e:
        st.error(f"❌ Error: {e}")
            """, language="python")
        
        # Demo funcional
        st.markdown("### 🎯 Demo Funcional")
        
        demo_col1, demo_col2 = st.columns(2)
        
        with demo_col1:
            demo_num1 = st.number_input("Primer número", value=0.0, key="demo_num1")
        
        with demo_col2:
            demo_num2 = st.number_input("Segundo número", value=0.0, key="demo_num2")
        
        demo_op = st.selectbox("Operación:", ["+", "-", "*", "/"], key="demo_op")
        
        if st.button("🔢 Calcular Demo", key="demo_calc"):
            try:
                if demo_op == "+":
                    resultado = demo_num1 + demo_num2
                elif demo_op == "-":
                    resultado = demo_num1 - demo_num2
                elif demo_op == "*":
                    resultado = demo_num1 * demo_num2
                elif demo_op == "/":
                    if demo_num2 == 0:
                        st.error("❌ Error: División por cero")
                    else:
                        resultado = demo_num1 / demo_num2
                
                if 'resultado' in locals():
                    st.success(f"✅ Resultado: {resultado}")
                    
            except Exception as e:
                st.error(f"❌ Error: {e}")

def render_ejercicio_dashboard():
    """Ejercicio intermedio: Dashboard de datos."""
    st.markdown("""
    **🎯 Objetivo:** Crear un dashboard interactivo con datos
    
    **Requisitos:**
    1. Generar datos de muestra (ventas por mes)
    2. Mostrar métricas principales (total, promedio, máximo)
    3. Crear un gráfico de líneas
    4. Agregar filtros interactivos
    5. Usar st.columns para layout
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Tu Código")
        
        codigo_dashboard = st.text_area(
            "Escribe tu código aquí:",
            placeholder="""import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Dashboard de Ventas")

# Tu código aquí...
""",
            height=400,
            key="dashboard_code"
        )
        
        if st.button("▶️ Ejecutar Dashboard", key="run_dashboard"):
            ejecutar_codigo_seguro(codigo_dashboard, "dashboard")
    
    with col2:
        st.markdown("### 💡 Solución Sugerida")
        
        with st.expander("Ver solución completa"):
            st.code("""
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

st.title("📊 Dashboard de Ventas")

# Generar datos de muestra
@st.cache_data
def generar_datos():
    fechas = pd.date_range(
        start=datetime.now() - timedelta(days=365),
        end=datetime.now(),
        freq='D'
    )
    
    datos = {
        'fecha': fechas,
        'ventas': np.random.normal(1000, 200, len(fechas)),
        'productos': np.random.choice(['A', 'B', 'C'], len(fechas)),
        'region': np.random.choice(['Norte', 'Sur', 'Centro'], len(fechas))
    }
    
    return pd.DataFrame(datos)

df = generar_datos()

# Filtros
col1, col2 = st.columns(2)

with col1:
    productos_seleccionados = st.multiselect(
        "Productos:", 
        df['productos'].unique(),
        default=df['productos'].unique()
    )

with col2:
    regiones_seleccionadas = st.multiselect(
        "Regiones:",
        df['region'].unique(),
        default=df['region'].unique()
    )

# Filtrar datos
df_filtrado = df[
    (df['productos'].isin(productos_seleccionados)) &
    (df['region'].isin(regiones_seleccionadas))
]

# Métricas
col1, col2, col3 = st.columns(3)

with col1:
    total_ventas = df_filtrado['ventas'].sum()
    st.metric("Total Ventas", f"${total_ventas:,.0f}")

with col2:
    promedio_ventas = df_filtrado['ventas'].mean()
    st.metric("Promedio Diario", f"${promedio_ventas:,.0f}")

with col3:
    max_ventas = df_filtrado['ventas'].max()
    st.metric("Máximo Día", f"${max_ventas:,.0f}")

# Gráficos
fig_lineas = px.line(
    df_filtrado, 
    x='fecha', 
    y='ventas',
    title='Evolución de Ventas'
)
st.plotly_chart(fig_lineas, use_container_width=True)

# Gráfico por categorías
ventas_por_producto = df_filtrado.groupby('productos')['ventas'].sum()
fig_barras = px.bar(
    x=ventas_por_producto.index,
    y=ventas_por_producto.values,
    title='Ventas por Producto'
)
st.plotly_chart(fig_barras, use_container_width=True)
            """, language="python")

def render_ejercicio_login():
    """Ejercicio avanzado: Sistema de login."""
    st.markdown("""
    **🎯 Objetivo:** Crear un sistema de autenticación básico
    
    **Requisitos:**
    1. Formulario de login con usuario y contraseña
    2. Validación de credenciales
    3. Mantener estado de sesión
    4. Área protegida para usuarios autenticados
    5. Opción de logout
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Tu Código")
        
        codigo_login = st.text_area(
            "Escribe tu código aquí:",
            placeholder="""import streamlit as st

st.title("🔐 Sistema de Login")

# Tu código aquí...
""",
            height=400,
            key="login_code"
        )
        
        if st.button("▶️ Ejecutar Login System", key="run_login"):
            ejecutar_codigo_seguro(codigo_login, "login")
    
    with col2:
        st.markdown("### 💡 Demo Funcional")
        
        # Demo sistema de login
        demo_login_system()

def demo_login_system():
    """Demo funcional del sistema de login."""
    # Usuarios de ejemplo
    USUARIOS = {
        "admin": "123456",
        "user": "password",
        "demo": "demo"
    }
    
    # Inicializar estado de sesión
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
    
    if not st.session_state.logged_in:
        # Formulario de login
        st.markdown("### 🔑 Iniciar Sesión")
        
        with st.form("login_form"):
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            
            login_button = st.form_submit_button("🚀 Entrar")
            
            if login_button:
                if username in USUARIOS and USUARIOS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"✅ Bienvenido, {username}!")
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas")
        
        # Ayuda para el demo
        st.info("""
        **Usuarios de prueba:**
        - admin / 123456
        - user / password
        - demo / demo
        """)
    
    else:
        # Área protegida
        st.markdown(f"### 👋 Bienvenido, {st.session_state.username}!")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.success("🔓 Acceso autorizado al área protegida")
        
        with col2:
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.rerun()
        
        # Contenido protegido
        st.markdown("---")
        st.markdown("### 📊 Panel de Control")
        
        tab1, tab2, tab3 = st.tabs(["📈 Métricas", "👥 Usuarios", "⚙️ Configuración"])
        
        with tab1:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Usuarios Activos", "1,234", delta="12%")
            with col2:
                st.metric("Sesiones", "5,678", delta="-3%")
            with col3:
                st.metric("Ingresos", "$89,012", delta="8%")
        
        with tab2:
            st.markdown("Lista de usuarios registrados:")
            user_data = {
                'Usuario': ['admin', 'user', 'demo'],
                'Último Login': ['2024-01-15', '2024-01-14', '2024-01-13'],
                'Estado': ['Activo', 'Activo', 'Inactivo']
            }
            st.dataframe(user_data)
        
        with tab3:
            st.markdown("Configuraciones del sistema:")
            st.checkbox("Modo debug")
            st.selectbox("Tema", ["Claro", "Oscuro"])
            st.slider("Timeout de sesión (min)", 5, 60, 30)

def render_ejercicio_sentimientos():
    """Ejercicio desafío: Análisis de sentimientos."""
    st.markdown("""
    **🎯 Objetivo:** Crear un analizador de sentimientos de texto
    
    **Requisitos:**
    1. Input de texto para analizar
    2. Análisis de sentimiento (positivo/negativo/neutral)
    3. Mostrar confianza del análisis
    4. Historial de análisis
    5. Visualización de resultados
    """)
    
    st.info("💡 Para este ejercicio, usaremos un análisis simple basado en palabras clave.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Analizador de Sentimientos")
        
        # Input de texto
        texto_analizar = st.text_area(
            "Ingresa el texto a analizar:",
            placeholder="Escribe aquí el texto que quieres analizar...",
            height=150
        )
        
        if st.button("🔍 Analizar Sentimiento", key="analyze_sentiment"):
            if texto_analizar.strip():
                resultado = analizar_sentimiento_simple(texto_analizar)
                mostrar_resultado_sentimiento(resultado, texto_analizar)
            else:
                st.warning("⚠️ Por favor ingresa algún texto para analizar.")
    
    with col2:
        st.markdown("### 📊 Historial de Análisis")
        
        if 'sentiment_history' not in st.session_state:
            st.session_state.sentiment_history = []
        
        if st.session_state.sentiment_history:
            for i, analisis in enumerate(reversed(st.session_state.sentiment_history[-5:])):
                with st.expander(f"Análisis {len(st.session_state.sentiment_history) - i}"):
                    st.write(f"**Texto:** {analisis['texto'][:50]}...")
                    
                    color = {
                        'Positivo': 'green',
                        'Negativo': 'red',
                        'Neutral': 'gray'
                    }[analisis['sentimiento']]
                    
                    st.markdown(f"**Sentimiento:** :{color}[{analisis['sentimiento']}]")
                    st.write(f"**Confianza:** {analisis['confianza']:.1%}")
                    st.write(f"**Fecha:** {analisis['timestamp']}")
        else:
            st.info("No hay análisis previos.")
        
        if st.button("🧹 Limpiar Historial"):
            st.session_state.sentiment_history = []
            st.rerun()

def analizar_sentimiento_simple(texto):
    """Análisis de sentimiento simple basado en palabras clave."""
    # Palabras positivas y negativas
    palabras_positivas = [
        'bueno', 'excelente', 'fantástico', 'increíble', 'perfecto',
        'feliz', 'contento', 'alegre', 'satisfecho', 'genial',
        'maravilloso', 'brillante', 'estupendo', 'magnífico'
    ]
    
    palabras_negativas = [
        'malo', 'terrible', 'horrible', 'pésimo', 'desastre',
        'triste', 'molesto', 'enojado', 'furioso', 'decepcionado',
        'frustrante', 'aburrido', 'difícil', 'complicado'
    ]
    
    texto_lower = texto.lower()
    
    # Contar palabras positivas y negativas
    positivas_encontradas = sum(1 for palabra in palabras_positivas if palabra in texto_lower)
    negativas_encontradas = sum(1 for palabra in palabras_negativas if palabra in texto_lower)
    
    # Determinar sentimiento
    if positivas_encontradas > negativas_encontradas:
        sentimiento = 'Positivo'
        confianza = min(0.9, 0.5 + (positivas_encontradas - negativas_encontradas) * 0.1)
    elif negativas_encontradas > positivas_encontradas:
        sentimiento = 'Negativo'
        confianza = min(0.9, 0.5 + (negativas_encontradas - positivas_encontradas) * 0.1)
    else:
        sentimiento = 'Neutral'
        confianza = 0.5
    
    return {
        'sentimiento': sentimiento,
        'confianza': confianza,
        'palabras_positivas': positivas_encontradas,
        'palabras_negativas': negativas_encontradas
    }

def mostrar_resultado_sentimiento(resultado, texto):
    """Muestra los resultados del análisis de sentimiento."""
    st.markdown("### 📊 Resultado del Análisis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        color = {
            'Positivo': 'green',
            'Negativo': 'red',
            'Neutral': 'gray'
        }[resultado['sentimiento']]
        
        st.markdown(f"**Sentimiento:** :{color}[{resultado['sentimiento']}]")
    
    with col2:
        st.metric("Confianza", f"{resultado['confianza']:.1%}")
    
    with col3:
        palabras_total = resultado['palabras_positivas'] + resultado['palabras_negativas']
        st.metric("Palabras Clave", palabras_total)
    
    # Barra de progreso para confianza
    st.progress(resultado['confianza'])
    
    # Detalles
    with st.expander("Ver detalles del análisis"):
        st.write(f"**Palabras positivas encontradas:** {resultado['palabras_positivas']}")
        st.write(f"**Palabras negativas encontradas:** {resultado['palabras_negativas']}")
        st.write(f"**Longitud del texto:** {len(texto)} caracteres")
    
    # Guardar en historial
    analisis = {
        'texto': texto,
        'sentimiento': resultado['sentimiento'],
        'confianza': resultado['confianza'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    if 'sentiment_history' not in st.session_state:
        st.session_state.sentiment_history = []
    
    st.session_state.sentiment_history.append(analisis)

def ejecutar_codigo_seguro(codigo, tipo):
    """Ejecuta código de usuario de forma segura (simulado)."""
    st.markdown("### 🔧 Resultado de la Ejecución")
    
    # Simulación de ejecución segura
    if not codigo.strip():
        st.warning("⚠️ No hay código para ejecutar.")
        return
    
    try:
        # Verificaciones básicas de seguridad
        palabras_prohibidas = ['import os', 'import sys', 'exec(', 'eval(', '__import__']
        
        for palabra in palabras_prohibidas:
            if palabra in codigo:
                st.error(f"❌ Código no permitido: uso de '{palabra}'")
                return
        
        # Simular resultado basado en el tipo
        if tipo == "calculadora":
            if "st.title" in codigo and "st.number_input" in codigo and "st.button" in codigo:
                st.success("✅ ¡Excelente! Tu calculadora tiene todos los elementos básicos.")
                if "try:" in codigo and "except" in codigo:
                    st.success("🏆 ¡Bonus! Incluiste manejo de errores.")
            else:
                st.warning("⚠️ Tu código parece incompleto. Verifica que incluyas todos los elementos requeridos.")
        
        elif tipo == "dashboard":
            if "st.metric" in codigo and "plotly" in codigo and "st.columns" in codigo:
                st.success("✅ ¡Perfecto! Tu dashboard incluye métricas, gráficos y layout en columnas.")
                if "@st.cache_data" in codigo:
                    st.success("🏆 ¡Bonus! Usaste cache para optimizar performance.")
            else:
                st.warning("⚠️ Verifica que incluyas métricas, gráficos y columnas.")
        
        elif tipo == "login":
            if "st.session_state" in codigo and "st.form" in codigo:
                st.success("✅ ¡Genial! Tu sistema usa session state y formularios.")
                if "st.rerun" in codigo:
                    st.success("🏆 ¡Bonus! Manejas correctamente los reruns.")
            else:
                st.warning("⚠️ Asegúrate de usar session_state para mantener el estado de login.")
        
        # Mostrar fragmento del código
        st.code(codigo[:200] + "..." if len(codigo) > 200 else codigo, language="python")
        
    except Exception as e:
        st.error(f"❌ Error en el código: {e}")

def render_proyectos_guiados():
    """Renderiza proyectos guiados paso a paso."""
    st.subheader("🏗️ Proyectos Guiados")
    
    st.markdown("""
    Sigue proyectos paso a paso para construir aplicaciones completas.
    """)
    
    proyectos = [
        "📈 Analizador de Stocks",
        "🎮 Juego de Trivia",
        "📝 Generador de Reportes",
        "🤖 Chatbot Simple"
    ]
    
    proyecto_seleccionado = st.selectbox(
        "Selecciona un proyecto:",
        proyectos,
        key="proyecto_selector"
    )
    
    if "Analizador de Stocks" in proyecto_seleccionado:
        render_proyecto_stocks()
    elif "Juego de Trivia" in proyecto_seleccionado:
        render_proyecto_trivia()
    elif "Generador de Reportes" in proyecto_seleccionado:
        render_proyecto_reportes()
    elif "Chatbot Simple" in proyecto_seleccionado:
        render_proyecto_chatbot()

def render_proyecto_stocks():
    """Proyecto guiado: Analizador de Stocks."""
    st.markdown("### 📈 Proyecto: Analizador de Stocks")
    
    steps = [
        "Configuración inicial y imports",
        "Interface de usuario y inputs",
        "Obtención de datos (simulados)",
        "Cálculo de métricas financieras",
        "Visualización de gráficos",
        "Dashboard final"
    ]
    
    # Selector de paso
    paso_actual = st.selectbox("Paso actual:", steps, key="stock_step")
    
    if "Configuración inicial" in paso_actual:
        st.markdown("""
        **Paso 1: Configuración inicial**
        
        Primero, configuramos los imports necesarios y la estructura básica:
        """)
        
        st.code("""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Analizador de Stocks",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Analizador de Stocks")
st.markdown("Analiza el rendimiento de acciones con métricas en tiempo real.")
        """, language="python")
        
    elif "Interface de usuario" in paso_actual:
        st.markdown("""
        **Paso 2: Interface de usuario**
        
        Creamos los controles para que el usuario seleccione las acciones:
        """)
        
        st.code("""
# Sidebar para controles
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Selector de acción
    simbolos = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
    simbolo_seleccionado = st.selectbox("Símbolo de la acción:", simbolos)
    
    # Rango de fechas
    fecha_inicio = st.date_input(
        "Fecha de inicio:",
        value=datetime.now() - timedelta(days=365)
    )
    
    fecha_fin = st.date_input(
        "Fecha de fin:",
        value=datetime.now()
    )
    
    # Indicadores técnicos
    mostrar_media_movil = st.checkbox("Media móvil (20 días)", value=True)
    mostrar_bandas_bollinger = st.checkbox("Bandas de Bollinger")
        """, language="python")
    
    # Y así sucesivamente para cada paso...

def render_proyecto_trivia():
    """Proyecto guiado: Juego de Trivia."""
    st.markdown("### 🎮 Proyecto: Juego de Trivia")
    
    st.info("Este proyecto te guiará paso a paso para crear un juego de trivia completo.")
    
    # Demo del juego de trivia
    if 'trivia_score' not in st.session_state:
        st.session_state.trivia_score = 0
        st.session_state.trivia_question = 0
    
    preguntas_trivia = [
        {
            "pregunta": "¿Cuál es la capital de Francia?",
            "opciones": ["Londres", "Berlín", "París", "Madrid"],
            "correcta": 2
        },
        {
            "pregunta": "¿En qué año llegó el hombre a la Luna?",
            "opciones": ["1967", "1969", "1971", "1973"],
            "correcta": 1
        },
        {
            "pregunta": "¿Cuál es el planeta más grande del sistema solar?",
            "opciones": ["Tierra", "Júpiter", "Saturno", "Neptuno"],
            "correcta": 1
        }
    ]
    
    if st.session_state.trivia_question < len(preguntas_trivia):
        pregunta_actual = preguntas_trivia[st.session_state.trivia_question]
        
        st.markdown(f"### Pregunta {st.session_state.trivia_question + 1}")
        st.markdown(f"**{pregunta_actual['pregunta']}**")
        
        respuesta = st.radio("Selecciona tu respuesta:", pregunta_actual['opciones'], key=f"trivia_{st.session_state.trivia_question}")
        
        if st.button("Responder", key=f"answer_{st.session_state.trivia_question}"):
            if pregunta_actual['opciones'].index(respuesta) == pregunta_actual['correcta']:
                st.success("✅ ¡Correcto!")
                st.session_state.trivia_score += 1
            else:
                st.error(f"❌ Incorrecto. La respuesta era: {pregunta_actual['opciones'][pregunta_actual['correcta']]}")
            
            st.session_state.trivia_question += 1
            time.sleep(1)
            st.rerun()
    
    else:
        st.markdown("### 🎉 ¡Juego Terminado!")
        st.metric("Puntuación Final", f"{st.session_state.trivia_score}/{len(preguntas_trivia)}")
        
        if st.button("🔄 Jugar de Nuevo"):
            st.session_state.trivia_score = 0
            st.session_state.trivia_question = 0
            st.rerun()

def render_proyecto_reportes():
    """Proyecto guiado: Generador de Reportes."""
    st.markdown("### 📝 Proyecto: Generador de Reportes")
    st.info("Aprende a crear un sistema de reportes automáticos con exportación.")
    
    # Demo simple del generador
    tipo_reporte = st.selectbox(
        "Tipo de reporte:",
        ["Ventas Mensual", "Inventario", "Usuarios Activos"]
    )
    
    formato = st.selectbox("Formato:", ["PDF", "Excel", "CSV"])
    
    if st.button("🎯 Generar Reporte"):
        with st.spinner("Generando reporte..."):
            time.sleep(2)  # Simular procesamiento
            
            # Generar datos de ejemplo
            if tipo_reporte == "Ventas Mensual":
                datos = {
                    'Mes': ['Enero', 'Febrero', 'Marzo', 'Abril'],
                    'Ventas': [15000, 18000, 22000, 19000],
                    'Meta': [16000, 17000, 20000, 21000]
                }
            elif tipo_reporte == "Inventario":
                datos = {
                    'Producto': ['A', 'B', 'C', 'D'],
                    'Stock': [150, 75, 200, 30],
                    'Mínimo': [100, 50, 150, 25]
                }
            else:
                datos = {
                    'Usuario': ['user1', 'user2', 'user3'],
                    'Último Login': ['2024-01-15', '2024-01-14', '2024-01-10'],
                    'Sesiones': [45, 23, 12]
                }
            
            df = pd.DataFrame(datos)
            
            st.success(f"✅ Reporte '{tipo_reporte}' generado en formato {formato}")
            st.dataframe(df)
            
            # Simular descarga
            csv = df.to_csv(index=False)
            st.download_button(
                label=f"📥 Descargar {formato}",
                data=csv,
                file_name=f"reporte_{tipo_reporte.lower().replace(' ', '_')}.csv",
                mime="text/csv"
            )

def render_proyecto_chatbot():
    """Proyecto guiado: Chatbot Simple."""
    st.markdown("### 🤖 Proyecto: Chatbot Simple")
    st.info("Construye un chatbot básico con respuestas predefinidas.")
    
    # Inicializar historial de chat
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "bot", "message": "¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte?"}
        ]
    
    # Mostrar historial
    for chat in st.session_state.chat_history:
        if chat['role'] == 'user':
            st.markdown(f"**Tú:** {chat['message']}")
        else:
            st.markdown(f"**🤖 Bot:** {chat['message']}")
    
    # Input del usuario
    user_input = st.text_input("Escribe tu mensaje:", key="chat_input")
    
    if st.button("Enviar") and user_input:
        # Agregar mensaje del usuario
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        
        # Generar respuesta del bot
        bot_response = generar_respuesta_bot(user_input)
        st.session_state.chat_history.append({"role": "bot", "message": bot_response})
        
        st.rerun()
    
    if st.button("🧹 Limpiar Chat"):
        st.session_state.chat_history = [
            {"role": "bot", "message": "¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte?"}
        ]
        st.rerun()

def generar_respuesta_bot(mensaje):
    """Genera respuesta simple del bot basada en palabras clave."""
    mensaje_lower = mensaje.lower()
    
    if "hola" in mensaje_lower or "hi" in mensaje_lower:
        return "¡Hola! Es un placer saludarte. ¿Cómo estás hoy?"
    
    elif "streamlit" in mensaje_lower:
        return "¡Streamlit es increíble! Es perfecto para crear aplicaciones web de datos rápidamente."
    
    elif "ayuda" in mensaje_lower or "help" in mensaje_lower:
        return "¡Por supuesto! Puedo ayudarte con preguntas sobre Streamlit, programación o charlar contigo."
    
    elif "gracias" in mensaje_lower or "thanks" in mensaje_lower:
        return "¡De nada! Siempre es un placer ayudar. ¿Hay algo más en lo que pueda asistirte?"
    
    elif "adiós" in mensaje_lower or "bye" in mensaje_lower:
        return "¡Hasta luego! Que tengas un excelente día. ¡Vuelve cuando quieras!"
    
    elif "?" in mensaje:
        return "Esa es una excelente pregunta. Aunque soy un bot simple, haré mi mejor esfuerzo para ayudarte."
    
    else:
        respuestas_genericas = [
            "Interesante punto de vista. ¿Podrías contarme más?",
            "Entiendo. ¿Hay algo específico en lo que pueda ayudarte?",
            "¡Qué genial! Me gusta aprender cosas nuevas.",
            "Gracias por compartir eso conmigo. ¿Qué más te gustaría saber?",
            "¡Fascinante! Cuéntame más sobre eso."
        ]
        return random.choice(respuestas_genericas)

def render_resultados():
    """Renderiza el resumen de resultados y progreso."""
    st.subheader("📊 Resultados y Progreso")
    
    st.markdown("""
    Revisa tu progreso en el curso y tus logros obtenidos.
    """)
    
    # Progreso general
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Progreso del Curso")
        
        # Calcular progreso basado en actividades completadas
        progreso_quiz = len(st.session_state.get('quiz_history', [])) > 0
        progreso_ejercicios = 'calc_code' in st.session_state and st.session_state.get('calc_code', '').strip() != ''
        progreso_proyectos = len(st.session_state.get('chat_history', [])) > 1
        
        actividades_completadas = sum([progreso_quiz, progreso_ejercicios, progreso_proyectos])
        total_actividades = 3
        progreso_porcentaje = (actividades_completadas / total_actividades) * 100
        
        st.progress(progreso_porcentaje / 100)
        st.write(f"Progreso general: {progreso_porcentaje:.0f}% ({actividades_completadas}/{total_actividades} actividades)")
        
        # Detalles por módulo
        st.markdown("#### 📋 Estado por Módulo")
        
        modulos = [
            {"nombre": "Quiz Teórico", "completado": progreso_quiz},
            {"nombre": "Ejercicios de Código", "completado": progreso_ejercicios},
            {"nombre": "Proyectos Guiados", "completado": progreso_proyectos}
        ]
        
        for modulo in modulos:
            estado = "✅" if modulo["completado"] else "⏳"
            st.write(f"{estado} {modulo['nombre']}")
    
    with col2:
        st.markdown("### 🏆 Logros")
        
        # Sistema de logros
        logros = []
        
        if progreso_quiz:
            logros.append("🎯 Primer Quiz Completado")
        
        if len(st.session_state.get('quiz_history', [])) >= 3:
            logros.append("📚 Estudiante Dedicado")
        
        if progreso_ejercicios:
            logros.append("💻 Primer Código Escrito")
        
        if progreso_proyectos:
            logros.append("🏗️ Constructor de Proyectos")
        
        if st.session_state.get('quiz_history', []):
            mejor_score = max([q['porcentaje'] for q in st.session_state.quiz_history])
            if mejor_score >= 80:
                logros.append("🌟 Puntuación Excelente")
        
        if logros:
            for logro in logros:
                st.success(logro)
        else:
            st.info("¡Completa actividades para desbloquear logros!")
    
    # Historial detallado
    st.markdown("---")
    st.markdown("### 📚 Historial Detallado")
    
    # Historial de quiz
    if st.session_state.get('quiz_history'):
        st.markdown("#### 🎯 Historial de Quiz")
        
        quiz_df = pd.DataFrame(st.session_state.quiz_history)
        quiz_df = quiz_df.sort_values('timestamp', ascending=False)
        
        st.dataframe(
            quiz_df[['timestamp', 'porcentaje', 'correctas', 'total_preguntas']],
            column_config={
                'timestamp': 'Fecha y Hora',
                'porcentaje': st.column_config.ProgressColumn('Porcentaje', min_value=0, max_value=100),
                'correctas': 'Correctas',
                'total_preguntas': 'Total'
            }
        )
    
    # Estadísticas de análisis de sentimientos
    if st.session_state.get('sentiment_history'):
        st.markdown("#### 🔍 Análisis de Sentimientos")
        
        sentiment_counts = {}
        for analisis in st.session_state.sentiment_history:
            sentimiento = analisis['sentimiento']
            sentiment_counts[sentimiento] = sentiment_counts.get(sentimiento, 0) + 1
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Distribución de sentimientos:**")
            for sentimiento, count in sentiment_counts.items():
                st.write(f"• {sentimiento}: {count}")
        
        with col2:
            if len(sentiment_counts) > 0:
                fig = px.pie(
                    values=list(sentiment_counts.values()),
                    names=list(sentiment_counts.keys()),
                    title="Distribución de Sentimientos Analizados"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Botón para exportar progreso
    if st.button("📥 Exportar Progreso"):
        progreso_data = {
            'fecha_exportacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'progreso_general': f"{progreso_porcentaje:.0f}%",
            'actividades_completadas': actividades_completadas,
            'total_actividades': total_actividades,
            'logros': logros,
            'quiz_history': st.session_state.get('quiz_history', []),
            'sentiment_history': st.session_state.get('sentiment_history', [])
        }
        
        json_str = json.dumps(progreso_data, indent=2, ensure_ascii=False)
        
        st.download_button(
            label="📄 Descargar Reporte JSON",
            data=json_str,
            file_name=f"progreso_streamlit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

if __name__ == "__main__":
    run()
