import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

def run():
    """Módulo de Aplicaciones Completas - Calculadora Financiera."""
    
    with st.container():
        st.title("💰 Clase 1: Calculadora Financiera Avanzada")
        st.markdown("""
        Construye una aplicación completa de finanzas personales con múltiples calculadoras,
        visualizaciones interactivas y análisis de inversiones.
        """)
        
        # Pestañas para diferentes calculadoras
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🏠 Préstamo Hipotecario",
            "📈 Inversión Compuesta",
            "💳 Tarjeta de Crédito",
            "📊 Comparador de Inversiones",
            "🔍 Ver Código Fuente"
        ])
        
        with tab1:
            st.subheader("🏠 Calculadora de Préstamo Hipotecario")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Parámetros del préstamo:**")
                monto_prestamo = st.number_input(
                    "Monto del préstamo ($)",
                    min_value=10000,
                    max_value=1000000,
                    value=200000,
                    step=5000,
                    key="hipoteca_monto"
                )
                
                tasa_anual = st.slider(
                    "Tasa de interés anual (%)",
                    min_value=1.0,
                    max_value=15.0,
                    value=4.5,
                    step=0.1,
                    key="hipoteca_tasa"
                )
                
                años = st.selectbox(
                    "Años del préstamo",
                    [15, 20, 25, 30],
                    index=3,
                    key="hipoteca_años"
                )
                
                pie_inicial = st.number_input(
                    "Pie inicial ($)",
                    min_value=0,
                    max_value=monto_prestamo,
                    value=int(monto_prestamo * 0.2),
                    step=1000,
                    key="hipoteca_pie"
                )
                
            with col2:
                # Cálculos de hipoteca
                tasa_mensual = tasa_anual / 100 / 12
                num_pagos = años * 12
                monto_financiado = monto_prestamo - pie_inicial
                
                if monto_financiado > 0:
                    # Fórmula de pago mensual
                    pago_mensual = monto_financiado * (tasa_mensual * (1 + tasa_mensual) ** num_pagos) / ((1 + tasa_mensual) ** num_pagos - 1)
                    total_pagado = pago_mensual * num_pagos
                    total_intereses = total_pagado - monto_financiado
                    
                    # Métricas principales
                    col_m1, col_m2, col_m3 = st.columns(3)
                    with col_m1:
                        st.metric("Pago Mensual", f"${pago_mensual:,.2f}")
                    with col_m2:
                        st.metric("Total de Intereses", f"${total_intereses:,.2f}")
                    with col_m3:
                        st.metric("Total Pagado", f"${total_pagado:,.2f}")
                    
                    # Crear tabla de amortización (primeros 12 meses)
                    amortizacion = []
                    saldo_restante = monto_financiado
                    
                    for mes in range(1, min(13, num_pagos + 1)):
                        interes_mes = saldo_restante * tasa_mensual
                        capital_mes = pago_mensual - interes_mes
                        saldo_restante -= capital_mes
                        
                        amortizacion.append({
                            'Mes': mes,
                            'Pago Total': pago_mensual,
                            'Capital': capital_mes,
                            'Interés': interes_mes,
                            'Saldo Restante': saldo_restante
                        })
                    
                    df_amortizacion = pd.DataFrame(amortizacion)
                    
                    # Mostrar tabla
                    st.markdown("**Tabla de Amortización (Primeros 12 meses):**")
                    st.dataframe(
                        df_amortizacion.style.format({
                            'Pago Total': '${:,.2f}',
                            'Capital': '${:,.2f}',
                            'Interés': '${:,.2f}',
                            'Saldo Restante': '${:,.2f}'
                        }),
                        use_container_width=True
                    )
                    
                    # Gráfico de evolución
                    fig = px.line(
                        df_amortizacion,
                        x='Mes',
                        y=['Capital', 'Interés'],
                        title="Evolución del Pago: Capital vs Interés",
                        labels={'value': 'Monto ($)', 'variable': 'Tipo'}
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                else:
                    st.warning("⚠️ El pie inicial no puede ser igual o mayor al monto del préstamo")
        
        with tab2:
            st.subheader("📈 Calculadora de Inversión con Interés Compuesto")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Parámetros de inversión:**")
                capital_inicial = st.number_input(
                    "Capital inicial ($)",
                    min_value=100,
                    max_value=100000,
                    value=10000,
                    step=100,
                    key="inversion_capital"
                )
                
                aporte_mensual = st.number_input(
                    "Aporte mensual ($)",
                    min_value=0,
                    max_value=5000,
                    value=500,
                    step=50,
                    key="inversion_aporte"
                )
                
                rentabilidad_anual = st.slider(
                    "Rentabilidad esperada (%)",
                    min_value=1.0,
                    max_value=25.0,
                    value=8.0,
                    step=0.5,
                    key="inversion_rentabilidad"
                )
                
                años_inversion = st.selectbox(
                    "Años de inversión",
                    [1, 3, 5, 10, 15, 20, 25, 30],
                    index=4,
                    key="inversion_años"
                )
                
            with col2:
                # Cálculos de inversión compuesta
                rentabilidad_mensual = rentabilidad_anual / 100 / 12
                meses_total = años_inversion * 12
                
                # Simulación mes a mes
                proyeccion = []
                capital_acumulado = capital_inicial
                
                for mes in range(1, meses_total + 1):
                    # Rendimiento del mes
                    rendimiento_mes = capital_acumulado * rentabilidad_mensual
                    
                    # Agregar aporte mensual
                    capital_acumulado += aporte_mensual + rendimiento_mes
                    
                    # Calcular totales
                    total_aportado = capital_inicial + (aporte_mensual * mes)
                    ganancia_total = capital_acumulado - total_aportado
                    
                    proyeccion.append({
                        'Mes': mes,
                        'Capital Acumulado': capital_acumulado,
                        'Total Aportado': total_aportado,
                        'Ganancia': ganancia_total,
                        'Rendimiento Mes': rendimiento_mes
                    })
                
                # Mostrar resultados finales
                valor_final = capital_acumulado
                total_aportado_final = capital_inicial + (aporte_mensual * meses_total)
                ganancia_final = valor_final - total_aportado_final
                
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Valor Final", f"${valor_final:,.2f}")
                with col_m2:
                    st.metric("Total Aportado", f"${total_aportado_final:,.2f}")
                with col_m3:
                    st.metric("Ganancia Total", f"${ganancia_final:,.2f}")
                
                # Crear gráfico de proyección
                df_proyeccion = pd.DataFrame(proyeccion)
                
                # Filtrar datos para mostrar (cada 6 meses si es muy largo)
                if len(df_proyeccion) > 60:
                    df_chart = df_proyeccion[df_proyeccion['Mes'] % 6 == 0].copy()
                else:
                    df_chart = df_proyeccion.copy()
                
                # Gráfico de área apilada
                fig = px.area(
                    df_chart,
                    x='Mes',
                    y=['Total Aportado', 'Ganancia'],
                    title="Proyección de Inversión con Interés Compuesto",
                    color_discrete_map={
                        'Total Aportado': 'lightblue',
                        'Ganancia': 'lightgreen'
                    }
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("💳 Calculadora de Pago de Tarjeta de Crédito")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Detalles de la tarjeta:**")
                saldo_inicial = st.number_input(
                    "Saldo actual ($)",
                    min_value=100,
                    max_value=50000,
                    value=5000,
                    step=100,
                    key="tarjeta_saldo"
                )
                
                tasa_anual_tc = st.slider(
                    "Tasa de interés anual (%)",
                    min_value=12.0,
                    max_value=36.0,
                    value=24.0,
                    step=0.5,
                    key="tarjeta_tasa"
                )
                
                pago_mensual_tc = st.number_input(
                    "Pago mensual ($)",
                    min_value=50,
                    max_value=2000,
                    value=200,
                    step=25,
                    key="tarjeta_pago"
                )
                
            with col2:
                # Cálculos de tarjeta de crédito
                tasa_mensual_tc = tasa_anual_tc / 100 / 12
                
                # Validar que el pago sea suficiente
                interes_minimo_mensual = saldo_inicial * tasa_mensual_tc
                
                if pago_mensual_tc <= interes_minimo_mensual:
                    st.error(f"""
                    ⚠️ **ALERTA**: Tu pago mensual (${pago_mensual_tc:,.2f}) es menor o igual 
                    al interés mensual (${interes_minimo_mensual:,.2f}).
                    
                    **Esto significa que tu deuda NUNCA se pagará y seguirá creciendo.**
                    
                    💡 **Pago mínimo recomendado**: ${(interes_minimo_mensual * 1.5):,.2f}
                    """)
                else:
                    # Simulación de pagos
                    saldo_actual = saldo_inicial
                    meses_pago = 0
                    total_pagado_tc = 0
                    total_intereses_tc = 0
                    
                    pagos_tc = []
                    
                    while saldo_actual > 0.01 and meses_pago < 360:  # Max 30 años
                        meses_pago += 1
                        
                        # Calcular interés del mes
                        interes_mes = saldo_actual * tasa_mensual_tc
                        
                        # Determinar pago (no puede ser mayor al saldo + intereses)
                        pago_efectivo = min(pago_mensual_tc, saldo_actual + interes_mes)
                        
                        # Calcular capital pagado
                        capital_pagado = pago_efectivo - interes_mes
                        
                        # Actualizar saldo
                        saldo_actual = max(0, saldo_actual - capital_pagado)
                        
                        total_pagado_tc += pago_efectivo
                        total_intereses_tc += interes_mes
                        
                        pagos_tc.append({
                            'Mes': meses_pago,
                            'Pago': pago_efectivo,
                            'Interés': interes_mes,
                            'Capital': capital_pagado,
                            'Saldo Restante': saldo_actual
                        })
                    
                    # Mostrar resultados
                    if meses_pago >= 360:
                        st.warning(f"⏰ Tiempo de pago muy largo: {meses_pago/12:.1f} años")
                    
                    col_m1, col_m2, col_m3 = st.columns(3)
                    with col_m1:
                        st.metric("Meses para pagar", meses_pago)
                    with col_m2:
                        st.metric("Total de intereses", f"${total_intereses_tc:,.2f}")
                    with col_m3:
                        st.metric("Total pagado", f"${total_pagado_tc:,.2f}")
                    
                    # Mostrar tabla de pagos (primeros 12 meses)
                    df_tarjeta = pd.DataFrame(pagos_tc[:12])
                    
                    st.markdown("**Cronograma de Pagos (Primeros 12 meses):**")
                    st.dataframe(
                        df_tarjeta.style.format({
                            'Pago': '${:,.2f}',
                            'Interés': '${:,.2f}',
                            'Capital': '${:,.2f}',
                            'Saldo Restante': '${:,.2f}'
                        }),
                        use_container_width=True
                    )
        
        with tab4:
            st.subheader("📊 Comparador de Opciones de Inversión")
            
            st.markdown("""
            Compara diferentes opciones de inversión side-by-side para tomar la mejor decisión.
            """)
            
            col1, col2, col3 = st.columns(3)
            
            opciones = []
            for i, col in enumerate([col1, col2, col3], 1):
                with col:
                    st.markdown(f"**Opción {i}:**")
                    nombre = st.text_input(f"Nombre", value=f"Inversión {i}", key=f"comp_nombre_{i}")
                    capital = st.number_input(f"Capital inicial ($)", value=10000, key=f"comp_capital_{i}")
                    rentabilidad = st.slider(f"Rentabilidad anual (%)", 1.0, 20.0, 5.0 + i*2, key=f"comp_rent_{i}")
                    años = st.selectbox(f"Años", [1, 3, 5, 10, 15, 20], index=2, key=f"comp_años_{i}")
                    
                    # Calcular valor final
                    valor_final = capital * (1 + rentabilidad/100) ** años
                    ganancia = valor_final - capital
                    
                    st.metric("Valor Final", f"${valor_final:,.2f}")
                    st.metric("Ganancia", f"${ganancia:,.2f}")
                    
                    opciones.append({
                        'Nombre': nombre,
                        'Capital Inicial': capital,
                        'Rentabilidad (%)': rentabilidad,
                        'Años': años,
                        'Valor Final': valor_final,
                        'Ganancia': ganancia,
                        'ROI (%)': (ganancia / capital) * 100
                    })
            
            # Tabla comparativa
            df_comparacion = pd.DataFrame(opciones)
            st.markdown("### 📈 Comparación de Resultados")
            st.dataframe(
                df_comparacion.style.format({
                    'Capital Inicial': '${:,.2f}',
                    'Rentabilidad (%)': '{:.1f}%',
                    'Valor Final': '${:,.2f}',
                    'Ganancia': '${:,.2f}',
                    'ROI (%)': '{:.1f}%'
                }).highlight_max(subset=['Valor Final', 'Ganancia', 'ROI (%)'], color='lightgreen'),
                use_container_width=True
            )
            
            # Gráfico de barras comparativo
            fig = px.bar(
                df_comparacion,
                x='Nombre',
                y=['Capital Inicial', 'Ganancia'],
                title="Comparación Visual de Inversiones",
                barmode='stack',
                color_discrete_map={
                    'Capital Inicial': 'lightblue',
                    'Ganancia': 'lightgreen'
                }
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab5:
            mostrar_codigo_fuente_calculadora()
        
        # Sección de consejos
        st.markdown("---")
        with st.expander("💡 Consejos Financieros", expanded=False):
            st.markdown("""
            ### 🎯 Consejos para el Éxito Financiero:
            
            **💰 Para Préstamos:**
            - Compara tasas de diferentes instituciones
            - Considera pagar más del mínimo para reducir intereses
            - El pie inicial reduce significativamente el costo total
            
            **📈 Para Inversiones:**
            - La constancia en los aportes es clave
            - El tiempo es tu mejor aliado (interés compuesto)
            - Diversifica tus inversiones
            
            **💳 Para Tarjetas de Crédito:**
            - Paga siempre más del mínimo
            - Evita usar toda la línea de crédito
            - Considera transferir saldo a tasas más bajas
            
            **🎯 General:**
            - Ten un fondo de emergencia (3-6 meses de gastos)
            - Automatiza tus inversiones
            - Revisa y ajusta tu estrategia regularmente
            """)
        
        # Footer con información adicional
        st.markdown("---")
        st.info("""
        🔧 **Tecnologías utilizadas en esta app:**
        - **Streamlit**: Framework principal
        - **Plotly**: Gráficos interactivos
        - **Pandas**: Manejo de datos
        - **Numpy**: Cálculos matemáticos
        
        📊 Esta calculadora es solo para fines educativos. Consulta siempre con un asesor financiero certificado.
        """)

def mostrar_codigo_fuente_calculadora():
    """Muestra el código fuente y explicaciones didácticas de la calculadora financiera."""
    
    st.subheader("🔍 Código Fuente y Explicaciones Didácticas")
    st.markdown("""
    Aquí puedes ver y entender cómo está construida cada calculadora financiera,
    con explicaciones detalladas de cada componente.
    """)
    
    # Selector de aplicación
    app_selector = st.selectbox(
        "Selecciona la aplicación para ver su código:",
        [
            "🏠 Calculadora de Préstamo Hipotecario",
            "📈 Calculadora de Inversión Compuesta", 
            "💳 Calculadora de Tarjeta de Crédito",
            "📊 Comparador de Inversiones"
        ],
        key="calc_code_selector"
    )
    
    if app_selector == "🏠 Calculadora de Préstamo Hipotecario":
        mostrar_codigo_hipoteca()
    elif app_selector == "📈 Calculadora de Inversión Compuesta":
        mostrar_codigo_inversion()
    elif app_selector == "💳 Calculadora de Tarjeta de Crédito":
        mostrar_codigo_tarjeta()
    elif app_selector == "📊 Comparador de Inversiones":
        mostrar_codigo_comparador()

def mostrar_codigo_hipoteca():
    """Muestra el código y explicación de la calculadora de hipoteca."""
    
    st.markdown("### 🏠 Calculadora de Préstamo Hipotecario")
    st.markdown("""
    Esta calculadora implementa la fórmula estándar de amortización de préstamos
    y genera una tabla detallada de pagos mensuales.
    """)
    
    with st.expander("📋 Explicación del Algoritmo", expanded=True):
        st.markdown("""
        **Conceptos Clave:**
        1. **Tasa Mensual**: Se convierte la tasa anual a mensual dividiéndola entre 12
        2. **Fórmula de Pago**: Utiliza la fórmula de amortización estándar
        3. **Tabla de Amortización**: Calcula capital e intereses para cada período
        
        **Fórmula Principal:**
        ```
        Pago Mensual = P × [r(1+r)^n] / [(1+r)^n - 1]
        ```
        Donde:
        - P = Monto financiado (préstamo - pie)
        - r = Tasa mensual (tasa_anual / 100 / 12)
        - n = Número de pagos (años × 12)
        """)
    
    with st.expander("💻 Código de Parámetros de Entrada", expanded=False):
        st.code("""
# Configuración de inputs para el préstamo hipotecario
monto_prestamo = st.number_input(
    "Monto del préstamo ($)",
    min_value=10000,
    max_value=1000000,
    value=200000,
    step=5000,
    key="hipoteca_monto"
)

tasa_anual = st.slider(
    "Tasa de interés anual (%)",
    min_value=1.0,
    max_value=15.0,
    value=4.5,
    step=0.1,
    key="hipoteca_tasa"
)

años = st.selectbox(
    "Años del préstamo",
    [15, 20, 25, 30],
    index=3,
    key="hipoteca_años"
)

pie_inicial = st.number_input(
    "Pie inicial ($)",
    min_value=0,
    max_value=monto_prestamo,
    value=int(monto_prestamo * 0.2),
    step=1000,
    key="hipoteca_pie"
)
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - `number_input`: Para valores monetarios con validaciones de rango
        - `slider`: Para la tasa de interés con pasos decimales
        - `selectbox`: Para años con opciones predefinidas
        - `key`: Identificadores únicos para evitar conflictos entre widgets
        """)
    
    with st.expander("🧮 Código de Cálculos Financieros", expanded=False):
        st.code("""
# Cálculos principales de la hipoteca
tasa_mensual = tasa_anual / 100 / 12
num_pagos = años * 12
monto_financiado = monto_prestamo - pie_inicial

if monto_financiado > 0:
    # Fórmula de pago mensual (amortización francesa)
    pago_mensual = monto_financiado * (tasa_mensual * (1 + tasa_mensual) ** num_pagos) / ((1 + tasa_mensual) ** num_pagos - 1)
    total_pagado = pago_mensual * num_pagos
    total_intereses = total_pagado - monto_financiado
    
    # Crear tabla de amortización
    amortizacion = []
    saldo_restante = monto_financiado
    
    for mes in range(1, min(13, num_pagos + 1)):
        interes_mes = saldo_restante * tasa_mensual
        capital_mes = pago_mensual - interes_mes
        saldo_restante -= capital_mes
        
        amortizacion.append({
            'Mes': mes,
            'Pago Total': pago_mensual,
            'Capital': capital_mes,
            'Interés': interes_mes,
            'Saldo Restante': saldo_restante
        })
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **Conversión de tasas**: Anual → Mensual dividiendo entre 12
        - **Fórmula de amortización**: Calcula el pago fijo mensual
        - **Loop de amortización**: Para cada mes calcula interés y capital
        - **Interés mensual**: Saldo restante × tasa mensual
        - **Capital mensual**: Pago total - interés del mes
        """)
    
    with st.expander("📊 Código de Visualización", expanded=False):
        st.code("""
# Mostrar métricas principales
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric("Pago Mensual", f"${pago_mensual:,.2f}")
with col_m2:
    st.metric("Total de Intereses", f"${total_intereses:,.2f}")
with col_m3:
    st.metric("Total Pagado", f"${total_pagado:,.2f}")

# Crear DataFrame y mostrar tabla formateada
df_amortizacion = pd.DataFrame(amortizacion)

st.dataframe(
    df_amortizacion.style.format({
        'Pago Total': '${:,.2f}',
        'Capital': '${:,.2f}',
        'Interés': '${:,.2f}',
        'Saldo Restante': '${:,.2f}'
    }),
    use_container_width=True
)

# Gráfico de evolución Capital vs Interés
fig = px.line(
    df_amortizacion,
    x='Mes',
    y=['Capital', 'Interés'],
    title="Evolución del Pago: Capital vs Interés",
    labels={'value': 'Monto ($)', 'variable': 'Tipo'}
)
st.plotly_chart(fig, use_container_width=True)
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **st.metric**: Muestra valores clave con formato monetario
        - **st.columns**: Organiza métricas en columnas
        - **DataFrame.style.format**: Formatea números como moneda
        - **px.line**: Gráfico interactivo para mostrar tendencias
        - **use_container_width**: Hace que elementos ocupen todo el ancho
        """)

def mostrar_codigo_inversion():
    """Muestra el código y explicación de la calculadora de inversión."""
    
    st.markdown("### 📈 Calculadora de Inversión con Interés Compuesto")
    st.markdown("""
    Esta calculadora modela el crecimiento de una inversión con aportes regulares
    y interés compuesto, mostrando la evolución temporal del capital.
    """)
    
    with st.expander("📋 Explicación del Algoritmo", expanded=True):
        st.markdown("""
        **Conceptos Clave:**
        1. **Interés Compuesto**: Los intereses generan más intereses
        2. **Aportes Regulares**: Inversiones adicionales periódicas
        3. **Cálculo Período a Período**: Simula mes a mes el crecimiento
        
        **Fórmulas Utilizadas:**
        ```
        Valor Futuro = Capital × (1 + r)^t + Aporte × [((1+r)^t - 1) / r]
        ```
        Donde:
        - r = Rentabilidad mensual
        - t = Tiempo en meses
        - Aporte = Contribución mensual
        """)
    
    with st.expander("💻 Código de Simulación de Inversión", expanded=False):
        st.code("""
# Parámetros de inversión
capital_inicial = st.number_input("Capital inicial ($)", ...)
aporte_mensual = st.number_input("Aporte mensual ($)", ...)
rentabilidad_anual = st.slider("Rentabilidad esperada (%)", ...)
años_inversion = st.selectbox("Años de inversión", ...)

# Cálculos de proyección
rentabilidad_mensual = rentabilidad_anual / 100 / 12
meses_total = años_inversion * 12

# Simulación mes a mes
proyeccion = []
capital_acumulado = capital_inicial

for mes in range(1, meses_total + 1):
    # Rendimiento del mes
    rendimiento_mes = capital_acumulado * rentabilidad_mensual
    
    # Agregar aporte mensual
    capital_acumulado += aporte_mensual + rendimiento_mes
    
    # Calcular totales
    total_aportado = capital_inicial + (aporte_mensual * mes)
    ganancia_total = capital_acumulado - total_aportado
    
    proyeccion.append({
        'Mes': mes,
        'Capital Acumulado': capital_acumulado,
        'Total Aportado': total_aportado,
        'Ganancia': ganancia_total,
        'Rendimiento Mes': rendimiento_mes
    })
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **Simulación iterativa**: Calcula mes a mes para mayor precisión
        - **Rentabilidad mensual**: Convierte anual a mensual
        - **Capital acumulado**: Se reinvierte automáticamente
        - **Seguimiento de aportes**: Diferencia entre capital y aportes
        """)
    
    with st.expander("📊 Código de Gráficos Avanzados", expanded=False):
        st.code("""
# Crear DataFrame para visualización
df_proyeccion = pd.DataFrame(proyeccion)

# Filtrar datos para mostrar (cada 6 meses si es muy largo)
if len(df_proyeccion) > 60:
    df_chart = df_proyeccion[df_proyeccion['Mes'] % 6 == 0].copy()
else:
    df_chart = df_proyeccion.copy()

# Gráfico de área apilada
fig = px.area(
    df_chart,
    x='Mes',
    y=['Total Aportado', 'Ganancia'],
    title="Proyección de Inversión con Interés Compuesto",
    color_discrete_map={
        'Total Aportado': 'lightblue',
        'Ganancia': 'lightgreen'
    }
)
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **Filtrado de datos**: Reduce puntos para mejor visualización
        - **px.area**: Gráfico de área apilada para mostrar composición
        - **color_discrete_map**: Personaliza colores para claridad
        - **height**: Controla la altura del gráfico
        """)

def mostrar_codigo_tarjeta():
    """Muestra el código y explicación de la calculadora de tarjeta de crédito."""
    
    st.markdown("### 💳 Calculadora de Tarjeta de Crédito")
    st.markdown("""
    Esta calculadora simula diferentes estrategias de pago de tarjeta de crédito
    y muestra el impacto de pagar solo el mínimo vs. pagos fijos más altos.
    """)
    
    with st.expander("📋 Explicación del Algoritmo", expanded=True):
        st.markdown("""
        **Conceptos Clave:**
        1. **Pago Mínimo**: Usualmente 2-5% del saldo o monto fijo
        2. **Interés Mensual**: Se capitaliza mensualmente
        3. **Amortización Variable**: El pago reduce según el saldo
        
        **Cálculo de Intereses:**
        ```
        Interés Mensual = Saldo × (Tasa Anual / 12)
        ```
        """)
    
    with st.expander("💻 Código de Validaciones Críticas", expanded=False):
        st.code("""
# Cálculos de tarjeta de crédito
tasa_mensual_tc = tasa_anual_tc / 100 / 12

# Validar que el pago sea suficiente
interes_minimo_mensual = saldo_inicial * tasa_mensual_tc

if pago_mensual_tc <= interes_minimo_mensual:
    st.error('''
    ⚠️ **ALERTA**: Tu pago mensual es menor o igual al interés mensual.
    
    **Esto significa que tu deuda NUNCA se pagará y seguirá creciendo.**
    
    💡 **Pago mínimo recomendado**: Recomendación calculada
    ''')
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **Validación crítica**: Detecta pagos insuficientes
        - **st.error**: Alerta visual prominente
        - **Cálculo preventivo**: Evita loops infinitos
        - **Recomendación automática**: Sugiere pago mínimo viable
        """)
    
    with st.expander("🔄 Código de Simulación de Pagos", expanded=False):
        st.code("""
# Simulación de pagos
saldo_actual = saldo_inicial
meses_pago = 0
total_pagado_tc = 0
total_intereses_tc = 0

pagos_tc = []

while saldo_actual > 0.01 and meses_pago < 360:  # Max 30 años
    meses_pago += 1
    
    # Calcular interés del mes
    interes_mes = saldo_actual * tasa_mensual_tc
    
    # Determinar pago (no puede ser mayor al saldo + intereses)
    pago_efectivo = min(pago_mensual_tc, saldo_actual + interes_mes)
    
    # Calcular capital pagado
    capital_pagado = pago_efectivo - interes_mes
    
    # Actualizar saldo
    saldo_actual = max(0, saldo_actual - capital_pagado)
    
    total_pagado_tc += pago_efectivo
    total_intereses_tc += interes_mes
    
    pagos_tc.append({
        'Mes': meses_pago,
        'Pago': pago_efectivo,
        'Interés': interes_mes,
        'Capital': capital_pagado,
        'Saldo Restante': saldo_actual
    })
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **While loop**: Continúa hasta saldar la deuda
        - **Límite de iteraciones**: Máximo 360 meses (30 años)
        - **Pago efectivo**: No puede exceder saldo + intereses
        - **Acumulación de totales**: Seguimiento completo de pagos
        - **max(0, ...)**: Evita saldos negativos
        """)

def mostrar_codigo_comparador():
    """Muestra el código y explicación del comparador de inversiones."""
    
    st.markdown("### 📊 Comparador de Opciones de Inversión")
    st.markdown("""
    Esta herramienta permite comparar múltiples opciones de inversión
    side-by-side con cálculos automatizados y visualizaciones comparativas.
    """)
    
    with st.expander("📋 Explicación del Algoritmo", expanded=True):
        st.markdown("""
        **Conceptos Clave:**
        1. **Comparación Multi-opción**: Hasta 3 inversiones simultáneas
        2. **ROI (Return on Investment)**: Rendimiento sobre inversión
        3. **Valor Futuro Simple**: Sin aportes adicionales
        4. **Ranking Automático**: Resalta mejores opciones
        
        **Fórmulas:**
        ```
        Valor Final = Capital × (1 + rentabilidad)^años
        ROI = (Ganancia / Capital Inicial) × 100
        ```
        """)
    
    with st.expander("💻 Código de Comparación Dinámica", expanded=False):
        st.code("""
# Crear columnas para 3 opciones
col1, col2, col3 = st.columns(3)

opciones = []
for i, col in enumerate([col1, col2, col3], 1):
    with col:
        st.markdown(f"**Opción {i}:**")
        
        # Inputs para cada opción
        nombre = st.text_input(f"Nombre", value=f"Inversión {i}", key=f"comp_nombre_{i}")
        capital = st.number_input(f"Capital inicial ($)", value=10000, key=f"comp_capital_{i}")
        rentabilidad = st.slider(f"Rentabilidad anual (%)", 1.0, 20.0, 5.0 + i*2, key=f"comp_rent_{i}")
        años = st.selectbox(f"Años", [1, 3, 5, 10, 15, 20], index=2, key=f"comp_años_{i}")
        
        # Calcular resultados inmediatamente
        valor_final = capital * (1 + rentabilidad/100) ** años
        ganancia = valor_final - capital
        
        # Mostrar métricas en tiempo real
        st.metric("Valor Final", f"${valor_final:,.2f}")
        st.metric("Ganancia", f"${ganancia:,.2f}")
        
        # Almacenar datos para comparación
        opciones.append({
            'Nombre': nombre,
            'Capital Inicial': capital,
            'Rentabilidad (%)': rentabilidad,
            'Años': años,
            'Valor Final': valor_final,
            'Ganancia': ganancia,
            'ROI (%)': (ganancia / capital) * 100
        })
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **Loop dinámico**: Genera widgets para múltiples opciones
        - **Keys únicos**: Evita conflictos entre widgets similares
        - **Cálculo inmediato**: Actualiza resultados en tiempo real
        - **Estructura de datos**: Lista de diccionarios para fácil manejo
        """)
    
    with st.expander("📊 Código de Tabla Comparativa Avanzada", expanded=False):
        st.code("""
# Crear DataFrame comparativo
df_comparacion = pd.DataFrame(opciones)

# Tabla con formato y highlighting
st.dataframe(
    df_comparacion.style.format({
        'Capital Inicial': '${:,.2f}',
        'Rentabilidad (%)': '{:.1f}%',
        'Valor Final': '${:,.2f}',
        'Ganancia': '${:,.2f}',
        'ROI (%)': '{:.1f}%'
    }).highlight_max(
        subset=['Valor Final', 'Ganancia', 'ROI (%)'], 
        color='lightgreen'
    ),
    use_container_width=True
)

# Gráfico de barras apiladas
fig = px.bar(
    df_comparacion,
    x='Nombre',
    y=['Capital Inicial', 'Ganancia'],
    title="Comparación Visual de Inversiones",
    barmode='stack',
    color_discrete_map={
        'Capital Inicial': 'lightblue',
        'Ganancia': 'lightgreen'
    }
)
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **DataFrame.style**: Permite formato y conditional formatting
        - **highlight_max**: Resalta automáticamente los mejores valores
        - **Barras apiladas**: Muestra composición capital vs ganancia
        - **Color mapping**: Colores consistentes para mejor UX
        """)

if __name__ == "__main__":
    run()
