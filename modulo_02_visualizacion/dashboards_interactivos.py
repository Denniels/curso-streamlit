import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def run():
    """Módulo de Dashboards Interactivos."""
    
    with st.container():
        st.title("📈 Clase 2: Dashboards Interactivos")
        st.markdown("""
        Aprende a crear dashboards profesionales que combinan múltiples visualizaciones,
        filtros dinámicos y métricas clave en tiempo real.
        """)
        
        # Generar dataset de ventas simulado
        @st.cache_data
        def generar_datos_ventas():
            np.random.seed(42)
            fechas = pd.date_range('2024-01-01', '2024-12-31', freq='D')
            productos = ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Auriculares']
            regiones = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
            vendedores = ['Ana García', 'Carlos López', 'María Rodríguez', 'Juan Pérez', 'Laura Martínez']
            
            datos = []
            for fecha in fechas:
                n_ventas = np.random.poisson(8)  # Promedio 8 ventas por día
                for _ in range(n_ventas):
                    datos.append({
                        'fecha': fecha,
                        'producto': np.random.choice(productos),
                        'region': np.random.choice(regiones),
                        'vendedor': np.random.choice(vendedores),
                        'cantidad': np.random.randint(1, 10),
                        'precio_unitario': np.random.uniform(50, 2000),
                        'descuento': np.random.uniform(0, 0.3)
                    })
            
            df = pd.DataFrame(datos)
            df['total_bruto'] = df['cantidad'] * df['precio_unitario']
            df['total_neto'] = df['total_bruto'] * (1 - df['descuento'])
            df['mes'] = df['fecha'].dt.month
            df['trimestre'] = df['fecha'].dt.quarter
            
            return df
        
        df_ventas = generar_datos_ventas()
        
        # Pestañas del dashboard
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Overview General",
            "📈 Análisis Temporal", 
            "🌍 Análisis Regional",
            "👥 Performance Vendedores"
        ])
        
        with tab1:
            st.subheader("📊 Dashboard General de Ventas")
            
            # Filtros principales
            st.markdown("### 🎛️ Filtros")
            col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
            
            with col_filtro1:
                productos_selected = st.multiselect(
                    "Productos",
                    options=df_ventas['producto'].unique(),
                    default=df_ventas['producto'].unique(),
                    key="overview_productos"
                )
            
            with col_filtro2:
                regiones_selected = st.multiselect(
                    "Regiones", 
                    options=df_ventas['region'].unique(),
                    default=df_ventas['region'].unique(),
                    key="overview_regiones"
                )
            
            with col_filtro3:
                rango_fechas = st.date_input(
                    "Rango de fechas",
                    value=[df_ventas['fecha'].min(), df_ventas['fecha'].max()],
                    min_value=df_ventas['fecha'].min(),
                    max_value=df_ventas['fecha'].max(),
                    key="overview_fechas"
                )
            
            # Filtrar datos
            df_filtrado = df_ventas[
                (df_ventas['producto'].isin(productos_selected)) &
                (df_ventas['region'].isin(regiones_selected)) &
                (df_ventas['fecha'] >= pd.to_datetime(rango_fechas[0])) &
                (df_ventas['fecha'] <= pd.to_datetime(rango_fechas[1]))
            ]
            
            # KPIs principales
            st.markdown("### 🎯 KPIs Principales")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_ventas = df_filtrado['total_neto'].sum()
                st.metric("💰 Ventas Totales", f"${total_ventas:,.0f}")
            
            with col2:
                total_unidades = df_filtrado['cantidad'].sum()
                st.metric("📦 Unidades Vendidas", f"{total_unidades:,}")
            
            with col3:
                promedio_venta = df_filtrado['total_neto'].mean()
                st.metric("📊 Venta Promedio", f"${promedio_venta:.0f}")
            
            with col4:
                num_transacciones = len(df_filtrado)
                st.metric("🔢 Transacciones", f"{num_transacciones:,}")
            
            # Gráficos principales
            col_graf1, col_graf2 = st.columns(2)
            
            with col_graf1:
                # Ventas por producto
                ventas_producto = df_filtrado.groupby('producto')['total_neto'].sum().reset_index()
                fig_productos = px.bar(
                    ventas_producto, 
                    x='producto', 
                    y='total_neto',
                    title="Ventas por Producto",
                    color='total_neto',
                    color_continuous_scale='blues'
                )
                fig_productos.update_layout(showlegend=False)
                st.plotly_chart(fig_productos, use_container_width=True)
            
            with col_graf2:
                # Ventas por región
                ventas_region = df_filtrado.groupby('region')['total_neto'].sum().reset_index()
                fig_regiones = px.pie(
                    ventas_region,
                    values='total_neto',
                    names='region', 
                    title="Distribución por Región"
                )
                st.plotly_chart(fig_regiones, use_container_width=True)
            
            # Tabla de resumen
            st.markdown("### 📋 Resumen Detallado")
            resumen = df_filtrado.groupby(['producto', 'region']).agg({
                'total_neto': 'sum',
                'cantidad': 'sum',
                'fecha': 'count'
            }).round(2)
            resumen.columns = ['Ventas ($)', 'Unidades', 'Transacciones']
            st.dataframe(resumen, use_container_width=True)
        
        with tab2:
            st.subheader("📈 Análisis Temporal de Ventas")
            
            # Controles temporales
            col_temp1, col_temp2 = st.columns(2)
            
            with col_temp1:
                granularidad = st.selectbox(
                    "Granularidad temporal",
                    ["Diario", "Semanal", "Mensual"],
                    key="temporal_granularidad"
                )
            
            with col_temp2:
                producto_temporal = st.selectbox(
                    "Producto (opcional)",
                    ["Todos"] + list(df_ventas['producto'].unique()),
                    key="temporal_producto"
                )
            
            # Filtrar por producto si se selecciona
            df_temp = df_ventas.copy()
            if producto_temporal != "Todos":
                df_temp = df_temp[df_temp['producto'] == producto_temporal]
            
            # Agrupar según granularidad
            if granularidad == "Diario":
                df_temp['periodo'] = df_temp['fecha']
            elif granularidad == "Semanal":
                df_temp['periodo'] = df_temp['fecha'].dt.to_period('W').dt.start_time
            else:  # Mensual
                df_temp['periodo'] = df_temp['fecha'].dt.to_period('M').dt.start_time
            
            ventas_tiempo = df_temp.groupby('periodo').agg({
                'total_neto': 'sum',
                'cantidad': 'sum'
            }).reset_index()
            
            # Gráfico temporal principal
            fig_temporal = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Ventas en $', 'Unidades Vendidas'),
                vertical_spacing=0.1
            )
            
            fig_temporal.add_trace(
                go.Scatter(
                    x=ventas_tiempo['periodo'],
                    y=ventas_tiempo['total_neto'],
                    mode='lines+markers',
                    name='Ventas ($)',
                    line=dict(color='#1f77b4', width=3)
                ),
                row=1, col=1
            )
            
            fig_temporal.add_trace(
                go.Scatter(
                    x=ventas_tiempo['periodo'],
                    y=ventas_tiempo['cantidad'],
                    mode='lines+markers',
                    name='Unidades',
                    line=dict(color='#ff7f0e', width=3)
                ),
                row=2, col=1
            )
            
            fig_temporal.update_layout(
                title=f"Tendencia {granularidad} de Ventas",
                height=600,
                showlegend=False
            )
            
            st.plotly_chart(fig_temporal, use_container_width=True)
            
            # Análisis de tendencia
            col_trend1, col_trend2, col_trend3 = st.columns(3)
            
            with col_trend1:
                # Crecimiento promedio
                if len(ventas_tiempo) > 1:
                    crecimiento = ((ventas_tiempo['total_neto'].iloc[-1] / ventas_tiempo['total_neto'].iloc[0]) - 1) * 100
                    st.metric("📈 Crecimiento Total", f"{crecimiento:+.1f}%")
            
            with col_trend2:
                # Mejor período
                mejor_periodo = ventas_tiempo.loc[ventas_tiempo['total_neto'].idxmax()]
                st.metric("🏆 Mejor Período", f"${mejor_periodo['total_neto']:,.0f}")
                st.caption(f"{mejor_periodo['periodo'].strftime('%Y-%m-%d')}")
            
            with col_trend3:
                # Promedio del período
                promedio_periodo = ventas_tiempo['total_neto'].mean()
                st.metric("📊 Promedio", f"${promedio_periodo:,.0f}")
        
        with tab3:
            st.subheader("🌍 Análisis Regional Detallado")
            
            # Análisis por región
            col_reg1, col_reg2 = st.columns([2, 1])
            
            with col_reg2:
                st.markdown("### 🎛️ Configuración")
                
                metrica_regional = st.selectbox(
                    "Métrica a analizar",
                    ["Ventas ($)", "Unidades", "Transacciones", "Venta Promedio"],
                    key="regional_metrica"
                )
                
                incluir_tendencia = st.checkbox("Mostrar tendencia temporal", key="regional_tendencia")
                
                st.markdown("### 📊 Rankings")
                
                # Calcular métricas por región
                metricas_region = df_ventas.groupby('region').agg({
                    'total_neto': ['sum', 'mean'],
                    'cantidad': 'sum',
                    'fecha': 'count'
                }).round(2)
                
                metricas_region.columns = ['Ventas ($)', 'Venta Promedio', 'Unidades', 'Transacciones']
                metricas_region = metricas_region.sort_values('Ventas ($)', ascending=False)
                
                st.dataframe(metricas_region, use_container_width=True)
            
            with col_reg1:
                # Mapear métrica seleccionada
                metrica_map = {
                    "Ventas ($)": 'Ventas ($)',
                    "Unidades": 'Unidades', 
                    "Transacciones": 'Transacciones',
                    "Venta Promedio": 'Venta Promedio'
                }
                
                col_metrica = metrica_map[metrica_regional]
                
                # Gráfico principal regional
                fig_regional = px.bar(
                    metricas_region.reset_index(),
                    x='region',
                    y=col_metrica,
                    title=f"{metrica_regional} por Región",
                    color=col_metrica,
                    color_continuous_scale='viridis'
                )
                
                st.plotly_chart(fig_regional, use_container_width=True)
                
                # Tendencia temporal por región si se solicita
                if incluir_tendencia:
                    ventas_region_tiempo = df_ventas.groupby(['fecha', 'region'])['total_neto'].sum().reset_index()
                    
                    fig_trend_regional = px.line(
                        ventas_region_tiempo,
                        x='fecha',
                        y='total_neto',
                        color='region',
                        title="Tendencia de Ventas por Región"
                    )
                    
                    st.plotly_chart(fig_trend_regional, use_container_width=True)
            
            # Comparación detallada
            st.markdown("### 🔍 Comparación Detallada por Región")
            
            col_comp1, col_comp2 = st.columns(2)
            
            with col_comp1:
                region_1 = st.selectbox("Región 1", df_ventas['region'].unique(), key="comp_region1")
            
            with col_comp2:
                region_2 = st.selectbox("Región 2", df_ventas['region'].unique(), index=1, key="comp_region2")
            
            if region_1 != region_2:
                # Comparar regiones
                datos_r1 = df_ventas[df_ventas['region'] == region_1]
                datos_r2 = df_ventas[df_ventas['region'] == region_2]
                
                col_metrics1, col_metrics2 = st.columns(2)
                
                with col_metrics1:
                    st.markdown(f"#### 📍 {region_1}")
                    st.metric("💰 Ventas", f"${datos_r1['total_neto'].sum():,.0f}")
                    st.metric("📦 Unidades", f"{datos_r1['cantidad'].sum():,}")
                    st.metric("📊 Venta Promedio", f"${datos_r1['total_neto'].mean():.0f}")
                
                with col_metrics2:
                    st.markdown(f"#### 📍 {region_2}")
                    st.metric("💰 Ventas", f"${datos_r2['total_neto'].sum():,.0f}")
                    st.metric("📦 Unidades", f"{datos_r2['cantidad'].sum():,}")
                    st.metric("📊 Venta Promedio", f"${datos_r2['total_neto'].mean():.0f}")
        
        with tab4:
            st.subheader("👥 Performance de Vendedores")
            
            # Análisis de vendedores
            performance = df_ventas.groupby('vendedor').agg({
                'total_neto': ['sum', 'mean', 'count'],
                'cantidad': 'sum',
                'descuento': 'mean'
            }).round(2)
            
            performance.columns = ['Ventas Totales', 'Venta Promedio', 'Transacciones', 'Unidades', 'Descuento Promedio']
            performance = performance.sort_values('Ventas Totales', ascending=False)
            
            col_perf1, col_perf2 = st.columns([2, 1])
            
            with col_perf1:
                # Gráfico de performance
                fig_vendedores = px.bar(
                    performance.reset_index(),
                    x='vendedor',
                    y='Ventas Totales',
                    title="Ventas Totales por Vendedor",
                    color='Ventas Totales',
                    color_continuous_scale='blues'
                )
                
                fig_vendedores.update_layout(
                    xaxis_tickangle=-45,
                    showlegend=False
                )
                
                st.plotly_chart(fig_vendedores, use_container_width=True)
                
                # Análisis de eficiencia (venta promedio vs número de transacciones)
                fig_eficiencia = px.scatter(
                    performance.reset_index(),
                    x='Transacciones',
                    y='Venta Promedio',
                    size='Ventas Totales',
                    color='Descuento Promedio',
                    hover_name='vendedor',
                    title="Eficiencia: Venta Promedio vs Número de Transacciones",
                    color_continuous_scale='viridis'
                )
                
                st.plotly_chart(fig_eficiencia, use_container_width=True)
            
            with col_perf2:
                st.markdown("### 🏆 Rankings")
                
                # Top performers
                st.markdown("**🥇 Top Ventas:**")
                top_ventas = performance.head(3)['Ventas Totales']
                for i, (vendedor, ventas) in enumerate(top_ventas.items()):
                    emoji = ["🥇", "🥈", "🥉"][i]
                    st.write(f"{emoji} {vendedor}: ${ventas:,.0f}")
                
                st.markdown("**💎 Mayor Venta Promedio:**")
                top_promedio = performance.sort_values('Venta Promedio', ascending=False).head(3)['Venta Promedio']
                for i, (vendedor, promedio) in enumerate(top_promedio.items()):
                    emoji = ["🥇", "🥈", "🥉"][i]
                    st.write(f"{emoji} {vendedor}: ${promedio:.0f}")
                
                st.markdown("**⚡ Más Activos:**")
                top_transacciones = performance.sort_values('Transacciones', ascending=False).head(3)['Transacciones']
                for i, (vendedor, trans) in enumerate(top_transacciones.items()):
                    emoji = ["🥇", "🥈", "🥉"][i]
                    st.write(f"{emoji} {vendedor}: {trans} ventas")
            
            # Tabla completa de performance
            st.markdown("### 📊 Tabla Completa de Performance")
            st.dataframe(performance, use_container_width=True)
        
        # Conclusión del módulo
        st.markdown("---")
        st.markdown("### 🎯 ¿Qué aprendiste en esta clase?")
        st.markdown("""
        - **Dashboards multi-tab** para organizar información compleja
        - **Filtros interactivos** que afectan múltiples visualizaciones
        - **KPIs y métricas** calculadas dinámicamente
        - **Análisis temporal** con diferentes granularidades
        - **Comparaciones regionales** y de performance
        - **Subplots** para mostrar múltiples gráficos relacionados
        - **Integración de tablas** con visualizaciones
        """)
        
        st.success("🎉 ¡Excelente! Ahora puedes crear dashboards profesionales completos.")
