import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

def run():
    """Módulo de Aplicaciones Completas - Sistema de Gestión de Inventario."""
    
    with st.container():
        st.title("📦 Clase 2: Sistema de Gestión de Inventario")
        st.markdown("""
        Construye un sistema completo de gestión de inventario con seguimiento de stock,
        alertas automáticas, análisis de ventas y predicción de demanda.
        """)
        
        # Inicializar datos de ejemplo en session_state
        if 'inventario_data' not in st.session_state:
            st.session_state.inventario_data = generar_datos_inventario()
        
        if 'movimientos_data' not in st.session_state:
            st.session_state.movimientos_data = generar_movimientos()
          # Pestañas del sistema
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Dashboard Principal",
            "📦 Gestión de Productos",
            "📈 Movimientos de Stock",
            "⚠️ Alertas y Reportes",
            "🔮 Predicción de Demanda",
            "🔍 Ver Código Fuente"
        ])
        
        with tab1:
            render_dashboard_principal()
        
        with tab2:
            render_gestion_productos()
        
        with tab3:
            render_movimientos_stock()
        
        with tab4:
            render_alertas_reportes()
        
        with tab5:
            render_prediccion_demanda()

        
        with tab6:
            mostrar_codigo_fuente_inventario()

def generar_datos_inventario():
    """Genera datos de ejemplo para el inventario."""
    np.random.seed(42)
    categorias = ['Electrónicos', 'Ropa', 'Hogar', 'Deportes', 'Libros']
    proveedores = ['Proveedor A', 'Proveedor B', 'Proveedor C', 'Proveedor D']
    
    productos = []
    for i in range(50):
        categoria = np.random.choice(categorias)
        precio_base = np.random.uniform(10, 500)
        stock_actual = np.random.randint(0, 100)
        stock_minimo = np.random.randint(5, 20)
        
        productos.append({
            'ID': f'PROD{i+1:03d}',
            'Nombre': f'Producto {i+1}',
            'Categoría': categoria,
            'Proveedor': np.random.choice(proveedores),
            'Precio Compra': round(precio_base, 2),
            'Precio Venta': round(precio_base * np.random.uniform(1.3, 2.0), 2),
            'Stock Actual': stock_actual,
            'Stock Mínimo': stock_minimo,
            'Stock Máximo': stock_minimo * np.random.randint(3, 8),
            'Estado': 'Crítico' if stock_actual < stock_minimo else 'Normal' if stock_actual < stock_minimo * 2 else 'Óptimo',
            'Última Actualización': datetime.now() - timedelta(days=np.random.randint(0, 30))
        })
    
    return pd.DataFrame(productos)

def generar_movimientos():
    """Genera datos de movimientos de stock."""
    np.random.seed(42)
    movimientos = []
    
    for i in range(200):
        tipo = np.random.choice(['Entrada', 'Salida'], p=[0.3, 0.7])
        cantidad = np.random.randint(1, 20)
        
        movimientos.append({
            'ID Movimiento': f'MOV{i+1:04d}',
            'Producto ID': f'PROD{np.random.randint(1, 51):03d}',
            'Tipo': tipo,
            'Cantidad': cantidad,
            'Fecha': datetime.now() - timedelta(days=np.random.randint(0, 90)),
            'Usuario': f'Usuario{np.random.randint(1, 6)}',
            'Motivo': np.random.choice([
                'Venta', 'Compra', 'Ajuste', 'Devolución', 'Merma', 'Transferencia'
            ])
        })
    
    return pd.DataFrame(movimientos)

def render_dashboard_principal():
    """Renderiza el dashboard principal."""
    st.subheader("📊 Dashboard Principal")
    
    df_inventario = st.session_state.inventario_data
    df_movimientos = st.session_state.movimientos_data
    
    # KPIs principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_productos = len(df_inventario)
        st.metric("Total Productos", total_productos)
    
    with col2:
        valor_inventario = (df_inventario['Stock Actual'] * df_inventario['Precio Compra']).sum()
        st.metric("Valor Inventario", f"${valor_inventario:,.2f}")
    
    with col3:
        productos_criticos = len(df_inventario[df_inventario['Estado'] == 'Crítico'])
        st.metric("Productos Críticos", productos_criticos, delta=f"-{productos_criticos}")
    
    with col4:
        movimientos_hoy = len(df_movimientos[df_movimientos['Fecha'].dt.date == datetime.now().date()])
        st.metric("Movimientos Hoy", movimientos_hoy)
    
    st.markdown("---")
    
    # Gráficos principales
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribución por categoría
        dist_categoria = df_inventario.groupby('Categoría').agg({
            'Stock Actual': 'sum',
            'Precio Compra': lambda x: (x * df_inventario.loc[x.index, 'Stock Actual']).sum()
        }).reset_index()
        dist_categoria.columns = ['Categoría', 'Cantidad', 'Valor']
        
        fig_categoria = px.pie(
            dist_categoria,
            values='Valor',
            names='Categoría',
            title="Distribución de Valor por Categoría"
        )
        st.plotly_chart(fig_categoria, use_container_width=True)
    
    with col2:
        # Estado del inventario
        estado_count = df_inventario['Estado'].value_counts()
        
        fig_estado = px.bar(
            x=estado_count.index,
            y=estado_count.values,
            title="Estado del Inventario",
            color=estado_count.index,
            color_discrete_map={
                'Crítico': 'red',
                'Normal': 'orange', 
                'Óptimo': 'green'
            }
        )
        st.plotly_chart(fig_estado, use_container_width=True)
    
    # Tabla de productos críticos
    productos_criticos = df_inventario[df_inventario['Estado'] == 'Crítico']
    if not productos_criticos.empty:
        st.markdown("### ⚠️ Productos que Requieren Atención Inmediata")
        st.dataframe(
            productos_criticos[['ID', 'Nombre', 'Categoría', 'Stock Actual', 'Stock Mínimo']].style.format({
                'Stock Actual': '{:,}',
                'Stock Mínimo': '{:,}'
            }),
            use_container_width=True
        )
    
    # Movimientos recientes
    st.markdown("### 📋 Movimientos Recientes")
    movimientos_recientes = df_movimientos.nlargest(10, 'Fecha')[
        ['ID Movimiento', 'Producto ID', 'Tipo', 'Cantidad', 'Fecha', 'Motivo']
    ]
    st.dataframe(movimientos_recientes, use_container_width=True)

def render_gestion_productos():
    """Renderiza la gestión de productos."""
    st.subheader("📦 Gestión de Productos")
    
    df_inventario = st.session_state.inventario_data
    
    # Controles de filtrado
    col1, col2, col3 = st.columns(3)
    
    with col1:
        categoria_filter = st.selectbox(
            "Filtrar por categoría",
            ['Todas'] + list(df_inventario['Categoría'].unique()),
            key="prod_categoria_filter"
        )
    
    with col2:
        estado_filter = st.selectbox(
            "Filtrar por estado",
            ['Todos'] + list(df_inventario['Estado'].unique()),
            key="prod_estado_filter"
        )
    
    with col3:
        buscar = st.text_input("Buscar producto", key="prod_buscar")
    
    # Aplicar filtros
    df_filtrado = df_inventario.copy()
    
    if categoria_filter != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Categoría'] == categoria_filter]
    
    if estado_filter != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Estado'] == estado_filter]
    
    if buscar:
        df_filtrado = df_filtrado[
            df_filtrado['Nombre'].str.contains(buscar, case=False) |
            df_filtrado['ID'].str.contains(buscar, case=False)
        ]
    
    # Botones de acción
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("➕ Nuevo Producto", key="nuevo_producto"):
            st.session_state.show_new_product_form = True
    
    with col2:
        if st.button("📊 Exportar", key="exportar_productos"):
            csv = df_filtrado.to_csv(index=False)
            st.download_button(
                label="⬇️ Descargar CSV",
                data=csv,
                file_name=f"inventario_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
      # Mostrar formulario de nuevo producto si se activó
    if getattr(st.session_state, 'show_new_product_form', False):
        with st.expander("➕ Agregar Nuevo Producto", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nuevo_id = st.text_input("ID del Producto", value=f"PROD{len(df_inventario)+1:03d}")
                nuevo_nombre = st.text_input("Nombre del Producto")
                nueva_categoria = st.selectbox("Categoría", df_inventario['Categoría'].unique())
                nuevo_proveedor = st.selectbox("Proveedor", df_inventario['Proveedor'].unique())
            
            with col2:
                nuevo_precio_compra = st.number_input("Precio de Compra", min_value=0.01, value=10.0, format="%.2f")
                nuevo_precio_venta = st.number_input("Precio de Venta", min_value=0.01, value=15.0, format="%.2f")
                nuevo_stock_inicial = st.number_input("Stock Inicial", min_value=0, value=10, step=1, format="%d")
                nuevo_stock_minimo = st.number_input("Stock Mínimo", min_value=1, value=5, step=1, format="%d")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("✅ Guardar Producto"):
                    # Agregar nuevo producto
                    nuevo_producto = {
                        'ID': nuevo_id,
                        'Nombre': nuevo_nombre,
                        'Categoría': nueva_categoria,
                        'Proveedor': nuevo_proveedor,
                        'Precio Compra': nuevo_precio_compra,
                        'Precio Venta': nuevo_precio_venta,
                        'Stock Actual': nuevo_stock_inicial,
                        'Stock Mínimo': nuevo_stock_minimo,
                        'Stock Máximo': nuevo_stock_minimo * 4,
                        'Estado': 'Normal',
                        'Última Actualización': datetime.now()
                    }
                    
                    # Agregar al DataFrame
                    st.session_state.inventario_data = pd.concat([
                        st.session_state.inventario_data,
                        pd.DataFrame([nuevo_producto])
                    ], ignore_index=True)
                    
                    st.success("✅ Producto agregado exitosamente!")
                    st.session_state.show_new_product_form = False
                    st.rerun()
            
            with col_btn2:
                if st.button("❌ Cancelar"):
                    st.session_state.show_new_product_form = False
                    st.rerun()
      # Tabla principal de productos
    st.markdown("### 📋 Lista de Productos")
    
    st.dataframe(
        df_filtrado.style.format({
            'Precio Compra': '${:.2f}',
            'Precio Venta': '${:.2f}',
            'Stock Actual': '{:,}',
            'Stock Mínimo': '{:,}',
            'Stock Máximo': '{:,}'
        }).map(
            lambda x: 'background-color: #ffcccc' if x == 'Crítico' else '', 
            subset=['Estado']
        ),
        use_container_width=True
    )
    
    # Estadísticas rápidas
    st.markdown("### 📈 Estadísticas Rápidas")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        precio_promedio = df_filtrado['Precio Venta'].mean()
        st.metric("Precio Promedio", f"${precio_promedio:.2f}")
    
    with col2:
        stock_total = df_filtrado['Stock Actual'].sum()
        st.metric("Stock Total", f"{stock_total:,}")
    
    with col3:
        margen_promedio = ((df_filtrado['Precio Venta'] - df_filtrado['Precio Compra']) / df_filtrado['Precio Compra'] * 100).mean()
        st.metric("Margen Promedio", f"{margen_promedio:.1f}%")

def render_movimientos_stock():
    """Renderiza la gestión de movimientos de stock."""
    st.subheader("📈 Movimientos de Stock")
    
    df_movimientos = st.session_state.movimientos_data
    df_inventario = st.session_state.inventario_data
    
    # Controles para nuevo movimiento
    with st.expander("➕ Registrar Nuevo Movimiento", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            producto_id = st.selectbox(
                "Producto",
                df_inventario['ID'].tolist(),
                key="mov_producto_id"
            )
            tipo_movimiento = st.selectbox(
                "Tipo de Movimiento",
                ["Entrada", "Salida"],
                key="mov_tipo"            )
            
            cantidad = st.number_input(
                "Cantidad",
                min_value=1,
                value=1,
                step=1,
                format="%d",
                key="mov_cantidad"
            )
        
        with col2:
            motivo = st.selectbox(
                "Motivo",
                ["Venta", "Compra", "Ajuste", "Devolución", "Merma", "Transferencia"],
                key="mov_motivo"
            )
            usuario = st.text_input(
                "Usuario",
                value="Usuario1",
                key="mov_usuario"
            )
        
        if st.button("✅ Registrar Movimiento"):
            # Crear nuevo movimiento
            nuevo_movimiento = {
                'ID Movimiento': f'MOV{len(df_movimientos)+1:04d}',
                'Producto ID': producto_id,
                'Tipo': tipo_movimiento,
                'Cantidad': cantidad,
                'Fecha': datetime.now(),
                'Usuario': usuario,
                'Motivo': motivo
            }
            
            # Agregar movimiento
            st.session_state.movimientos_data = pd.concat([
                st.session_state.movimientos_data,
                pd.DataFrame([nuevo_movimiento])
            ], ignore_index=True)
            
            # Actualizar stock del producto
            idx = st.session_state.inventario_data[
                st.session_state.inventario_data['ID'] == producto_id
            ].index[0]
            
            if tipo_movimiento == "Entrada":
                st.session_state.inventario_data.loc[idx, 'Stock Actual'] += cantidad
            else:
                st.session_state.inventario_data.loc[idx, 'Stock Actual'] -= cantidad
            
            # Actualizar estado del producto
            stock_actual = st.session_state.inventario_data.loc[idx, 'Stock Actual']
            stock_minimo = st.session_state.inventario_data.loc[idx, 'Stock Mínimo']
            
            if stock_actual < stock_minimo:
                estado = 'Crítico'
            elif stock_actual < stock_minimo * 2:
                estado = 'Normal'
            else:
                estado = 'Óptimo'
            
            st.session_state.inventario_data.loc[idx, 'Estado'] = estado
            st.session_state.inventario_data.loc[idx, 'Última Actualización'] = datetime.now()
            
            st.success("✅ Movimiento registrado exitosamente!")
            st.rerun()
    
    # Filtros para movimientos
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tipo_filter = st.selectbox(
            "Filtrar por tipo",
            ['Todos', 'Entrada', 'Salida'],
            key="mov_tipo_filter"
        )
    
    with col2:
        dias_filter = st.selectbox(
            "Período",
            [7, 30, 90, 365],
            format_func=lambda x: f"Últimos {x} días",
            key="mov_dias_filter"
        )
    
    with col3:
        producto_filter = st.selectbox(
            "Filtrar por producto",
            ['Todos'] + df_inventario['ID'].tolist(),
            key="mov_producto_filter"
        )
    
    # Aplicar filtros
    df_mov_filtrado = df_movimientos.copy()
    
    if tipo_filter != 'Todos':
        df_mov_filtrado = df_mov_filtrado[df_mov_filtrado['Tipo'] == tipo_filter]
    
    fecha_limite = datetime.now() - timedelta(days=dias_filter)
    df_mov_filtrado = df_mov_filtrado[df_mov_filtrado['Fecha'] >= fecha_limite]
    
    if producto_filter != 'Todos':
        df_mov_filtrado = df_mov_filtrado[df_mov_filtrado['Producto ID'] == producto_filter]
    
    # Gráfico de movimientos por día
    movimientos_por_dia = df_mov_filtrado.groupby([
        df_mov_filtrado['Fecha'].dt.date, 'Tipo'
    ])['Cantidad'].sum().reset_index()
    
    if not movimientos_por_dia.empty:
        fig_movimientos = px.line(
            movimientos_por_dia,
            x='Fecha',
            y='Cantidad',
            color='Tipo',
            title="Movimientos de Stock por Día",
            markers=True
        )
        st.plotly_chart(fig_movimientos, use_container_width=True)
    
    # Tabla de movimientos
    st.markdown("### 📋 Historial de Movimientos")
    st.dataframe(
        df_mov_filtrado.sort_values('Fecha', ascending=False),
        use_container_width=True
    )

def render_alertas_reportes():
    """Renderiza alertas y reportes."""
    st.subheader("⚠️ Alertas y Reportes")
    
    df_inventario = st.session_state.inventario_data
    df_movimientos = st.session_state.movimientos_data
    
    # Alertas automáticas
    st.markdown("### 🚨 Alertas Automáticas")
    
    # Stock crítico
    productos_criticos = df_inventario[df_inventario['Estado'] == 'Crítico']
    if not productos_criticos.empty:
        st.error(f"⚠️ **{len(productos_criticos)} productos** con stock crítico:")
        for _, producto in productos_criticos.iterrows():
            st.warning(f"- **{producto['Nombre']}** ({producto['ID']}): {producto['Stock Actual']} unidades (Mínimo: {producto['Stock Mínimo']})")
    else:
        st.success("✅ No hay productos con stock crítico")
    
    # Productos sin movimiento
    fecha_limite = datetime.now() - timedelta(days=30)
    productos_con_movimiento = df_movimientos[df_movimientos['Fecha'] >= fecha_limite]['Producto ID'].unique()
    productos_sin_movimiento = df_inventario[~df_inventario['ID'].isin(productos_con_movimiento)]
    
    if not productos_sin_movimiento.empty:
        st.warning(f"🔄 **{len(productos_sin_movimiento)} productos** sin movimiento en 30 días:")
        with st.expander("Ver productos sin movimiento"):
            st.dataframe(productos_sin_movimiento[['ID', 'Nombre', 'Categoría', 'Stock Actual']])
    
    # Reportes
    st.markdown("### 📊 Reportes Ejecutivos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Reporte por categoría
        reporte_categoria = df_inventario.groupby('Categoría').agg({
            'Stock Actual': 'sum',
            'Precio Compra': lambda x: (x * df_inventario.loc[x.index, 'Stock Actual']).sum(),
            'Precio Venta': lambda x: (x * df_inventario.loc[x.index, 'Stock Actual']).sum()
        }).reset_index()
        reporte_categoria.columns = ['Categoría', 'Cantidad Total', 'Valor Compra', 'Valor Venta']
        reporte_categoria['Margen Potencial'] = reporte_categoria['Valor Venta'] - reporte_categoria['Valor Compra']
        
        st.markdown("**Reporte por Categoría:**")
        st.dataframe(
            reporte_categoria.style.format({
                'Cantidad Total': '{:,}',
                'Valor Compra': '${:,.2f}',
                'Valor Venta': '${:,.2f}',
                'Margen Potencial': '${:,.2f}'
            }),
            use_container_width=True
        )
    
    with col2:
        # Reporte por proveedor
        reporte_proveedor = df_inventario.groupby('Proveedor').agg({
            'ID': 'count',
            'Stock Actual': 'sum',
            'Precio Compra': lambda x: (x * df_inventario.loc[x.index, 'Stock Actual']).sum()
        }).reset_index()
        reporte_proveedor.columns = ['Proveedor', 'Productos', 'Stock Total', 'Valor Total']
        
        st.markdown("**Reporte por Proveedor:**")
        st.dataframe(
            reporte_proveedor.style.format({
                'Stock Total': '{:,}',
                'Valor Total': '${:,.2f}'
            }),
            use_container_width=True
        )
    
    # Análisis de rotación
    st.markdown("### 🔄 Análisis de Rotación de Inventario")
    
    # Calcular rotación aproximada basada en movimientos de salida
    movimientos_salida = df_movimientos[df_movimientos['Tipo'] == 'Salida']
    rotacion_por_producto = movimientos_salida.groupby('Producto ID')['Cantidad'].sum()
    
    df_rotacion = df_inventario.copy()
    df_rotacion['Ventas 90 días'] = df_rotacion['ID'].map(rotacion_por_producto).fillna(0)
    df_rotacion['Días de Stock'] = np.where(
        df_rotacion['Ventas 90 días'] > 0,
        (df_rotacion['Stock Actual'] / df_rotacion['Ventas 90 días']) * 90,
        999  # Productos sin ventas
    )
    
    # Clasificar productos por rotación
    df_rotacion['Clasificación'] = pd.cut(
        df_rotacion['Días de Stock'],
        bins=[0, 30, 60, 180, 999],
        labels=['Rápida', 'Normal', 'Lenta', 'Sin Movimiento']
    )
    
    # Gráfico de clasificación de rotación
    rotacion_count = df_rotacion['Clasificación'].value_counts()
    fig_rotacion = px.pie(
        values=rotacion_count.values,
        names=rotacion_count.index,
        title="Clasificación por Rotación de Inventario"
    )
    st.plotly_chart(fig_rotacion, use_container_width=True)
    
    # Tabla de productos con rotación lenta
    productos_lenta_rotacion = df_rotacion[df_rotacion['Clasificación'].isin(['Lenta', 'Sin Movimiento'])]
    if not productos_lenta_rotacion.empty:
        st.markdown("**Productos con Rotación Lenta o Sin Movimiento:**")
        st.dataframe(
            productos_lenta_rotacion[['ID', 'Nombre', 'Categoría', 'Stock Actual', 'Días de Stock', 'Clasificación']].style.format({
                'Stock Actual': '{:,}',
                'Días de Stock': '{:.0f}'
            }),
            use_container_width=True
        )

def render_prediccion_demanda():
    """Renderiza la predicción de demanda."""
    st.subheader("🔮 Predicción de Demanda")
    
    st.markdown("""
    Utiliza análisis de tendencias históricas para predecir la demanda futura
    y optimizar los niveles de inventario.
    """)
    
    df_movimientos = st.session_state.movimientos_data
    df_inventario = st.session_state.inventario_data
    
    # Selector de producto para análisis
    producto_seleccionado = st.selectbox(
        "Selecciona un producto para análisis:",
        df_inventario['ID'].tolist(),
        key="pred_producto"
    )
    
    if producto_seleccionado:
        # Obtener datos del producto
        producto_info = df_inventario[df_inventario['ID'] == producto_seleccionado].iloc[0]
        movimientos_producto = df_movimientos[
            (df_movimientos['Producto ID'] == producto_seleccionado) &
            (df_movimientos['Tipo'] == 'Salida')
        ].copy()
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Información del Producto:**")
            st.write(f"**Nombre:** {producto_info['Nombre']}")
            st.write(f"**Categoría:** {producto_info['Categoría']}")
            st.write(f"**Stock Actual:** {producto_info['Stock Actual']}")
            st.write(f"**Stock Mínimo:** {producto_info['Stock Mínimo']}")
            st.write(f"**Precio:** ${producto_info['Precio Venta']:.2f}")
        
        with col2:
            if not movimientos_producto.empty:
                # Agregar movimientos por semana
                movimientos_producto['Semana'] = movimientos_producto['Fecha'].dt.to_period('W')
                ventas_semanales = movimientos_producto.groupby('Semana')['Cantidad'].sum()
                
                # Crear DataFrame para el gráfico
                df_ventas = pd.DataFrame({
                    'Semana': ventas_semanales.index.astype(str),
                    'Ventas': ventas_semanales.values
                })
                  # Gráfico de tendencia
                fig_tendencia = px.line(
                    df_ventas,
                    x='Semana',
                    y='Ventas',
                    title=f"Tendencia de Ventas - {producto_info['Nombre']}",
                    markers=True
                )
                fig_tendencia.update_layout(xaxis_tickangle=45)
                st.plotly_chart(fig_tendencia, use_container_width=True)
            else:
                st.warning("No hay datos de ventas suficientes para este producto")
        
        # Análisis predictivo simple
        if not movimientos_producto.empty and len(movimientos_producto) >= 4:
            st.markdown("### 📈 Análisis Predictivo")
            
            # Calcular estadísticas
            ventas_promedio_semanal = movimientos_producto.groupby(
                movimientos_producto['Fecha'].dt.to_period('W')
            )['Cantidad'].sum().mean()
            
            ventas_promedio_mensual = ventas_promedio_semanal * 4.33  # Semanas promedio por mes
            
            # Predicciones simples
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Demanda Semanal Promedio", f"{ventas_promedio_semanal:.1f} unidades")
            
            with col2:
                st.metric("Demanda Mensual Estimada", f"{ventas_promedio_mensual:.1f} unidades")
            
            with col3:
                dias_stock = producto_info['Stock Actual'] / (ventas_promedio_semanal / 7) if ventas_promedio_semanal > 0 else 999
                st.metric("Días de Stock Restantes", f"{dias_stock:.0f} días")
            
            # Recomendaciones
            st.markdown("### 💡 Recomendaciones")
            
            if dias_stock < 14:
                st.error("🚨 **Acción Inmediata Requerida**: Stock muy bajo, reabastecer urgentemente")
                cantidad_recomendada = max(ventas_promedio_mensual * 2, producto_info['Stock Mínimo'] * 3)
                st.info(f"💡 **Cantidad recomendada de reabastecimiento:** {cantidad_recomendada:.0f} unidades")
            elif dias_stock < 30:
                st.warning("⚠️ **Programar Reabastecimiento**: Considerar pedido en la próxima semana")
                cantidad_recomendada = ventas_promedio_mensual * 1.5
                st.info(f"💡 **Cantidad recomendada:** {cantidad_recomendada:.0f} unidades")
            else:
                st.success("✅ **Stock Adecuado**: Nivel de inventario óptimo")
            
            # Simulación de escenarios
            st.markdown("### 🎯 Simulación de Escenarios")
            
            aumento_demanda = st.slider(
                "Simular cambio en demanda (%)",
                -50, 100, 0,
                key="sim_demanda"
            )
            
            nueva_demanda_semanal = ventas_promedio_semanal * (1 + aumento_demanda/100)
            nuevos_dias_stock = producto_info['Stock Actual'] / (nueva_demanda_semanal / 7) if nueva_demanda_semanal > 0 else 999
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Nueva Demanda Semanal",
                    f"{nueva_demanda_semanal:.1f}",
                    delta=f"{nueva_demanda_semanal - ventas_promedio_semanal:.1f}"
                )
            with col2:
                st.metric(
                    "Nuevos Días de Stock",
                    f"{nuevos_dias_stock:.0f}",
                    delta=f"{nuevos_dias_stock - dias_stock:.0f}"
                )
        
        else:
            st.info("📊 Se necesitan más datos históricos para realizar predicciones precisas")
    
    # Análisis general de categorías
    st.markdown("---")
    st.markdown("### 📊 Análisis por Categoría")
    
    # Agrupar movimientos por categoría
    movimientos_con_categoria = df_movimientos.merge(
        df_inventario[['ID', 'Categoría']], 
        left_on='Producto ID', 
        right_on='ID'
    )
    
    movimientos_salida_categoria = movimientos_con_categoria[
        movimientos_con_categoria['Tipo'] == 'Salida'
    ]
    
    if not movimientos_salida_categoria.empty:
        # Ventas por categoría en los últimos 30 días
        fecha_limite = datetime.now() - timedelta(days=30)
        ventas_categoria_30d = movimientos_salida_categoria[
            movimientos_salida_categoria['Fecha'] >= fecha_limite
        ].groupby('Categoría')['Cantidad'].sum().sort_values(ascending=False)
        
        fig_categoria = px.bar(
            x=ventas_categoria_30d.index,
            y=ventas_categoria_30d.values,
            title="Ventas por Categoría (Últimos 30 días)",
            labels={'x': 'Categoría', 'y': 'Unidades Vendidas'}
        )
        st.plotly_chart(fig_categoria, use_container_width=True)
        
        # Tabla resumen por categoría
        resumen_categoria = df_inventario.groupby('Categoría').agg({
            'Stock Actual': 'sum',
            'ID': 'count'
        }).reset_index()
        resumen_categoria.columns = ['Categoría', 'Stock Total', 'Productos']
        
        # Agregar ventas
        resumen_categoria['Ventas 30d'] = resumen_categoria['Categoría'].map(ventas_categoria_30d).fillna(0)
        resumen_categoria['Rotación (días)'] = np.where(
            resumen_categoria['Ventas 30d'] > 0,
            (resumen_categoria['Stock Total'] / resumen_categoria['Ventas 30d']) * 30,
            999
        )
        
        st.markdown("**Resumen por Categoría:**")
        st.dataframe(
            resumen_categoria.style.format({
                'Stock Total': '{:,}',
                'Ventas 30d': '{:,}',
                'Rotación (días)': '{:.0f}'
            }),
            use_container_width=True
        )

if __name__ == "__main__":
    run()

def mostrar_codigo_fuente_inventario():
    """Muestra el código fuente y explicaciones didácticas del sistema de inventario."""
    
    st.subheader("🔍 Código Fuente y Explicaciones Didácticas")
    st.markdown("""
    Aquí puedes ver y entender cómo está construido cada componente del sistema de inventario,
    con explicaciones detalladas de cada funcionalidad.
    """)
    
    # Selector de componente
    componente_selector = st.selectbox(
        "Selecciona el componente para ver su código:",
        [
            "📊 Dashboard Principal",
            "📦 Gestión de Productos",
            "📈 Movimientos de Stock",
            "⚠️ Sistema de Alertas",
            "🔮 Predicción de Demanda",
            "🗂️ Estructura de Datos"
        ],
        key="inventario_code_selector"
    )
    
    if componente_selector == "📊 Dashboard Principal":
        mostrar_codigo_dashboard()
    elif componente_selector == "📦 Gestión de Productos":
        mostrar_codigo_productos()
    elif componente_selector == "📈 Movimientos de Stock":
        mostrar_codigo_movimientos()
    elif componente_selector == "⚠️ Sistema de Alertas":
        mostrar_codigo_alertas()
    elif componente_selector == "🔮 Predicción de Demanda":
        mostrar_codigo_prediccion()
    elif componente_selector == "🗂️ Estructura de Datos":
        mostrar_codigo_estructura()

def mostrar_codigo_dashboard():
    """Muestra el código del dashboard principal."""
    
    st.markdown("### 📊 Dashboard Principal del Sistema")
    st.markdown("""
    El dashboard proporciona una vista general del estado del inventario
    con métricas clave, gráficos de resumen y alertas visuales.
    """)
    
    with st.expander("📋 Explicación del Dashboard", expanded=True):
        st.markdown("""
        **Componentes Principales:**
        1. **Métricas de Resumen**: Total productos, valor inventario, alertas
        2. **Gráficos de Estado**: Distribución por categoría y estado de stock
        3. **Tablas Dinámicas**: Productos con bajo stock y más vendidos
        4. **Indicadores Visuales**: Colores y alertas para decisiones rápidas
        
        **Tecnologías Utilizadas:**
        - **session_state**: Para mantener datos entre interacciones
        - **métricas con delta**: Para mostrar cambios y tendencias
        - **gráficos plotly**: Para visualizaciones interactivas
        """)
    
    with st.expander("💻 Código de Métricas Principales", expanded=False):
        st.code("""
def render_dashboard_principal():
    st.markdown("## 📊 Dashboard del Sistema de Inventario")
    
    # Obtener datos del inventario
    df_inventario = pd.DataFrame(st.session_state.inventario_data)
    df_movimientos = pd.DataFrame(st.session_state.movimientos_data)
    
    # Calcular métricas principales
    total_productos = len(df_inventario)
    valor_total_inventario = (df_inventario['Stock Actual'] * df_inventario['Precio Unitario']).sum()
    productos_bajo_stock = len(df_inventario[df_inventario['Stock Actual'] <= df_inventario['Stock Mínimo']])
    productos_sin_stock = len(df_inventario[df_inventario['Stock Actual'] == 0])
    
    # Mostrar métricas en columnas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Productos", 
            total_productos,
            delta="Activo" if total_productos > 0 else "Sin productos"
        )
    
    with col2:
        st.metric(
            "Valor Total Inventario", 
            f"${valor_total_inventario:,.2f}",
            delta=f"{valor_total_inventario/total_productos:.2f} promedio" if total_productos > 0 else "0"
        )
    
    with col3:
        st.metric(
            "Productos Bajo Stock", 
            productos_bajo_stock,
            delta="⚠️ Crítico" if productos_bajo_stock > 5 else "✅ Normal",
            delta_color="inverse" if productos_bajo_stock > 5 else "normal"
        )
    
    with col4:
        st.metric(
            "Sin Stock", 
            productos_sin_stock,
            delta="🚨 Urgente" if productos_sin_stock > 0 else "✅ OK",
            delta_color="inverse" if productos_sin_stock > 0 else "normal"
        )
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **Cálculos agregados**: Suma, conteo y promedios de datos del inventario
        - **st.metric con delta**: Proporciona contexto adicional a las métricas
        - **delta_color**: Controla el color del indicador (normal/inverse)
        - **Validaciones**: Evita división por cero y maneja casos edge
        """)
    
    with st.expander("📊 Código de Gráficos del Dashboard", expanded=False):
        st.code("""
# Gráficos del dashboard
col1, col2 = st.columns(2)

with col1:
    # Gráfico de distribución por categoría
    categoria_counts = df_inventario['Categoría'].value_counts()
    
    fig_categoria = px.pie(
        values=categoria_counts.values,
        names=categoria_counts.index,
        title="Distribución de Productos por Categoría",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_categoria.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_categoria, use_container_width=True)

with col2:
    # Gráfico de estado de stock
    df_inventario['Estado Stock'] = df_inventario.apply(lambda row: 
        'Sin Stock' if row['Stock Actual'] == 0 
        else 'Bajo Stock' if row['Stock Actual'] <= row['Stock Mínimo']
        else 'Stock Normal', axis=1
    )
    
    estado_counts = df_inventario['Estado Stock'].value_counts()
    
    # Definir colores para cada estado
    colores_estado = {
        'Sin Stock': '#ff4444',      # Rojo
        'Bajo Stock': '#ffaa00',     # Naranja  
        'Stock Normal': '#44ff44'    # Verde
    }
    
    fig_estado = px.bar(
        x=estado_counts.index,
        y=estado_counts.values,
        title="Estado del Stock por Producto",
        color=estado_counts.index,
        color_discrete_map=colores_estado
    )
    fig_estado.update_layout(showlegend=False)
    st.plotly_chart(fig_estado, use_container_width=True)
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **px.pie**: Gráfico circular para mostrar proporciones
        - **apply con lambda**: Calcula estado de stock dinámicamente
        - **color_discrete_map**: Asigna colores específicos por categoría
        - **update_traces**: Personaliza la visualización de datos en el gráfico
        """)
    
    with st.expander("🚨 Código de Sistema de Alertas", expanded=False):
        st.code("""
# Sistema de alertas automáticas
st.markdown("---")
st.markdown("### 🚨 Alertas del Sistema")

alertas = []

# Productos sin stock
if productos_sin_stock > 0:
    productos_sin_stock_lista = df_inventario[df_inventario['Stock Actual'] == 0]['Nombre'].tolist()
    alertas.append({
        'tipo': 'error',
        'mensaje': f"❌ {productos_sin_stock} productos SIN STOCK",
        'detalles': f"Productos: {', '.join(productos_sin_stock_lista[:3])}{'...' if len(productos_sin_stock_lista) > 3 else ''}"
    })

# Productos con bajo stock
if productos_bajo_stock > productos_sin_stock:
    productos_bajo_stock_lista = df_inventario[
        (df_inventario['Stock Actual'] <= df_inventario['Stock Mínimo']) & 
        (df_inventario['Stock Actual'] > 0)
    ]['Nombre'].tolist()
    
    alertas.append({
        'tipo': 'warning',
        'mensaje': f"⚠️ {len(productos_bajo_stock_lista)} productos con BAJO STOCK",
        'detalles': f"Productos: {', '.join(productos_bajo_stock_lista[:3])}{'...' if len(productos_bajo_stock_lista) > 3 else ''}"
    })

# Mostrar alertas
if alertas:
    for alerta in alertas:
        if alerta['tipo'] == 'error':
            st.error(f"{alerta['mensaje']}\\n{alerta['detalles']}")
        elif alerta['tipo'] == 'warning':
            st.warning(f"{alerta['mensaje']}\\n{alerta['detalles']}")
else:
    st.success("✅ Todos los productos tienen stock adecuado")
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **Sistema de alertas dinámico**: Evalúa condiciones y genera alertas
        - **Múltiples niveles**: Error, warning, success según la situación
        - **Listas comprensivas**: Filtra productos según condiciones específicas
        - **Truncado de texto**: Muestra solo primeros elementos para legibilidad
        """)

def mostrar_codigo_productos():
    """Muestra el código de gestión de productos."""
    
    st.markdown("### 📦 Sistema de Gestión de Productos")
    st.markdown("""
    Este módulo permite el CRUD completo de productos: crear, leer, actualizar y eliminar
    productos del inventario con validaciones y persistencia de datos.
    """)
    
    with st.expander("📋 Explicación del Sistema CRUD", expanded=True):
        st.markdown("""
        **Operaciones CRUD:**
        1. **Create**: Agregar nuevos productos con validaciones
        2. **Read**: Visualizar y filtrar productos existentes
        3. **Update**: Modificar información de productos
        4. **Delete**: Eliminar productos del sistema
        
        **Validaciones Implementadas:**
        - Nombres únicos de productos
        - Valores numéricos positivos
        - Categorías predefinidas
        - Stock mínimo lógico
        """)
    
    with st.expander("💻 Código de Agregar Producto", expanded=False):
        st.code("""
def render_gestion_productos():
    st.markdown("## 📦 Gestión de Productos")
    
    # Pestañas para diferentes operaciones
    tab_agregar, tab_editar, tab_lista = st.tabs(["➕ Agregar", "✏️ Editar", "📋 Lista"])
    
    with tab_agregar:
        st.markdown("### ➕ Agregar Nuevo Producto")
        
        with st.form("form_nuevo_producto"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre del Producto*", key="nuevo_nombre")
                categoria = st.selectbox(
                    "Categoría*", 
                    ["Electrónicos", "Ropa", "Hogar", "Deportes", "Libros"],
                    key="nueva_categoria"
                )
                precio = st.number_input(
                    "Precio Unitario ($)*", 
                    min_value=0.01, 
                    value=10.0, 
                    step=0.01,
                    key="nuevo_precio"
                )
            
            with col2:
                stock_actual = st.number_input(
                    "Stock Inicial*", 
                    min_value=0, 
                    value=100, 
                    step=1,
                    key="nuevo_stock"
                )
                stock_minimo = st.number_input(
                    "Stock Mínimo*", 
                    min_value=0, 
                    value=10, 
                    step=1,
                    key="nuevo_stock_min"
                )
                descripcion = st.text_area(
                    "Descripción", 
                    placeholder="Descripción opcional del producto...",
                    key="nueva_descripcion"
                )
            
            # Botón de envío
            submitted = st.form_submit_button("🔄 Agregar Producto", type="primary")
            
            if submitted:
                # Validaciones
                if not nombre.strip():
                    st.error("❌ El nombre del producto es obligatorio")
                elif any(p['Nombre'].lower() == nombre.lower() for p in st.session_state.inventario_data):
                    st.error("❌ Ya existe un producto con ese nombre")
                elif stock_minimo > stock_actual:
                    st.warning("⚠️ El stock mínimo no puede ser mayor al stock actual")
                else:
                    # Agregar producto
                    nuevo_id = max([p['ID'] for p in st.session_state.inventario_data]) + 1
                    
                    nuevo_producto = {
                        'ID': nuevo_id,
                        'Nombre': nombre.strip(),
                        'Categoría': categoria,
                        'Stock Actual': stock_actual,
                        'Stock Mínimo': stock_minimo,
                        'Precio Unitario': precio,
                        'Descripción': descripcion.strip() if descripcion else "Sin descripción"
                    }
                    
                    st.session_state.inventario_data.append(nuevo_producto)
                    st.success(f"✅ Producto '{nombre}' agregado exitosamente!")
                    st.rerun()
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **st.form**: Agrupa widgets para envío conjunto
        - **Validaciones múltiples**: Nombre único, valores lógicos
        - **session_state**: Persiste datos entre reruns
        - **st.rerun()**: Actualiza la interfaz después de cambios
        """)
    
    with st.expander("✏️ Código de Editar Producto", expanded=False):
        st.code("""
with tab_editar:
    st.markdown("### ✏️ Editar Producto Existente")
    
    if st.session_state.inventario_data:
        # Selector de producto a editar
        productos_nombres = [f"{p['Nombre']} (ID: {p['ID']})" for p in st.session_state.inventario_data]
        producto_seleccionado = st.selectbox(
            "Selecciona producto a editar:",
            productos_nombres,
            key="editar_selector"
        )
        
        if producto_seleccionado:
            # Encontrar producto seleccionado
            producto_id = int(producto_seleccionado.split("ID: ")[1].split(")")[0])
            producto = next(p for p in st.session_state.inventario_data if p['ID'] == producto_id)
            
            with st.form("form_editar_producto"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nombre_edit = st.text_input("Nombre del Producto", value=producto['Nombre'])
                    categoria_edit = st.selectbox(
                        "Categoría", 
                        ["Electrónicos", "Ropa", "Hogar", "Deportes", "Libros"],
                        index=["Electrónicos", "Ropa", "Hogar", "Deportes", "Libros"].index(producto['Categoría'])
                    )
                    precio_edit = st.number_input(
                        "Precio Unitario ($)", 
                        min_value=0.01, 
                        value=float(producto['Precio Unitario']), 
                        step=0.01
                    )
                
                with col2:
                    stock_actual_edit = st.number_input(
                        "Stock Actual", 
                        min_value=0, 
                        value=int(producto['Stock Actual']), 
                        step=1
                    )
                    stock_minimo_edit = st.number_input(
                        "Stock Mínimo", 
                        min_value=0, 
                        value=int(producto['Stock Mínimo']), 
                        step=1
                    )
                    descripcion_edit = st.text_area(
                        "Descripción", 
                        value=producto.get('Descripción', '')
                    )
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    submitted_edit = st.form_submit_button("💾 Guardar Cambios", type="primary")
                with col_btn2:
                    submitted_delete = st.form_submit_button("🗑️ Eliminar Producto", type="secondary")
                
                if submitted_edit:
                    # Actualizar producto
                    for i, p in enumerate(st.session_state.inventario_data):
                        if p['ID'] == producto_id:
                            st.session_state.inventario_data[i].update({
                                'Nombre': nombre_edit.strip(),
                                'Categoría': categoria_edit,
                                'Stock Actual': stock_actual_edit,
                                'Stock Mínimo': stock_minimo_edit,
                                'Precio Unitario': precio_edit,
                                'Descripción': descripcion_edit.strip()
                            })
                            break
                    
                    st.success(f"✅ Producto '{nombre_edit}' actualizado!")
                    st.rerun()
                
                if submitted_delete:
                    # Confirmar eliminación
                    st.session_state.inventario_data = [p for p in st.session_state.inventario_data if p['ID'] != producto_id]
                    st.success(f"🗑️ Producto eliminado!")
                    st.rerun()
    else:
        st.info("📝 No hay productos para editar. Agrega algunos primero.")
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **Selector dinámico**: Lista productos con ID para identificación única
        - **Pre-llenado de campos**: Carga valores actuales para edición
        - **Doble botón**: Permite guardar o eliminar en el mismo formulario
        - **Búsqueda por ID**: Encuentra producto específico en la lista
        """)

def mostrar_codigo_movimientos():
    """Muestra el código de movimientos de stock."""
    
    st.markdown("### 📈 Sistema de Movimientos de Stock")
    st.markdown("""
    Registra y visualiza todos los movimientos de entrada y salida de productos
    con trazabilidad completa y reportes históricos.
    """)
    
    with st.expander("📋 Explicación del Sistema", expanded=True):
        st.markdown("""
        **Tipos de Movimientos:**
        1. **Entrada**: Compras, devoluciones, ajustes positivos
        2. **Salida**: Ventas, devoluciones, ajustes negativos
        
        **Funcionalidades:**
        - Registro de movimientos con fecha y motivo
        - Actualización automática de stock
        - Historial completo de transacciones
        - Filtros por fecha, producto y tipo
        """)
    
    with st.expander("💻 Código de Registro de Movimientos", expanded=False):
        st.code("""
def render_movimientos_stock():
    st.markdown("## 📈 Movimientos de Stock")
    
    tab_nuevo, tab_historial = st.tabs(["➕ Nuevo Movimiento", "📋 Historial"])
    
    with tab_nuevo:
        st.markdown("### ➕ Registrar Nuevo Movimiento")
        
        if st.session_state.inventario_data:
            with st.form("form_movimiento"):
                col1, col2 = st.columns(2)
                
                with col1:
                    # Selector de producto
                    productos_opciones = [f"{p['Nombre']} (Stock: {p['Stock Actual']})" 
                                        for p in st.session_state.inventario_data]
                    producto_seleccionado = st.selectbox(
                        "Producto*",
                        productos_opciones,
                        key="mov_producto"
                    )
                    
                    tipo_movimiento = st.selectbox(
                        "Tipo de Movimiento*",
                        ["Entrada", "Salida"],
                        key="mov_tipo"
                    )
                    
                    cantidad = st.number_input(
                        "Cantidad*",
                        min_value=1,
                        value=1,
                        step=1,
                        key="mov_cantidad"
                    )
                
                with col2:
                    motivo = st.selectbox(
                        "Motivo*",
                        ["Compra", "Venta", "Devolución", "Ajuste de Inventario", "Producto Dañado", "Otro"],
                        key="mov_motivo"
                    )
                    
                    fecha_movimiento = st.date_input(
                        "Fecha",
                        value=datetime.now().date(),
                        key="mov_fecha"
                    )
                    
                    observaciones = st.text_area(
                        "Observaciones",
                        placeholder="Observaciones adicionales (opcional)...",
                        key="mov_observaciones"
                    )
                
                submitted = st.form_submit_button("📝 Registrar Movimiento", type="primary")
                
                if submitted:
                    # Obtener producto seleccionado
                    nombre_producto = producto_seleccionado.split(" (Stock:")[0]
                    producto = next(p for p in st.session_state.inventario_data if p['Nombre'] == nombre_producto)
                    
                    # Validar stock suficiente para salidas
                    if tipo_movimiento == "Salida" and cantidad > producto['Stock Actual']:
                        st.error(f"❌ Stock insuficiente. Stock actual: {producto['Stock Actual']}")
                    else:
                        # Crear movimiento
                        nuevo_movimiento = {
                            'ID': len(st.session_state.movimientos_data) + 1,
                            'Fecha': fecha_movimiento,
                            'Producto ID': producto['ID'],
                            'Producto': producto['Nombre'],
                            'Tipo': tipo_movimiento,
                            'Cantidad': cantidad,
                            'Motivo': motivo,
                            'Stock Anterior': producto['Stock Actual'],
                            'Stock Nuevo': producto['Stock Actual'] + (cantidad if tipo_movimiento == "Entrada" else -cantidad),
                            'Observaciones': observaciones.strip() if observaciones else "Sin observaciones"
                        }
                        
                        # Actualizar stock del producto
                        for i, p in enumerate(st.session_state.inventario_data):
                            if p['ID'] == producto['ID']:
                                if tipo_movimiento == "Entrada":
                                    st.session_state.inventario_data[i]['Stock Actual'] += cantidad
                                else:
                                    st.session_state.inventario_data[i]['Stock Actual'] -= cantidad
                                break
                        
                        # Agregar movimiento al historial
                        st.session_state.movimientos_data.append(nuevo_movimiento)
                        
                        st.success(f"✅ Movimiento registrado: {tipo_movimiento} de {cantidad} unidades de {producto['Nombre']}")
                        st.rerun()
        else:
            st.info("📝 No hay productos disponibles. Agrega productos primero.")
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **Validación de stock**: Previene salidas mayores al stock disponible
        - **Actualización atómica**: Modifica stock y registra movimiento juntos
        - **Cálculo automático**: Stock nuevo = anterior +/- cantidad según tipo
        - **Trazabilidad completa**: Registra estado anterior y nuevo
        """)
    
    with st.expander("📊 Código de Visualización de Historial", expanded=False):
        st.code("""
with tab_historial:
    st.markdown("### 📋 Historial de Movimientos")
    
    if st.session_state.movimientos_data:
        df_movimientos = pd.DataFrame(st.session_state.movimientos_data)
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtro_tipo = st.selectbox(
                "Filtrar por tipo:",
                ["Todos", "Entrada", "Salida"],
                key="filtro_tipo_mov"
            )
        
        with col2:
            productos_unicos = df_movimientos['Producto'].unique()
            filtro_producto = st.selectbox(
                "Filtrar por producto:",
                ["Todos"] + list(productos_unicos),
                key="filtro_producto_mov"
            )
        
        with col3:
            dias_filtro = st.selectbox(
                "Filtrar por período:",
                ["Todos", "Últimos 7 días", "Últimos 30 días", "Últimos 90 días"],
                key="filtro_dias_mov"
            )
        
        # Aplicar filtros
        df_filtrado = df_movimientos.copy()
        
        if filtro_tipo != "Todos":
            df_filtrado = df_filtrado[df_filtrado['Tipo'] == filtro_tipo]
        
        if filtro_producto != "Todos":
            df_filtrado = df_filtrado[df_filtrado['Producto'] == filtro_producto]
        
        if dias_filtro != "Todos":
            dias_map = {"Últimos 7 días": 7, "Últimos 30 días": 30, "Últimos 90 días": 90}
            dias = dias_map[dias_filtro]
            fecha_limite = datetime.now().date() - timedelta(days=dias)
            df_filtrado = df_filtrado[pd.to_datetime(df_filtrado['Fecha']).dt.date >= fecha_limite]
        
        # Mostrar tabla
        if not df_filtrado.empty:
            # Ordenar por fecha descendente
            df_filtrado = df_filtrado.sort_values('Fecha', ascending=False)
            
            st.dataframe(
                df_filtrado[['Fecha', 'Producto', 'Tipo', 'Cantidad', 'Motivo', 'Stock Anterior', 'Stock Nuevo']],
                use_container_width=True
            )
            
            # Resumen de movimientos
            st.markdown("#### 📊 Resumen de Movimientos")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_movimientos = len(df_filtrado)
                st.metric("Total Movimientos", total_movimientos)
            
            with col2:
                entradas = df_filtrado[df_filtrado['Tipo'] == 'Entrada']['Cantidad'].sum()
                st.metric("Total Entradas", int(entradas) if not pd.isna(entradas) else 0)
            
            with col3:
                salidas = df_filtrado[df_filtrado['Tipo'] == 'Salida']['Cantidad'].sum()
                st.metric("Total Salidas", int(salidas) if not pd.isna(salidas) else 0)
            
            with col4:
                saldo_neto = entradas - salidas if not pd.isna(entradas) and not pd.isna(salidas) else 0
                st.metric("Saldo Neto", int(saldo_neto), delta="Positivo" if saldo_neto > 0 else "Negativo")
        
        else:
            st.info("📊 No hay movimientos que coincidan con los filtros seleccionados")
    
    else:
        st.info("📊 No hay movimientos registrados aún")
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **Filtros múltiples**: Por tipo, producto y período de tiempo
        - **Filtrado de DataFrames**: Usa condiciones booleanas para filtrar
        - **Resumen automático**: Calcula métricas agregadas
        - **Ordenamiento**: Por fecha descendente para ver lo más reciente
        """)

def mostrar_codigo_alertas():
    """Muestra el código del sistema de alertas."""
    
    st.markdown("### ⚠️ Sistema de Alertas y Reportes")
    st.markdown("""
    Sistema automatizado de alertas que monitorea el inventario y genera
    reportes de estado, productos críticos y recomendaciones de restock.
    """)
    
    with st.expander("📋 Explicación del Sistema de Alertas", expanded=True):
        st.markdown("""
        **Tipos de Alertas:**
        1. **Críticas**: Productos sin stock (requieren acción inmediata)
        2. **Advertencia**: Productos con bajo stock (requieren atención)
        3. **Informativas**: Estado general del inventario
        
        **Reportes Generados:**
        - Lista de productos críticos
        - Recomendaciones de compra
        - Análisis de rotación de productos
        - Valor del inventario en riesgo
        """)
    
    with st.expander("💻 Código de Generación de Alertas", expanded=False):
        st.code("""
def render_alertas_reportes():
    st.markdown("## ⚠️ Alertas y Reportes del Sistema")
    
    df_inventario = pd.DataFrame(st.session_state.inventario_data)
    df_movimientos = pd.DataFrame(st.session_state.movimientos_data)
    
    # Análisis de productos críticos
    productos_sin_stock = df_inventario[df_inventario['Stock Actual'] == 0]
    productos_bajo_stock = df_inventario[
        (df_inventario['Stock Actual'] <= df_inventario['Stock Mínimo']) & 
        (df_inventario['Stock Actual'] > 0)
    ]
    
    # Panel de alertas críticas
    st.markdown("### 🚨 Alertas Críticas")
    
    if len(productos_sin_stock) > 0:
        st.error(f"❌ {len(productos_sin_stock)} productos SIN STOCK - Acción inmediata requerida")
        
        # Mostrar productos sin stock
        with st.expander("Ver productos sin stock", expanded=True):
            productos_criticos = productos_sin_stock[['Nombre', 'Categoría', 'Stock Mínimo', 'Precio Unitario']]
            productos_criticos['Valor en Riesgo'] = productos_criticos['Stock Mínimo'] * productos_criticos['Precio Unitario']
            
            st.dataframe(
                productos_criticos.style.format({
                    'Precio Unitario': '${:,.2f}',
                    'Valor en Riesgo': '${:,.2f}'
                }),
                use_container_width=True
            )
            
            valor_total_riesgo = productos_criticos['Valor en Riesgo'].sum()
            st.metric("💰 Valor Total en Riesgo", f"${valor_total_riesgo:,.2f}")
    
    if len(productos_bajo_stock) > 0:
        st.warning(f"⚠️ {len(productos_bajo_stock)} productos con BAJO STOCK - Revisar pronto")
        
        with st.expander("Ver productos con bajo stock", expanded=False):
            productos_atencion = productos_bajo_stock[['Nombre', 'Categoría', 'Stock Actual', 'Stock Mínimo']].copy()
            productos_atencion['Diferencia'] = productos_atencion['Stock Mínimo'] - productos_atencion['Stock Actual']
            productos_atencion['% del Mínimo'] = (productos_atencion['Stock Actual'] / productos_atencion['Stock Mínimo'] * 100).round(1)
            
            st.dataframe(
                productos_atencion.style.format({'% del Mínimo': '{:.1f}%'}),
                use_container_width=True
            )
    
    if len(productos_sin_stock) == 0 and len(productos_bajo_stock) == 0:
        st.success("✅ Todos los productos tienen stock adecuado")
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **Análisis automático**: Evalúa estado de cada producto
        - **Clasificación por severidad**: Crítico, advertencia, normal
        - **Cálculos de riesgo**: Valor monetario en riesgo por falta de stock
        - **Formateo condicional**: Estilos diferentes según el tipo de alerta
        """)
    
    with st.expander("📊 Código de Reportes de Restock", expanded=False):
        st.code("""
# Recomendaciones de restock
st.markdown("---")
st.markdown("### 📋 Recomendaciones de Restock")

productos_restock = pd.concat([productos_sin_stock, productos_bajo_stock])

if len(productos_restock) > 0:
    # Calcular recomendaciones de compra
    recomendaciones = []
    
    for _, producto in productos_restock.iterrows():
        # Calcular ventas promedio si hay datos
        ventas_producto = df_movimientos[
            (df_movimientos['Producto ID'] == producto['ID']) & 
            (df_movimientos['Tipo'] == 'Salida')
        ]
        
        if len(ventas_producto) > 0:
            # Calcular promedio de ventas de los últimos 30 días
            fecha_limite = datetime.now() - timedelta(days=30)
            ventas_recientes = ventas_producto[
                pd.to_datetime(ventas_producto['Fecha']) >= fecha_limite
            ]
            
            if len(ventas_recientes) > 0:
                venta_promedio_diaria = ventas_recientes['Cantidad'].sum() / 30
                stock_recomendado = max(
                    producto['Stock Mínimo'] * 2,  # Mínimo 2x el stock mínimo
                    int(venta_promedio_diaria * 45)  # O 45 días de venta
                )
            else:
                stock_recomendado = producto['Stock Mínimo'] * 2
        else:
            stock_recomendado = producto['Stock Mínimo'] * 2
        
        cantidad_comprar = stock_recomendado - producto['Stock Actual']
        costo_estimado = cantidad_comprar * producto['Precio Unitario']
        
        recomendaciones.append({
            'Producto': producto['Nombre'],
            'Categoría': producto['Categoría'],
            'Stock Actual': producto['Stock Actual'],
            'Stock Recomendado': stock_recomendado,
            'Cantidad a Comprar': cantidad_comprar,
            'Costo Estimado': costo_estimado,
            'Prioridad': 'Alta' if producto['Stock Actual'] == 0 else 'Media'
        })
    
    df_recomendaciones = pd.DataFrame(recomendaciones)
    df_recomendaciones = df_recomendaciones.sort_values(['Prioridad', 'Costo Estimado'], ascending=[True, False])
    
    st.dataframe(
        df_recomendaciones.style.format({
            'Costo Estimado': '${:,.2f}'
        }).apply(lambda x: ['background-color: #ffebee' if x['Prioridad'] == 'Alta' 
                          else 'background-color: #fff3e0' for _ in x], axis=1),
        use_container_width=True
    )
    
    # Resumen de costos
    costo_total_alta = df_recomendaciones[df_recomendaciones['Prioridad'] == 'Alta']['Costo Estimado'].sum()
    costo_total_media = df_recomendaciones[df_recomendaciones['Prioridad'] == 'Media']['Costo Estimado'].sum()
    costo_total = costo_total_alta + costo_total_media
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Costo Prioridad Alta", f"${costo_total_alta:,.2f}")
    with col2:
        st.metric("💰 Costo Prioridad Media", f"${costo_total_media:,.2f}")
    with col3:
        st.metric("💰 Costo Total Restock", f"${costo_total:,.2f}")

else:
    st.info("✅ No se requieren compras en este momento")
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **Análisis de demanda**: Calcula ventas promedio para recomendaciones
        - **Algoritmo de restock**: Considera stock mínimo y patrones de venta
        - **Priorización**: Alta para sin stock, media para bajo stock
        - **Cálculo de costos**: Estima inversión necesaria para restock
        """)

def mostrar_codigo_prediccion():
    """Muestra el código de predicción de demanda."""
    
    st.markdown("### 🔮 Sistema de Predicción de Demanda")
    st.markdown("""
    Utiliza análisis estadístico de datos históricos para predecir la demanda futura
    y optimizar los niveles de stock de cada producto.
    """)
    
    with st.expander("📋 Explicación del Algoritmo", expanded=True):
        st.markdown("""
        **Metodología de Predicción:**
        1. **Análisis de Tendencias**: Evalúa patrones de venta históricos
        2. **Promedio Móvil**: Calcula demanda promedio por período
        3. **Análisis de Estacionalidad**: Detecta patrones cíclicos
        4. **Proyección Futura**: Estima demanda para próximos períodos
        
        **Factores Considerados:**
        - Ventas de los últimos 30, 60 y 90 días
        - Tendencia de crecimiento/decrecimiento
        - Variabilidad de la demanda
        - Días de stock disponible
        """)
    
    with st.expander("💻 Código de Análisis de Demanda", expanded=False):
        st.code("""
def render_prediccion_demanda():
    st.markdown("## 🔮 Predicción de Demanda")
    
    df_inventario = pd.DataFrame(st.session_state.inventario_data)
    df_movimientos = pd.DataFrame(st.session_state.movimientos_data)
    
    if len(df_movimientos) > 0:
        # Análisis por producto
        productos_analisis = []
        
        for _, producto in df_inventario.iterrows():
            # Obtener movimientos de salida del producto
            movimientos_producto = df_movimientos[
                (df_movimientos['Producto ID'] == producto['ID']) & 
                (df_movimientos['Tipo'] == 'Salida')
            ].copy()
            
            if len(movimientos_producto) > 0:
                # Convertir fechas
                movimientos_producto['Fecha'] = pd.to_datetime(movimientos_producto['Fecha'])
                movimientos_producto = movimientos_producto.sort_values('Fecha')
                
                # Calcular métricas de demanda
                fecha_actual = datetime.now()
                
                # Ventas últimos 30 días
                fecha_30d = fecha_actual - timedelta(days=30)
                ventas_30d = movimientos_producto[
                    movimientos_producto['Fecha'] >= fecha_30d
                ]['Cantidad'].sum()
                
                # Ventas últimos 60 días
                fecha_60d = fecha_actual - timedelta(days=60)
                ventas_60d = movimientos_producto[
                    movimientos_producto['Fecha'] >= fecha_60d
                ]['Cantidad'].sum()
                
                # Calcular promedios
                if ventas_30d > 0:
                    demanda_diaria_30d = ventas_30d / 30
                    dias_stock_actual = producto['Stock Actual'] / demanda_diaria_30d if demanda_diaria_30d > 0 else 999
                else:
                    demanda_diaria_30d = 0
                    dias_stock_actual = 999
                
                # Tendencia (comparar 30d vs 60d)
                ventas_30d_anterior = ventas_60d - ventas_30d
                if ventas_30d_anterior > 0:
                    tendencia = (ventas_30d - ventas_30d_anterior) / ventas_30d_anterior * 100
                else:
                    tendencia = 0
                
                # Predicción próximos 30 días
                factor_tendencia = 1 + (tendencia / 100 * 0.5)  # Suavizar tendencia
                prediccion_30d = ventas_30d * factor_tendencia
                
                productos_analisis.append({
                    'Producto': producto['Nombre'],
                    'Categoría': producto['Categoría'],
                    'Stock Actual': producto['Stock Actual'],
                    'Ventas 30d': ventas_30d,
                    'Demanda Diaria': round(demanda_diaria_30d, 2),
                    'Días de Stock': round(dias_stock_actual, 1),
                    'Tendencia (%)': round(tendencia, 1),
                    'Predicción 30d': round(prediccion_30d, 1),
                    'Estado': 'Crítico' if dias_stock_actual < 7 
                             else 'Atención' if dias_stock_actual < 15 
                             else 'Normal'
                })
            
            else:
                # Producto sin movimientos
                productos_analisis.append({
                    'Producto': producto['Nombre'],
                    'Categoría': producto['Categoría'],
                    'Stock Actual': producto['Stock Actual'],
                    'Ventas 30d': 0,
                    'Demanda Diaria': 0,
                    'Días de Stock': 999,
                    'Tendencia (%)': 0,
                    'Predicción 30d': 0,
                    'Estado': 'Sin Datos'
                })
        
        df_analisis = pd.DataFrame(productos_analisis)
        
        # Mostrar análisis
        st.markdown("### 📊 Análisis de Demanda por Producto")
        
        # Filtro por estado
        estados_filtro = st.multiselect(
            "Filtrar por estado:",
            ["Crítico", "Atención", "Normal", "Sin Datos"],
            default=["Crítico", "Atención"],
            key="filtro_estados_pred"
        )
        
        df_filtrado = df_analisis[df_analisis['Estado'].isin(estados_filtro)] if estados_filtro else df_analisis
        
        # Mostrar tabla con formato condicional
        if not df_filtrado.empty:
            def aplicar_colores(row):
                if row['Estado'] == 'Crítico':
                    return ['background-color: #ffebee'] * len(row)
                elif row['Estado'] == 'Atención':
                    return ['background-color: #fff3e0'] * len(row)
                elif row['Estado'] == 'Normal':
                    return ['background-color: #e8f5e8'] * len(row)
                else:
                    return ['background-color: #f5f5f5'] * len(row)
            
            st.dataframe(
                df_filtrado.style.apply(aplicar_colores, axis=1).format({
                    'Demanda Diaria': '{:.2f}',
                    'Días de Stock': '{:.1f}',
                    'Tendencia (%)': '{:.1f}',
                    'Predicción 30d': '{:.1f}'
                }),
                use_container_width=True
            )
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **Análisis temporal**: Compara períodos para detectar tendencias
        - **Cálculo de días de stock**: Stock actual / demanda diaria
        - **Factor de tendencia**: Ajusta predicción según crecimiento/decrecimiento
        - **Clasificación automática**: Crítico, atención, normal según días de stock
        """)
    
    with st.expander("📈 Código de Visualización de Predicciones", expanded=False):
        st.code("""
        # Gráfico de análisis de demanda
        productos_con_demanda = df_analisis[df_analisis['Demanda Diaria'] > 0]
        
        if not productos_con_demanda.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de días de stock
                fig_stock = px.bar(
                    productos_con_demanda.sort_values('Días de Stock'),
                    x='Producto',
                    y='Días de Stock',
                    color='Estado',
                    title="Días de Stock Disponible por Producto",
                    color_discrete_map={
                        'Crítico': '#f44336',
                        'Atención': '#ff9800', 
                        'Normal': '#4caf50',
                        'Sin Datos': '#9e9e9e'
                    }
                )
                fig_stock.update_xaxes(tickangle=45)
                fig_stock.add_hline(y=15, line_dash="dash", line_color="orange", 
                                   annotation_text="Límite Atención")
                fig_stock.add_hline(y=7, line_dash="dash", line_color="red", 
                                   annotation_text="Límite Crítico")
                st.plotly_chart(fig_stock, use_container_width=True)
            
            with col2:
                # Gráfico de tendencias
                fig_tendencia = px.scatter(
                    productos_con_demanda,
                    x='Ventas 30d',
                    y='Predicción 30d',
                    size='Demanda Diaria',
                    color='Estado',
                    hover_data=['Producto'],
                    title="Ventas Actuales vs Predicción",
                    color_discrete_map={
                        'Crítico': '#f44336',
                        'Atención': '#ff9800', 
                        'Normal': '#4caf50',
                        'Sin Datos': '#9e9e9e'
                    }
                )
                # Línea de referencia y=x (sin cambio)
                max_val = max(productos_con_demanda['Ventas 30d'].max(), 
                             productos_con_demanda['Predicción 30d'].max())
                fig_tendencia.add_shape(
                    type="line", x0=0, y0=0, x1=max_val, y1=max_val,
                    line=dict(dash="dash", color="gray"),
                )
                st.plotly_chart(fig_tendencia, use_container_width=True)
            
            # Resumen de predicciones
            st.markdown("### 📈 Resumen de Predicciones")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                productos_criticos = len(df_analisis[df_analisis['Estado'] == 'Crítico'])
                st.metric("Productos Críticos", productos_criticos)
            
            with col2:
                productos_atencion = len(df_analisis[df_analisis['Estado'] == 'Atención'])
                st.metric("Requieren Atención", productos_atencion)
            
            with col3:
                demanda_total = df_analisis['Predicción 30d'].sum()
                st.metric("Demanda Predicha 30d", f"{demanda_total:.0f} unidades")
            
            with col4:
                productos_sin_movimiento = len(df_analisis[df_analisis['Estado'] == 'Sin Datos'])
                st.metric("Sin Movimientos", productos_sin_movimiento)
        
        else:
            st.info("📊 No hay datos suficientes para generar predicciones")
    
    else:
        st.info("📊 No hay movimientos registrados para análisis de demanda")
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **Visualización dual**: Días de stock + scatter plot de tendencias
        - **Líneas de referencia**: Límites críticos y de atención
        - **Scatter plot**: Muestra relación entre ventas actuales y predichas
        - **Métricas de resumen**: Vista general del estado del sistema
        """)

def mostrar_codigo_estructura():
    """Muestra el código de estructura de datos."""
    
    st.markdown("### 🗂️ Estructura de Datos del Sistema")
    st.markdown("""
    Explicación detallada de cómo se organizan y gestionan los datos
    en el sistema de inventario usando session_state de Streamlit.
    """)
    
    with st.expander("📋 Arquitectura de Datos", expanded=True):
        st.markdown("""
        **Entidades Principales:**
        1. **Inventario**: Productos con stock y características
        2. **Movimientos**: Transacciones de entrada y salida
        3. **Sesión**: Estado persistente durante la ejecución
        
        **Relaciones:**
        - Inventario 1:N Movimientos (un producto tiene muchos movimientos)
        - Cada movimiento referencia un producto por ID
        """)
    
    with st.expander("💻 Código de Inicialización de Datos", expanded=False):
        st.code("""
def generar_datos_inventario():
    \"\"\"Genera datos de ejemplo para el inventario.\"\"\"
    return [
        {
            'ID': 1,
            'Nombre': 'Laptop Dell XPS 13',
            'Categoría': 'Electrónicos',
            'Stock Actual': 25,
            'Stock Mínimo': 5,
            'Precio Unitario': 1299.99,
            'Descripción': 'Laptop ultrabook con procesador Intel i7'
        },
        {
            'ID': 2,
            'Nombre': 'Camiseta Nike Dri-FIT',
            'Categoría': 'Ropa',
            'Stock Actual': 150,
            'Stock Mínimo': 20,
            'Precio Unitario': 29.99,
            'Descripción': 'Camiseta deportiva de secado rápido'
        },
        {
            'ID': 3,
            'Nombre': 'Cafetera Nespresso',
            'Categoría': 'Hogar',
            'Stock Actual': 3,  # Bajo stock
            'Stock Mínimo': 10,
            'Precio Unitario': 199.99,
            'Descripción': 'Cafetera automática con cápsulas'
        },
        {
            'ID': 4,
            'Nombre': 'Pelota de Fútbol',
            'Categoría': 'Deportes',
            'Stock Actual': 0,  # Sin stock
            'Stock Mínimo': 15,
            'Precio Unitario': 39.99,
            'Descripción': 'Pelota oficial FIFA size 5'
        },
        {
            'ID': 5,
            'Nombre': 'El Quijote',
            'Categoría': 'Libros',
            'Stock Actual': 45,
            'Stock Mínimo': 8,
            'Precio Unitario': 15.99,
            'Descripción': 'Edición clásica de la obra maestra'
        }
    ]

def generar_movimientos():
    \"\"\"Genera movimientos de ejemplo para demostrar el sistema.\"\""
    movimientos = []
    base_date = datetime.now() - timedelta(days=60)
    
    # Generar movimientos aleatorios para cada producto
    productos_ids = [1, 2, 3, 4, 5]
    tipos = ['Entrada', 'Salida']
    motivos = ['Compra', 'Venta', 'Devolución', 'Ajuste de Inventario']
    
    for i in range(50):  # 50 movimientos de ejemplo
        fecha = base_date + timedelta(days=random.randint(0, 60))
        producto_id = random.choice(productos_ids)
        tipo = random.choice(tipos)
        cantidad = random.randint(1, 10)
        motivo = random.choice(motivos)
        
        movimientos.append({
            'ID': i + 1,
            'Fecha': fecha.date(),
            'Producto ID': producto_id,
            'Producto': f'Producto {producto_id}',  # Se actualizará con nombre real
            'Tipo': tipo,
            'Cantidad': cantidad,
            'Motivo': motivo,
            'Stock Anterior': random.randint(10, 100),
            'Stock Nuevo': random.randint(5, 95),
            'Observaciones': f'Movimiento automático {i+1}'
        })
    
    return movimientos
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **Datos de ejemplo**: Incluye productos en diferentes estados (normal, bajo stock, sin stock)
        - **Relaciones por ID**: Los movimientos referencian productos por ID
        - **Datos realistas**: Precios, categorías y cantidades representativas
        - **Historial simulado**: Movimientos distribuidos en los últimos 60 días
        """)
    
    with st.expander("🔄 Código de Gestión de Session State", expanded=False):
        st.code("""
# Inicialización del estado de la sesión
if 'inventario_data' not in st.session_state:
    st.session_state.inventario_data = generar_datos_inventario()

if 'movimientos_data' not in st.session_state:
    st.session_state.movimientos_data = generar_movimientos()

# Función para actualizar productos después de movimientos
def actualizar_nombres_productos():
    \"\"\"Actualiza los nombres de productos en movimientos basándose en el inventario actual.\"\""
    inventario_dict = {p['ID']: p['Nombre'] for p in st.session_state.inventario_data}
    
    for movimiento in st.session_state.movimientos_data:
        producto_id = movimiento['Producto ID']
        if producto_id in inventario_dict:
            movimiento['Producto'] = inventario_dict[producto_id]

# Función para limpiar datos inconsistentes
def validar_consistencia_datos():
    \"\"\"Valida y corrige inconsistencias en los datos del sistema.\"\""
    problemas = []
    
    # Verificar IDs únicos en inventario
    ids_inventario = [p['ID'] for p in st.session_state.inventario_data]
    if len(ids_inventario) != len(set(ids_inventario)):
        problemas.append("IDs duplicados en inventario")
    
    # Verificar referencias en movimientos
    ids_validos = set(ids_inventario)
    for mov in st.session_state.movimientos_data:
        if mov['Producto ID'] not in ids_validos:
            problemas.append(f"Movimiento {mov['ID']} referencia producto inexistente")
    
    # Verificar stocks negativos
    for producto in st.session_state.inventario_data:
        if producto['Stock Actual'] < 0:
            problemas.append(f"Stock negativo en {producto['Nombre']}")
    
    return problemas

# Función para exportar datos
def exportar_datos_sistema():
    \"\"\"Prepara los datos del sistema para exportación.\"\""
    datos_export = {
        'inventario': st.session_state.inventario_data,
        'movimientos': st.session_state.movimientos_data,
        'timestamp': datetime.now().isoformat(),
        'version': '1.0'
    }
    return json.dumps(datos_export, indent=2, default=str)

# Función para importar datos
def importar_datos_sistema(datos_json):
    \"\"\"Importa datos desde JSON y actualiza el session_state.\"\""
    try:
        datos = json.loads(datos_json)
        
        if 'inventario' in datos and 'movimientos' in datos:
            st.session_state.inventario_data = datos['inventario']
            st.session_state.movimientos_data = datos['movimientos']
            return True, "Datos importados exitosamente"
        else:
            return False, "Formato de datos inválido"
    
    except json.JSONDecodeError:
        return False, "Error al procesar el archivo JSON"
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"
        """, language="python")
        
        st.markdown("""
        **Explicación:**
        - **Session State**: Mantiene datos persistentes durante la sesión
        - **Validación de integridad**: Verifica consistencia de IDs y referencias
        - **Exportación/Importación**: Permite backup y restauración de datos
        - **Manejo de errores**: Captura y reporta problemas de datos
        """)
