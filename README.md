# 🎓 Curso Streamlit Interactivo

Un curso completo e interactivo para aprender Streamlit desde cero hasta aplicaciones avanzadas, diseñado por **Daniel Mardones**.

## ✨ Características

- **Estructura modular** organizada por niveles de dificultad
- **Gestión avanzada de estado** para evitar errores del DOM
- **Keys únicas** para todos los widgets
- **Interfaz limpia** con pestañas y contenedores
- **Código de ejemplo** ejecutable en cada lección
- **Sistema de evaluación interactivo** con quiz y ejercicios
- **Navegación profesional** y configuración optimizada

## 🏗️ Arquitectura del Proyecto

```
curso-streamlit/
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias actualizadas
├── modulo_01_fundamentos/  # ✅ Módulo 1: Fundamentos
│   ├── __init__.py
│   ├── hello_world.py      # Clase 1: Hello, Streamlit
│   ├── widgets_basicos.py  # Clase 2: Widgets básicos  
│   └── sidebar_layout.py   # Clase 3: Sidebar y layout
├── modulo_02_visualizacion/    # ✅ Módulo 2: Visualización
│   ├── __init__.py
│   ├── graficos_basicos.py     # Clase 1: Gráficos básicos
│   └── dashboards_interactivos.py # Clase 2: Dashboards interactivos
├── modulo_03_interactividad/   # ✅ Módulo 3: Interactividad
│   ├── __init__.py
│   └── manejo_datos.py         # Clase 1: Manejo de datos
├── modulo_04_aplicaciones/     # ✅ Módulo 4: Aplicaciones
│   ├── __init__.py
│   ├── calculadora_financiera.py  # Clase 1: Calculadora financiera
│   └── sistema_inventario.py      # Clase 2: Sistema de inventario
├── modulo_05_despliegue/       # ✅ Módulo 5: Despliegue
│   ├── __init__.py
│   └── streamlit_cloud.py      # Clase 1: Streamlit Cloud
├── modulo_06_bonus_automatizacion/ # ✅ Bonus: Automatización
│   ├── __init__.py
│   └── github_actions.py       # Clase 1: GitHub Actions
└── modulo_07_evaluacion/       # 🆕 Módulo 7: Evaluación
    ├── __init__.py
    └── test_interactivo.py     # Clase 1: Test Interactivo
```

## 🎯 Módulos Disponibles

### ✅ Módulo 1: Fundamentos
- **Clase 1:** Hello, Streamlit - Primeros pasos
- **Clase 2:** Widgets básicos - Inputs y controles
- **Clase 3:** Sidebar y layout - Organización visual

### ✅ Módulo 2: Visualización
- **Clase 1:** Gráficos básicos - Charts con Plotly
- **Clase 2:** Dashboards interactivos - Métricas y KPIs

### ✅ Módulo 3: Interactividad
- **Clase 1:** Manejo de datos - Session state y cache

### ✅ Módulo 4: Aplicaciones
- **Clase 1:** Calculadora financiera - App práctica
- **Clase 2:** Sistema de inventario - CRUD completo

### ✅ Módulo 5: Despliegue
- **Clase 1:** Streamlit Cloud - Configuración y secretos

### ✅ Bonus: Automatización
- **Clase 1:** GitHub Actions - CI/CD automatizado

### 🆕 Módulo 7: Evaluación
- **Clase 1:** Test Interactivo - Quiz, ejercicios y proyectos

## 🚀 Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/Denniels/curso-streamlit.git
cd curso-streamlit
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

#### ⭐ Versión Final - V5.0 (Completo + Evaluación Interactiva)
```bash
streamlit run main.py
```

## 🛡️ Mejoras Implementadas para la Estabilidad

### ✅ Gestión de Estado Optimizada
- **Una sola configuración de página** en `main.py`
- **Sistema de limpieza automática** de estado entre módulos
- **Keys únicas** generadas automáticamente para cada widget
- **Prevención de conflictos** entre componentes

### ✅ Arquitectura Robusta
- **Separación de responsabilidades** por módulos
- **11 clases interactivas** completamente funcionales
- **Contenedores seguros** (`st.container()`) para encapsular widgets
- **Debug opcional** para monitorear el estado de la aplicación

### ✅ Prevención de Errores DOM
- Eliminación de múltiples llamadas a `st.set_page_config()`
- Limpieza automática de widgets al cambiar entre módulos
- Keys únicas y consistentes para evitar conflictos
- Gestión centralizada del estado de la aplicación

### 🆕 Sistema de Evaluación Interactivo
- **Quiz teórico** con 8 preguntas sobre conceptos clave
- **Ejercicios prácticos** de programación con validación automática
- **Proyectos guiados** paso a paso (analizador de stocks, trivia, etc.)
- **Sistema de puntuación** y seguimiento de progreso
- **Historial de resultados** exportable

## 📚 Contenido Completo del Curso

### ✅ Módulo 1: Fundamentos
- **Clase 1**: Hello, Streamlit - Primeros pasos y configuración
- **Clase 2**: Widgets básicos - Inputs, botones y controles
- **Clase 3**: Sidebar y layout - Organización visual y columnas

### ✅ Módulo 2: Visualización
- **Clase 1**: Gráficos básicos - Plotly, matplotlib, y charts nativos
- **Clase 2**: Dashboards interactivos - Métricas, KPIs y layouts avanzados

### ✅ Módulo 3: Interactividad  
- **Clase 1**: Manejo de datos - Session state, cache y flujo de datos

### ✅ Módulo 4: Aplicaciones
- **Clase 1**: Calculadora financiera - App práctica con cálculos VPN/TIR
- **Clase 2**: Sistema de inventario - CRUD completo con pandas

### ✅ Módulo 5: Despliegue
- **Clase 1**: Streamlit Cloud - Configuración, secretos y mejores prácticas

### ✅ Bonus: Automatización
- **Clase 1**: GitHub Actions - CI/CD para aplicaciones Streamlit

### 🆕 Módulo 7: Evaluación
- **Clase 1**: Test Interactivo - Quiz, ejercicios de código y proyectos guiados

## 🎯 Últimas Mejoras Implementadas (V5.0)

### � Sección 2 (Configuración) - Ampliada y Mejorada
- **Ejemplos prácticos de config.toml** para desarrollo, testing y producción
- **Scripts de utilidades** para diferentes ambientes
- **Demo interactiva** de configuración de temas
- **Configuración responsive** para dispositivos móviles
- **CSS personalizado** con ejemplos funcionales

### 🔍 Sección 4 (Monitoreo y Debug) - Completamente Renovada
- **Sistema de métricas en tiempo real** con gráficos interactivos
- **Error tracking avanzado** con Sentry integration
- **Analytics dashboard** con seguimiento de usuarios
- **Performance monitoring** con psutil
- **Ejemplos de código completos** para implementación

### 🆕 Módulo 7: Evaluación Interactiva
- **Quiz teórico** con 8 preguntas validadas automáticamente
- **4 ejercicios prácticos** de código con validación segura:
  - Calculadora básica
  - Dashboard de datos
  - Sistema de login
  - Analizador de sentimientos
- **Proyectos guiados** paso a paso:
  - Analizador de stocks con métricas financieras
  - Juego de trivia interactivo
  - Generador de reportes automáticos
  - Chatbot simple con respuestas inteligentes
- **Sistema de puntuación** y seguimiento de progreso
- **Exportación de resultados** en JSON

### 🔧 Mejoras Técnicas
- **Corrección de tipos mixtos** en widgets (number_input, slider)
- **Keys únicos dinámicos** para evitar duplicados
- **Limpieza de warnings** de pandas y plotly
- **Actualización de métodos deprecados**
- **Estructura de imports optimizada**

## 🚀 Funcionalidades Destacadas

### 📝 Sistema de Quiz Inteligente
```python
# Evaluación automática con explicaciones
def evaluar_quiz(preguntas):
    respuestas_correctas = sum(1 for answer in st.session_state.quiz_answers.values() if answer['correcta'])
    porcentaje = (respuestas_correctas / total_preguntas) * 100
    
    # Feedback personalizado
    if porcentaje >= 80:
        st.success("🏆 ¡Excelente!")
    elif porcentaje >= 60:
        st.info("👍 Bien hecho")
    else:
        st.warning("📚 Sigue estudiando")
```

### 💻 Validación Segura de Código
```python
def ejecutar_codigo_seguro(codigo, tipo):
    # Verificaciones de seguridad
    palabras_prohibidas = ['import os', 'import sys', 'exec(', 'eval(']
    
    for palabra in palabras_prohibidas:
        if palabra in codigo:
            st.error(f"❌ Código no permitido: uso de '{palabra}'")
            return
    
    # Validación específica por tipo de ejercicio
    if tipo == "calculadora":
        if "st.title" in codigo and "st.number_input" in codigo:
            st.success("✅ ¡Excelente! Tu calculadora tiene todos los elementos básicos.")
```

### 📊 Analytics Avanzado
```python
class StreamlitAnalytics:
    def track_event(self, event_name: str, properties: dict = None):
        event_data = {
            'timestamp': datetime.now(),
            'session_id': st.session_state.session_id,
            'event_name': event_name,
            'properties': properties or {}
        }
        st.session_state.analytics_data.append(event_data)
```

## 📋 Checklist de Completado

- ✅ **11 clases interactivas** funcionando correctamente
- ✅ **Navegación DOM-safe** sin errores de elementos duplicados  
- ✅ **Sistema de evaluación** completo con quiz y ejercicios
- ✅ **Monitoreo avanzado** con métricas en tiempo real
- ✅ **Configuración profesional** para múltiples ambientes
- ✅ **Error handling robusto** con logging y tracking
- ✅ **Código limpio** sin warnings ni deprecaciones
- ✅ **Documentación actualizada** con ejemplos prácticos
- ✅ **Exportación de progreso** y resultados

## 🎓 Listo para Uso Educativo

El curso está completamente funcional y listo para ser usado como herramienta educativa. Incluye desde conceptos básicos hasta técnicas avanzadas de desarrollo y despliegue de aplicaciones Streamlit, con un sistema de evaluación que permite medir el progreso del aprendizaje.

**Total de contenido**: 11 clases interactivas + sistema de evaluación completo

---
widget_key = safe_widget_key("mi_widget")
```

### Debug y Monitoreo
- Panel de debug opcional en sidebar
- Visualización del estado actual de la aplicación
- Conteo de keys activas por módulo

## 🎯 Mejores Prácticas Implementadas

1. **Una sola llamada a `st.set_page_config()`** al inicio
2. **Keys únicas** para todos los widgets interactivos
3. **Limpieza automática** de estado entre módulos
4. **Contenedores seguros** para encapsular componentes
5. **Gestión centralizada** del estado de la aplicación
6. **Arquitectura modular** escalable

## 🐛 Solución de Problemas

### Error "removeChild DOM"
Este error ha sido solucionado mediante:
- ✅ Configuración única de página
- ✅ Keys únicas para widgets
- ✅ Limpieza automática de estado
- ✅ Gestión centralizada del estado

### Debug
Activar el panel de debug en el sidebar para monitorear:
- Módulo actual activo
- Keys de widgets en memoria
- Estado de la aplicación

## 👨‍💻 Autor

**Daniel Mardones**  
Mentor técnico en Python y Data Science  
[GitHub](https://github.com/Denniels)

---

¡Aprende Streamlit de forma interactiva y construye aplicaciones web increíbles! 🚀