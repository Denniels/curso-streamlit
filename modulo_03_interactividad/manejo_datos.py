import streamlit as st
import pandas as pd
import numpy as np
import io

def run():
    """Módulo de Manejo de Datos y Archivos."""
    
    with st.container():
        st.title("📁 Clase 1: Manejo de Datos y Archivos")
        st.markdown("""
        Aprende a cargar, procesar y analizar datos desde diferentes fuentes.
        Streamlit hace que trabajar con archivos sea súper fácil.
        """)
        
        # Pestañas para diferentes aspectos del manejo de datos
        tab1, tab2, tab3, tab4 = st.tabs([
            "📤 Upload de Archivos",
            "🔍 Exploración de Datos",
            "✏️ Edición Interactiva", 
            "💾 Descarga de Resultados"
        ])
        
        with tab1:
            st.subheader("📤 Carga y Validación de Archivos")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Opciones de carga:**")
                
                # Selector de tipo de archivo
                tipo_archivo = st.selectbox(
                    "Tipo de archivo",
                    ["CSV", "Excel", "JSON", "Datos de Ejemplo"],
                    key="upload_tipo"
                )
                
                # Upload de archivo
                if tipo_archivo != "Datos de Ejemplo":
                    if tipo_archivo == "CSV":
                        uploaded_file = st.file_uploader(
                            "Selecciona un archivo CSV",
                            type=['csv'],
                            key="upload_csv"
                        )
                        
                        if uploaded_file:
                            # Opciones de parsing CSV
                            separador = st.selectbox("Separador", [",", ";", "\t", "|"], key="csv_sep")
                            encoding = st.selectbox("Encoding", ["utf-8", "latin-1", "cp1252"], key="csv_enc")
                            
                    elif tipo_archivo == "Excel":
                        uploaded_file = st.file_uploader(
                            "Selecciona un archivo Excel",
                            type=['xlsx', 'xls'],
                            key="upload_excel"
                        )
                        
                        if uploaded_file:
                            # Mostrar hojas disponibles sería ideal, pero requiere carga previa
                            sheet_name = st.text_input("Nombre de la hoja (opcional)", key="excel_sheet")
                            
                    else:  # JSON
                        uploaded_file = st.file_uploader(
                            "Selecciona un archivo JSON",
                            type=['json'],
                            key="upload_json"
                        )
                else:
                    uploaded_file = None
                
                # Generar datos de ejemplo
                if tipo_archivo == "Datos de Ejemplo":
                    tipo_ejemplo = st.selectbox(
                        "Tipo de datos",
                        ["Ventas", "Empleados", "Productos", "Finanzas"],
                        key="ejemplo_tipo"
                    )
            
            with col2:
                # Procesar archivo cargado o generar ejemplo
                df = None
                
                if tipo_archivo == "Datos de Ejemplo":
                    # Generar datos de ejemplo según el tipo
                    np.random.seed(42)
                    
                    if tipo_ejemplo == "Ventas":
                        df = pd.DataFrame({
                            'fecha': pd.date_range('2024-01-01', periods=100, freq='D'),
                            'producto': np.random.choice(['Laptop', 'Mouse', 'Teclado', 'Monitor'], 100),
                            'vendedor': np.random.choice(['Ana', 'Carlos', 'María', 'Juan'], 100),
                            'cantidad': np.random.randint(1, 10, 100),
                            'precio': np.random.uniform(50, 1500, 100)
                        })
                        df['total'] = df['cantidad'] * df['precio']
                        
                    elif tipo_ejemplo == "Empleados":
                        df = pd.DataFrame({
                            'nombre': [f'Empleado_{i}' for i in range(1, 51)],
                            'departamento': np.random.choice(['IT', 'Ventas', 'Marketing', 'RRHH', 'Finanzas'], 50),
                            'salario': np.random.normal(50000, 15000, 50),
                            'experiencia': np.random.randint(1, 20, 50),
                            'edad': np.random.randint(22, 65, 50)
                        })
                        
                    elif tipo_ejemplo == "Productos":
                        df = pd.DataFrame({
                            'codigo': [f'PROD_{i:03d}' for i in range(1, 31)],
                            'nombre': [f'Producto {i}' for i in range(1, 31)],
                            'categoria': np.random.choice(['Electrónicos', 'Ropa', 'Hogar', 'Deportes'], 30),
                            'precio': np.random.uniform(10, 500, 30),
                            'stock': np.random.randint(0, 100, 30),
                            'calificacion': np.random.uniform(1, 5, 30)
                        })
                        
                    else:  # Finanzas
                        fechas = pd.date_range('2024-01-01', periods=365, freq='D')
                        precio_inicial = 100
                        cambios = np.random.normal(0, 0.02, 365)
                        precios = [precio_inicial]
                        for cambio in cambios[1:]:
                            precios.append(precios[-1] * (1 + cambio))
                        
                        df = pd.DataFrame({
                            'fecha': fechas,
                            'precio': precios,
                            'volumen': np.random.randint(1000, 50000, 365),
                            'sector': np.random.choice(['Tecnología', 'Salud', 'Energía', 'Finanzas'], 365)
                        })
                
                elif uploaded_file is not None:
                    try:
                        if tipo_archivo == "CSV":
                            df = pd.read_csv(uploaded_file, sep=separador, encoding=encoding)
                        elif tipo_archivo == "Excel":
                            if sheet_name:
                                df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                            else:
                                df = pd.read_excel(uploaded_file)
                        else:  # JSON
                            df = pd.read_json(uploaded_file)
                        
                        st.success(f"✅ Archivo cargado exitosamente: {uploaded_file.name}")
                        
                    except Exception as e:
                        st.error(f"❌ Error al cargar el archivo: {str(e)}")
                
                # Mostrar información del dataset
                if df is not None:
                    st.markdown("**📊 Información del Dataset:**")
                    
                    col_info1, col_info2, col_info3 = st.columns(3)
                    with col_info1:
                        st.metric("📏 Filas", len(df))
                    with col_info2:
                        st.metric("📐 Columnas", len(df.columns))
                    with col_info3:
                        st.metric("💾 Tamaño", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
                    
                    # Vista previa
                    st.markdown("**👀 Vista Previa:**")
                    st.dataframe(df.head(10), use_container_width=True)
            
            if df is not None:
                # Guardar en session_state para usar en otras pestañas
                st.session_state['dataset_actual'] = df
                
                st.code("""
# Cargar archivo CSV
uploaded_file = st.file_uploader("Selecciona archivo CSV", type=['csv'])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
    
# También funciona con Excel y JSON
df_excel = pd.read_excel(uploaded_file)
df_json = pd.read_json(uploaded_file)
""", language="python")
        
        with tab2:
            st.subheader("🔍 Exploración Interactiva de Datos")
            
            # Verificar si hay datos cargados
            if 'dataset_actual' not in st.session_state:
                st.warning("⚠️ Primero carga un dataset en la pestaña 'Upload de Archivos'")
                return
            
            df = st.session_state['dataset_actual']
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**🎛️ Controles de Exploración:**")
                
                # Selector de columnas para análisis
                columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
                columnas_categoricas = df.select_dtypes(include=['object', 'category']).columns.tolist()
                
                if columnas_numericas:
                    columna_numerica = st.selectbox(
                        "Columna numérica para análisis",
                        columnas_numericas,
                        key="explora_numerica"
                    )
                
                if columnas_categoricas:
                    columna_categorica = st.selectbox(
                        "Columna categórica para análisis",
                        ["Ninguna"] + columnas_categoricas,
                        key="explora_categorica"
                    )
                
                # Opciones de visualización
                mostrar_estadisticas = st.checkbox("Mostrar estadísticas", value=True, key="explora_stats")
                mostrar_nulos = st.checkbox("Mostrar valores nulos", value=True, key="explora_nulos")
                mostrar_distribucion = st.checkbox("Mostrar distribución", value=True, key="explora_dist")
            
            with col2:
                # Estadísticas generales
                if mostrar_estadisticas:
                    st.markdown("**📊 Estadísticas Descriptivas:**")
                    if columnas_numericas:
                        st.dataframe(df[columnas_numericas].describe(), use_container_width=True)
                
                # Análisis de valores nulos
                if mostrar_nulos:
                    st.markdown("**🕳️ Valores Nulos por Columna:**")
                    nulos = df.isnull().sum()
                    nulos_df = pd.DataFrame({
                        'Columna': nulos.index,
                        'Valores Nulos': nulos.values,
                        'Porcentaje': (nulos.values / len(df) * 100).round(2)
                    })
                    st.dataframe(nulos_df[nulos_df['Valores Nulos'] > 0], use_container_width=True)
                
                # Distribución de la columna seleccionada
                if mostrar_distribucion and 'columna_numerica' in locals():
                    st.markdown(f"**📈 Distribución de '{columna_numerica}':**")
                    
                    import plotly.express as px
                    
                    if columna_categorica != "Ninguna":
                        # Distribución por categoría
                        fig = px.box(df, x=columna_categorica, y=columna_numerica,
                                   title=f"Distribución de {columna_numerica} por {columna_categorica}")
                    else:
                        # Histograma simple
                        fig = px.histogram(df, x=columna_numerica, nbins=30,
                                         title=f"Distribución de {columna_numerica}")
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            # Filtros interactivos
            st.markdown("### 🎯 Filtros Interactivos")
            
            # Crear filtros para cada columna
            filtros_aplicados = {}
            
            col_filt1, col_filt2, col_filt3 = st.columns(3)
            columnas_para_filtros = list(df.columns)[:3]  # Limitar a 3 para el ejemplo
            
            for i, columna in enumerate(columnas_para_filtros):
                with [col_filt1, col_filt2, col_filt3][i]:
                    if df[columna].dtype in ['int64', 'float64']:
                        # Filtro numérico
                        min_val, max_val = float(df[columna].min()), float(df[columna].max())
                        rango = st.slider(
                            f"{columna}",
                            min_val, max_val, (min_val, max_val),
                            key=f"filtro_{columna}"
                        )
                        filtros_aplicados[columna] = rango
                    else:
                        # Filtro categórico
                        valores_unicos = df[columna].unique()
                        seleccionados = st.multiselect(
                            f"{columna}",
                            valores_unicos,
                            default=valores_unicos[:5] if len(valores_unicos) > 5 else valores_unicos,
                            key=f"filtro_{columna}"
                        )
                        filtros_aplicados[columna] = seleccionados
            
            # Aplicar filtros
            df_filtrado = df.copy()
            for columna, filtro in filtros_aplicados.items():
                if df[columna].dtype in ['int64', 'float64']:
                    df_filtrado = df_filtrado[
                        (df_filtrado[columna] >= filtro[0]) & 
                        (df_filtrado[columna] <= filtro[1])
                    ]
                else:
                    if filtro:  # Si hay valores seleccionados
                        df_filtrado = df_filtrado[df_filtrado[columna].isin(filtro)]
            
            # Mostrar datos filtrados
            st.markdown(f"**📋 Datos Filtrados ({len(df_filtrado)} de {len(df)} filas):**")
            st.dataframe(df_filtrado, use_container_width=True)
            
            # Guardar datos filtrados
            st.session_state['dataset_filtrado'] = df_filtrado
            
            st.code("""
# Exploración automática de datos
st.write("Estadísticas descriptivas:")
st.dataframe(df.describe())

st.write("Información de tipos de datos:")
st.write(df.dtypes)

st.write("Valores nulos:")
st.write(df.isnull().sum())

# Filtros numéricos - ejemplo genérico
# min_val = df['columna_numerica'].min()
# max_val = df['columna_numerica'].max()
# col_numerica = st.slider("Filtrar por columna", min_val, max_val, (min_val, max_val))
# df_filtrado = df[df['columna'].between(col_numerica[0], col_numerica[1])]
""", language="python")
        
        with tab3:
            st.subheader("✏️ Edición Interactiva de Datos")
            
            if 'dataset_filtrado' not in st.session_state:
                st.warning("⚠️ Primero explora los datos en la pestaña anterior")
                return
            
            df = st.session_state['dataset_filtrado'].copy()
            
            st.markdown("**🎛️ Opciones de Edición:**")
            
            col_edit1, col_edit2 = st.columns(2)
            
            with col_edit1:
                modo_edicion = st.selectbox(
                    "Modo de edición",
                    ["Visualizar", "Editar valores", "Agregar fila", "Eliminar filas"],
                    key="modo_edicion"
                )
            
            with col_edit2:
                if modo_edicion != "Visualizar":
                    confirmar_cambios = st.button("💾 Confirmar cambios", key="confirmar_cambios")
            
            if modo_edicion == "Visualizar":
                st.markdown("**👀 Vista de solo lectura:**")
                st.dataframe(df, use_container_width=True)
                
            elif modo_edicion == "Editar valores":
                st.markdown("**✏️ Editar valores existentes:**")
                
                # Seleccionar fila y columna para editar
                col_sel1, col_sel2, col_sel3 = st.columns(3)
                
                with col_sel1:
                    fila_editar = st.selectbox("Fila a editar", range(len(df)), key="fila_editar")
                
                with col_sel2:
                    columna_editar = st.selectbox("Columna a editar", df.columns, key="columna_editar")
                
                with col_sel3:
                    valor_actual = df.iloc[fila_editar][columna_editar]
                    st.write(f"Valor actual: **{valor_actual}**")
                
                # Input para nuevo valor
                if df[columna_editar].dtype in ['int64', 'float64']:
                    nuevo_valor = st.number_input("Nuevo valor", value=float(valor_actual), key="nuevo_valor_num")
                else:
                    nuevo_valor = st.text_input("Nuevo valor", value=str(valor_actual), key="nuevo_valor_text")
                
                # Vista previa del cambio
                df_preview = df.copy()
                df_preview.iloc[fila_editar, df_preview.columns.get_loc(columna_editar)] = nuevo_valor
                
                st.markdown("**👀 Vista previa con cambios:**")
                st.dataframe(df_preview, use_container_width=True)
                
                if confirmar_cambios:
                    st.session_state['dataset_filtrado'] = df_preview
                    st.success(f"✅ Valor actualizado en fila {fila_editar}, columna '{columna_editar}'")
                    st.rerun()
            
            elif modo_edicion == "Agregar fila":
                st.markdown("**➕ Agregar nueva fila:**")
                
                nueva_fila = {}
                cols = st.columns(min(len(df.columns), 4))
                
                for i, columna in enumerate(df.columns):
                    with cols[i % 4]:
                        if df[columna].dtype in ['int64', 'float64']:
                            valor = st.number_input(f"{columna}", key=f"new_{columna}")
                        else:
                            # Sugerir valores existentes
                            valores_existentes = df[columna].unique()[:5]
                            valor = st.text_input(
                                f"{columna}",
                                placeholder=f"ej: {valores_existentes[0] if len(valores_existentes) > 0 else ''}",
                                key=f"new_{columna}"
                            )
                        nueva_fila[columna] = valor
                
                # Vista previa de la nueva fila
                st.markdown("**👀 Nueva fila a agregar:**")
                st.json(nueva_fila)
                
                if confirmar_cambios:
                    df_nuevo = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
                    st.session_state['dataset_filtrado'] = df_nuevo
                    st.success("✅ Nueva fila agregada")
                    st.rerun()
            
            else:  # Eliminar filas
                st.markdown("**🗑️ Eliminar filas:**")
                
                filas_eliminar = st.multiselect(
                    "Selecciona filas a eliminar (por índice)",
                    range(len(df)),
                    key="filas_eliminar"
                )
                
                if filas_eliminar:
                    st.markdown(f"**⚠️ Se eliminarán {len(filas_eliminar)} filas:**")
                    st.dataframe(df.iloc[filas_eliminar], use_container_width=True)
                    
                    if confirmar_cambios:
                        df_nuevo = df.drop(filas_eliminar).reset_index(drop=True)
                        st.session_state['dataset_filtrado'] = df_nuevo
                        st.success(f"✅ {len(filas_eliminar)} filas eliminadas")
                        st.rerun()
            
            st.code("""
# Edición básica de DataFrames
# Nota: En Streamlit, la edición directa de DataFrames
# requiere manejo de session_state

# Agregar nueva fila
nueva_fila = {"columna1": valor1, "columna2": valor2}
df_nuevo = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)

# Eliminar filas
df_sin_filas = df.drop([indice1, indice2]).reset_index(drop=True)

# Modificar valores
df.loc[fila, 'columna'] = nuevo_valor
""", language="python")
        
        with tab4:
            st.subheader("💾 Descarga de Resultados")
            
            if 'dataset_filtrado' not in st.session_state:
                st.warning("⚠️ No hay datos procesados para descargar")
                return
            
            df = st.session_state['dataset_filtrado']
            
            st.markdown("**📊 Resumen de datos a descargar:**")
            col_info1, col_info2, col_info3, col_info4 = st.columns(4)
            
            with col_info1:
                st.metric("📏 Filas", len(df))
            with col_info2:
                st.metric("📐 Columnas", len(df.columns))
            with col_info3:
                st.metric("💾 Tamaño estimado", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            with col_info4:
                st.metric("🕒 Última modificación", "Ahora")
            
            # Opciones de descarga
            col_down1, col_down2 = st.columns(2)
            
            with col_down1:
                st.markdown("**📁 Formatos de descarga:**")
                
                # CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📄 Descargar como CSV",
                    data=csv,
                    file_name=f"datos_procesados_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key="download_csv"
                )
                
                # Excel
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name='Datos', index=False)
                
                st.download_button(
                    label="📊 Descargar como Excel",
                    data=buffer.getvalue(),
                    file_name=f"datos_procesados_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_excel"
                )
                
                # JSON
                json_data = df.to_json(orient='records', indent=2)
                st.download_button(
                    label="🗂️ Descargar como JSON",
                    data=json_data,
                    file_name=f"datos_procesados_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    key="download_json"
                )
            
            with col_down2:
                st.markdown("**👀 Vista previa de descarga:**")
                
                formato_preview = st.selectbox(
                    "Formato para vista previa",
                    ["CSV", "JSON", "Excel Info"],
                    key="preview_formato"
                )
                
                if formato_preview == "CSV":
                    st.code(df.to_csv(index=False)[:500] + "..." if len(df.to_csv(index=False)) > 500 else df.to_csv(index=False))
                elif formato_preview == "JSON":
                    st.json(df.head(3).to_dict('records'))
                else:  # Excel Info
                    st.write("**Información del archivo Excel:**")
                    st.write(f"- Hoja: 'Datos'")
                    st.write(f"- Filas: {len(df) + 1} (incluyendo headers)")
                    st.write(f"- Columnas: {len(df.columns)}")
                    st.write(f"- Headers: {', '.join(df.columns)}")
            
            # Estadísticas finales
            st.markdown("### 📈 Estadísticas del Procesamiento")
            
            if 'dataset_actual' in st.session_state:
                df_original = st.session_state['dataset_actual']
                
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                
                with col_stat1:
                    filas_removidas = len(df_original) - len(df)
                    st.metric("📉 Filas removidas", filas_removidas, delta=f"-{filas_removidas}")
                
                with col_stat2:
                    if len(df) > 0:
                        porcentaje_mantenido = (len(df) / len(df_original)) * 100
                        st.metric("💾 Datos mantenidos", f"{porcentaje_mantenido:.1f}%")
                
                with col_stat3:
                    columnas_modificadas = 0  # En una implementación real, trackearíamos esto
                    st.metric("✏️ Columnas modificadas", columnas_modificadas)
            
            st.code("""
# Generar y descargar archivos procesados

# CSV
csv = df.to_csv(index=False)
st.download_button(
    label="Descargar CSV",
    data=csv,
    file_name="datos.csv",
    mime="text/csv"
)

# Excel
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Datos', index=False)

st.download_button(
    label="Descargar Excel",
    data=buffer.getvalue(),
    file_name="datos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# JSON
json_data = df.to_json(orient='records', indent=2)
st.download_button(
    label="Descargar JSON",
    data=json_data,
    file_name="datos.json",
    mime="application/json"
)
""", language="python")
        
        # Conclusión del módulo
        st.markdown("---")
        st.markdown("### 🎯 ¿Qué aprendiste en esta clase?")
        st.markdown("""
        - **Upload de archivos** múltiples formatos (CSV, Excel, JSON)
        - **Exploración automática** de datasets con estadísticas descriptivas
        - **Filtros interactivos** para análisis de subconjuntos de datos
        - **Edición en tiempo real** de DataFrames
        - **Validación y limpieza** de datos de forma visual
        - **Descarga de resultados** en múltiples formatos
        - **Manejo de session_state** para persistir datos entre interacciones
        """)
        
        st.success("🎉 ¡Genial! Ahora puedes crear aplicaciones completas de análisis de datos.")
