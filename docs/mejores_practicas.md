# 📋 Guía de Mejores Prácticas - Streamlit

Esta guía contiene las mejores prácticas implementadas en el curso para evitar errores del DOM y crear aplicaciones Streamlit robustas.

## 🚫 Errores Comunes a Evitar

### 1. Múltiples `st.set_page_config()`
❌ **NUNCA hagas esto:**
```python
# En main.py
st.set_page_config(title="Main")

# En módulo.py
def run():
    st.set_page_config(title="Módulo")  # ❌ ERROR!
```

✅ **Hazlo así:**
```python
# Solo en main.py al inicio
st.set_page_config(
    page_title="Curso Streamlit",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### 2. Keys Duplicados o Inconsistentes
❌ **NUNCA hagas esto:**
```python
# Mismo key en diferentes módulos
boton1 = st.button("Click", key="mi_boton")  # Módulo A
boton2 = st.button("Click", key="mi_boton")  # Módulo B ❌ CONFLICTO!
```

✅ **Hazlo así:**
```python
from utils.state_manager import safe_widget_key

# Keys únicos automáticos
boton1 = st.button("Click", key=safe_widget_key("boton_principal"))
boton2 = st.button("Click", key=safe_widget_key("boton_secundario"))
```

### 3. No Limpiar Estado Entre Módulos
❌ **NUNCA hagas esto:**
```python
def modulo_a():
    # Crear widgets sin gestión de estado
    valor = st.slider("Mi slider", key="slider1")

def modulo_b():
    # Estado anterior puede causar conflictos
    valor = st.slider("Otro slider", key="slider1")  # ❌ CONFLICTO!
```

✅ **Hazlo así:**
```python
from utils.state_manager import set_current_module, safe_widget_key

def modulo_a():
    set_current_module('modulo_a', ['slider_', 'boton_'])
    valor = st.slider("Mi slider", key=safe_widget_key("principal"))

def modulo_b():
    set_current_module('modulo_b', ['slider_', 'boton_'])
    valor = st.slider("Otro slider", key=safe_widget_key("principal"))
```

## ✅ Mejores Prácticas

### 1. Estructura de Archivos Recomendada
```
proyecto/
├── main.py                    # Configuración única de página
├── requirements.txt           # Dependencias
├── utils/
│   ├── __init__.py
│   └── state_manager.py       # Gestión centralizada de estado
├── modulo_1/
│   ├── __init__.py
│   ├── clase_1.py
│   └── clase_2.py
└── modulo_2/
    ├── __init__.py
    └── clase_1.py
```

### 2. Template para Nuevos Módulos
```python
import streamlit as st
from utils.state_manager import set_current_module, safe_widget_key

def run():
    # 1. Configurar módulo y limpiar estado anterior
    set_current_module('mi_modulo', ['prefijos_', 'a_', 'limpiar_'])
    
    # 2. Título y descripción
    st.title("🎯 Mi Módulo")
    st.markdown("Descripción del módulo...")
    
    # 3. Contenido en contenedores seguros
    with st.container():
        # 4. Widgets con keys únicas
        valor = st.slider("Mi slider", 0, 100, 50, 
                         key=safe_widget_key("slider_principal"))
        
        if st.button("Mi botón", key=safe_widget_key("boton_accion")):
            st.success(f"Valor seleccionado: {valor}")
```

### 3. Gestión de Estado en main.py
```python
import streamlit as st
from utils.state_manager import initialize_app_state, display_debug_info

# Configuración única de página
st.set_page_config(...)

# Inicializar estado global
initialize_app_state()

# Tu lógica de navegación aquí...

# Debug opcional (solo desarrollo)
display_debug_info()
```

### 4. Uso de Contenedores Seguros
```python
# Envolver contenido en contenedores
with st.container():
    # Pestañas para organizar contenido
    tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
    
    with tab1:
        # Widgets específicos del tab
        pass
    
    with tab2:
        # Más widgets
        pass
```

### 5. Limpieza Automática de Estado
```python
# El sistema limpia automáticamente cuando cambias de módulo
current_selection = f"{modulo}_{clase}"
if 'last_selection' not in st.session_state or st.session_state.last_selection != current_selection:
    # Auto-limpieza de widgets específicos
    for key in list(st.session_state.keys()):
        if key.startswith(('boton_', 'slider_', 'input_')):
            del st.session_state[key]
    st.session_state.last_selection = current_selection
```

## 🔧 Utilidades Disponibles

### `set_current_module(module_name, clean_prefixes=None)`
Establece el módulo actual y limpia estado anterior si es necesario.

### `safe_widget_key(base_key, module_name=None)`
Genera keys únicos y seguros para widgets.

### `clear_module_state(module_prefixes)`
Limpia estado de widgets específicos.

### `initialize_app_state()`
Inicializa el estado global de la aplicación.

### `display_debug_info()`
Muestra información de debug del estado actual.

## 🎯 Checklist para Nuevos Módulos

- [ ] Una sola llamada a `st.set_page_config()` en main.py
- [ ] Importar y usar `set_current_module()` al inicio
- [ ] Keys únicos usando `safe_widget_key()`
- [ ] Contenedores seguros (`st.container()`, `st.tabs()`)
- [ ] Limpieza de estado apropiada
- [ ] Documentación clara del módulo
- [ ] Testing en diferentes navegadores

## 🐛 Debug y Troubleshooting

### Activar Debug
```python
# En main.py, después de la navegación
from utils.state_manager import display_debug_info
display_debug_info()
```

### Información que muestra:
- Módulo actual activo
- Última selección de navegación
- Total de keys en sesión
- Keys de widgets activos

### Señales de Problemas
- Keys duplicados en el debug
- Error "removeChild" en consola del navegador
- Widgets que no responden correctamente
- Estado que persiste entre módulos incorrectamente

---

**¡Siguiendo estas prácticas tendrás aplicaciones Streamlit robustas y libres de errores del DOM!** 🚀
