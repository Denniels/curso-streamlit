import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def run():
    """Módulo de Gráficos Básicos con Plotly."""
    
    with st.container():
        st.title("📊 Clase 1: Gráficos Básicos con Plotly")
        st.markdown("""
        Aprende a crear visualizaciones interactivas y profesionales con Plotly.  
        Estos gráficos son dinámicos, responsivos y perfectos para dashboards.
        """)
        
        # Pestañas para diferentes tipos de gráficos
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Gráfico de Líneas",
            "📊 Gráfico de Barras", 
            "🍕 Gráfico de Torta",
            "📉 Scatter Plot"
        ])
        
        with tab1:
            st.subheader("📈 Gráfico de Líneas Interactivo")
            
            # Controles para personalizar el gráfico
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Configuración:**")
                puntos = st.slider("Número de puntos", 10, 100, 50, key="lineas_puntos")
                ruido = st.slider("Nivel de ruido", 0.0, 2.0, 0.5, key="lineas_ruido")
                mostrar_puntos = st.checkbox("Mostrar puntos", value=True, key="lineas_mostrar_puntos")
            
            with col2:
                # Generar datos
                x = np.linspace(0, 10, puntos)
                y1 = np.sin(x) + np.random.normal(0, ruido, puntos)
                y2 = np.cos(x) + np.random.normal(0, ruido, puntos)
                
                # Crear gráfico con Plotly
                fig = go.Figure()
                
                mode = 'lines+markers' if mostrar_puntos else 'lines'
                
                fig.add_trace(go.Scatter(
                    x=x, y=y1, 
                    mode=mode,
                    name='Función Seno',
                    line=dict(color='#1f77b4', width=3)
                ))
                
                fig.add_trace(go.Scatter(
                    x=x, y=y2,
                    mode=mode, 
                    name='Función Coseno',
                    line=dict(color='#ff7f0e', width=3)
                ))
                
                fig.update_layout(
                    title="Funciones Trigonométricas",
                    xaxis_title="X",
                    yaxis_title="Y",
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            st.code("""
import plotly.graph_objects as go
import numpy as np

# Generar datos
x = np.linspace(0, 10, 50)
y1 = np.sin(x) + np.random.normal(0, 0.5, 50)
y2 = np.cos(x) + np.random.normal(0, 0.5, 50)

# Crear gráfico
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y1, mode='lines+markers', name='Seno'))
fig.add_trace(go.Scatter(x=x, y=y2, mode='lines+markers', name='Coseno'))

fig.update_layout(title="Funciones Trigonométricas")
st.plotly_chart(fig, use_container_width=True)
""", language="python")
        
        with tab2:
            st.subheader("📊 Gráfico de Barras Dinámico")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Datos de Ventas:**")
                # Permitir al usuario modificar los datos
                productos = ["Producto A", "Producto B", "Producto C", "Producto D", "Producto E"]
                ventas = []
                
                for i, producto in enumerate(productos):
                    venta = st.slider(
                        f"Ventas {producto}", 
                        0, 1000, 
                        np.random.randint(100, 800),
                        key=f"ventas_{i}"
                    )
                    ventas.append(venta)
                
                orientacion = st.radio(
                    "Orientación", 
                    ["Vertical", "Horizontal"],
                    key="barras_orientacion"
                )
            
            with col2:
                # Crear DataFrame
                df = pd.DataFrame({
                    'Producto': productos,
                    'Ventas': ventas
                })
                
                # Crear gráfico de barras
                if orientacion == "Vertical":
                    fig = px.bar(
                        df, 
                        x='Producto', 
                        y='Ventas',
                        color='Ventas',
                        color_continuous_scale='viridis',
                        title="Ventas por Producto"
                    )
                else:
                    fig = px.bar(
                        df, 
                        x='Ventas', 
                        y='Producto',
                        color='Ventas',
                        color_continuous_scale='viridis',
                        title="Ventas por Producto",
                        orientation='h'
                    )
                
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                
                # Mostrar datos
                st.markdown("**Datos actuales:**")
                st.dataframe(df, use_container_width=True)
            
            st.code("""
import plotly.express as px
import pandas as pd

# Crear datos
df = pd.DataFrame({
    'Producto': ['A', 'B', 'C', 'D', 'E'],
    'Ventas': [450, 380, 620, 290, 710]
})

# Crear gráfico de barras
fig = px.bar(df, x='Producto', y='Ventas', 
             color='Ventas', color_continuous_scale='viridis')
st.plotly_chart(fig, use_container_width=True)
""", language="python")
        
        with tab3:
            st.subheader("🍕 Gráfico de Torta Personalizable")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Distribución de Gastos:**")
                # Categorías predefinidas
                categorias = ["Vivienda", "Alimentación", "Transporte", "Entretenimiento", "Ahorros", "Otros"]
                gastos = {}
                
                for categoria in categorias:
                    gasto = st.number_input(
                        f"{categoria} ($)", 
                        min_value=0, 
                        max_value=5000,
                        value=np.random.randint(200, 1500),
                        step=50,
                        key=f"gasto_{categoria}"
                    )
                    gastos[categoria] = gasto
                
                mostrar_porcentajes = st.checkbox("Mostrar porcentajes", value=True, key="torta_porcentajes")
                tema = st.selectbox("Tema de colores", ["Plotly", "Viridis", "Rainbow"], key="torta_tema")
            
            with col2:
                # Crear DataFrame
                df_gastos = pd.DataFrame(list(gastos.items()), columns=['Categoría', 'Monto'])
                df_gastos = df_gastos[df_gastos['Monto'] > 0]  # Filtrar valores 0
                
                # Mapear temas de colores
                color_maps = {
                    "Plotly": px.colors.qualitative.Plotly,
                    "Viridis": px.colors.sequential.Viridis,
                    "Rainbow": px.colors.qualitative.Safe
                }
                
                # Crear gráfico de torta
                fig = px.pie(
                    df_gastos, 
                    values='Monto', 
                    names='Categoría',
                    title="Distribución de Gastos Mensuales",
                    color_discrete_sequence=color_maps[tema]
                )
                
                if mostrar_porcentajes:
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                else:
                    fig.update_traces(textposition='inside', textinfo='label')
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Estadísticas
                total = df_gastos['Monto'].sum()
                st.metric("💰 Total de Gastos", f"${total:,.0f}")
                
                if len(df_gastos) > 0:
                    mayor_gasto = df_gastos.loc[df_gastos['Monto'].idxmax()]
                    st.metric("📈 Mayor Gasto", f"{mayor_gasto['Categoría']}: ${mayor_gasto['Monto']:,.0f}")
            
            st.code("""
import plotly.express as px
import pandas as pd

# Datos de gastos
df = pd.DataFrame({
    'Categoría': ['Vivienda', 'Alimentación', 'Transporte', 'Entretenimiento'],
    'Monto': [1200, 600, 400, 300]
})

# Crear gráfico de torta
fig = px.pie(df, values='Monto', names='Categoría', 
             title="Distribución de Gastos")
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)
""", language="python")
        
        with tab4:
            st.subheader("📉 Scatter Plot con Análisis")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Configuración del Dataset:**")
                n_puntos = st.slider("Número de puntos", 50, 500, 200, key="scatter_puntos")
                correlacion = st.slider("Correlación", -1.0, 1.0, 0.7, key="scatter_correlacion")
                ruido = st.slider("Nivel de ruido", 0.1, 2.0, 0.5, key="scatter_ruido")
                
                # Opciones de colores
                color_por = st.selectbox(
                    "Colorear por:",
                    ["Ninguno", "Valor Y", "Categoría", "Distancia"],
                    key="scatter_color"
                )
                
                mostrar_tendencia = st.checkbox("Mostrar línea de tendencia", value=True, key="scatter_tendencia")
            
            with col2:
                # Generar datos correlacionados
                np.random.seed(42)  # Para reproducibilidad
                x = np.random.normal(0, 1, n_puntos)
                y = correlacion * x + np.sqrt(1 - correlacion**2) * np.random.normal(0, ruido, n_puntos)
                
                # Crear categorías aleatorias
                categorias = np.random.choice(['Tipo A', 'Tipo B', 'Tipo C'], n_puntos)
                distancias = np.sqrt(x**2 + y**2)
                
                # Crear DataFrame
                df_scatter = pd.DataFrame({
                    'X': x,
                    'Y': y,
                    'Categoría': categorias,
                    'Distancia': distancias
                })
                
                # Configurar color
                color = None
                if color_por == "Valor Y":
                    color = 'Y'
                elif color_por == "Categoría":
                    color = 'Categoría'
                elif color_por == "Distancia":
                    color = 'Distancia'
                
                # Crear scatter plot
                fig = px.scatter(
                    df_scatter, 
                    x='X', 
                    y='Y',
                    color=color,
                    title=f"Scatter Plot (Correlación: {correlacion:.2f})",
                    opacity=0.7
                )
                
                # Agregar línea de tendencia
                if mostrar_tendencia:
                    fig.add_traces(px.scatter(df_scatter, x='X', y='Y', trendline="ols").data[1:])
                
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Estadísticas
                corr_real = np.corrcoef(x, y)[0, 1]
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric("📊 Correlación Real", f"{corr_real:.3f}")
                with col_b:
                    st.metric("📈 Media X", f"{np.mean(x):.2f}")
                with col_c:
                    st.metric("📉 Media Y", f"{np.mean(y):.2f}")
            
            st.code("""
import plotly.express as px
import pandas as pd
import numpy as np

# Generar datos correlacionados
x = np.random.normal(0, 1, 200)
y = 0.7 * x + np.sqrt(1 - 0.7**2) * np.random.normal(0, 0.5, 200)

df = pd.DataFrame({'X': x, 'Y': y})

# Crear scatter plot con línea de tendencia
fig = px.scatter(df, x='X', y='Y', trendline="ols", 
                title="Scatter Plot con Tendencia")
st.plotly_chart(fig, use_container_width=True)
""", language="python")
        
        # Sección de conclusión
        st.markdown("---")
        st.markdown("### 🎯 ¿Qué aprendiste en esta clase?")
        st.markdown("""
        - **Gráficos de líneas** para mostrar tendencias temporales
        - **Gráficos de barras** para comparar categorías  
        - **Gráficos de torta** para mostrar proporciones
        - **Scatter plots** para analizar correlaciones
        - **Interactividad** con controles que modifican visualizaciones en tiempo real
        - **Plotly** como herramienta profesional para dashboards
        """)
        
        st.success("🎉 ¡Felicidades! Ya puedes crear gráficos interactivos profesionales con Streamlit y Plotly.")
