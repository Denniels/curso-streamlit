# 🎓 Curso Streamlit Interactivo

Un curso completo e interactivo para aprender Streamlit desde cero hasta aplicaciones avanzadas, diseñado por **Daniel Mardones**.

## ✨ Características

- **Estructura modular** organizada por niveles de dificultad
- **Gestión avanzada de estado** para evitar errores del DOM
- **Keys únicas** para todos los widgets
- **Interfaz limpia** con pestañas y contenedores
- **Código de ejemplo** ejecutable en cada lección

## 🏗️ Arquitectura del Proyecto

```
curso-streamlit/
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias
├── utils/                  # Utilidades compartidas
│   ├── __init__.py
│   └── state_manager.py    # Gestión segura del estado
├── modulo_01_fundamentos/  # Módulo 1: Fundamentos
│   ├── __init__.py
│   ├── hello_world.py      # Clase 1: Hello, Streamlit
│   ├── widgets_basicos.py  # Clase 2: Widgets básicos  
│   └── sidebar_layout.py   # Clase 3: Sidebar y layout
├── modulo_02_visualizacion/    # (En construcción)
├── modulo_03_interactividad/   # (En construcción)
├── modulo_04_aplicaciones/     # (En construcción)
├── modulo_05_despliegue/       # (En construcción)
└── modulo_06_bonus_automatizacion/ # (En construcción)
```

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

#### ⭐ Versión Recomendada - V4.1 (DOM-Safe + Navegación Corregida)
```bash
streamlit run main_v4_fixed.py --server.headless true
```

#### Versión V4.0 (Problemas de navegación conocidos)
```bash
streamlit run main_v4.py --server.headless true
```

#### Versión V3 (Solo DOM-Safe)
```bash
streamlit run main_v3.py --server.headless true
```

#### Versión Original
```bash
streamlit run main.py
```

**⚡ Recomendación**: Usa `main_v4_fixed.py` que resuelve los errores DOM y tiene navegación completamente funcional entre todos los módulos educativos.

## 🛡️ Mejoras Implementadas para la Estabilidad

### ✅ Gestión de Estado Optimizada
- **Una sola configuración de página** en `main.py`
- **Sistema de limpieza automática** de estado entre módulos
- **Keys únicas** generadas automáticamente para cada widget
- **Prevención de conflictos** entre componentes

### ✅ Arquitectura Robusta
- **Separación de responsabilidades** por módulos
- **Utilidades centralizadas** para gestión de estado
- **Contenedores seguros** (`st.container()`) para encapsular widgets
- **Debug opcional** para monitorear el estado de la aplicación

### ✅ Prevención de Errores DOM
- Eliminación de múltiples llamadas a `st.set_page_config()`
- Limpieza automática de widgets al cambiar entre módulos
- Keys únicas y consistentes para evitar conflictos
- Gestión centralizada del estado de la aplicación

## 📚 Contenido del Curso

### Módulo 1: Fundamentos ✅
- **Clase 1**: Hello, Streamlit - Primeros pasos
- **Clase 2**: Widgets básicos - Interactividad
- **Clase 3**: Sidebar y layout - Organización

### Módulos Futuros 🚧
- **Módulo 2**: Visualización de Datos
- **Módulo 3**: Interactividad Avanzada  
- **Módulo 4**: Aplicaciones Especializadas
- **Módulo 5**: Despliegue y Optimización
- **Bonus**: Automatización CI/CD

## 🔧 Características Técnicas

### Gestión de Estado
```python
from utils.state_manager import set_current_module, safe_widget_key

# Configurar módulo actual y limpiar estado anterior
set_current_module('mi_modulo', ['prefijos_', 'a_', 'limpiar_'])

# Generar keys seguras para widgets
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