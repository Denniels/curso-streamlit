"""
Gestor de estado robusto para Streamlit.
Soluciona problemas del DOM mediante técnicas avanzadas.
"""
import streamlit as st
import uuid
from typing import List, Optional

class StreamlitStateManager:
    """Gestor avanzado de estado para prevenir errores del DOM."""
    
    def __init__(self):
        self._initialize_core_state()
    
    def _initialize_core_state(self):
        """Inicializa el estado core de manera segura."""
        if '_state_manager_initialized' not in st.session_state:
            st.session_state._state_manager_initialized = True
            st.session_state._current_module = None
            st.session_state._widget_registry = {}
            st.session_state._cleanup_queue = []
    
    def safe_clear_state(self, prefixes: List[str] = None):
        """Limpia el estado de manera segura sin causar errores del DOM."""
        if prefixes is None:
            return
            
        # Marcar para limpieza en el próximo render
        for prefix in prefixes:
            keys_to_remove = [k for k in st.session_state.keys() if k.startswith(prefix)]
            for key in keys_to_remove:
                if key not in st.session_state._cleanup_queue:
                    st.session_state._cleanup_queue.append(key)
    
    def process_cleanup_queue(self):
        """Procesa la cola de limpieza de manera segura."""
        if hasattr(st.session_state, '_cleanup_queue'):
            for key in st.session_state._cleanup_queue[:]:
                if key in st.session_state:
                    try:
                        del st.session_state[key]
                        st.session_state._cleanup_queue.remove(key)
                    except:
                        # Si falla, lo dejamos para el próximo ciclo
                        pass
    
    def set_module(self, module_name: str, clean_prefixes: List[str] = None):
        """Establece el módulo actual de manera segura."""
        self._initialize_core_state()
        
        # Procesar limpieza pendiente
        self.process_cleanup_queue()
        
        # Solo limpiar si realmente cambió el módulo
        if st.session_state._current_module != module_name:
            if clean_prefixes:
                self.safe_clear_state(clean_prefixes)
            st.session_state._current_module = module_name
    
    def generate_safe_key(self, base_key: str, module_name: str = None) -> str:
        """Genera una key única y segura para widgets."""
        current_module = module_name or st.session_state.get('_current_module', 'unknown')
        
        # Usar un formato que incluya el módulo y sea único
        safe_key = f"{current_module}_{base_key}_{id(self)}"
        
        # Registrar la key
        if '_widget_registry' not in st.session_state:
            st.session_state._widget_registry = {}
        st.session_state._widget_registry[safe_key] = True
        
        return safe_key
    
    def force_rerun_safe(self):
        """Fuerza un rerun de manera segura."""
        # Limpiar registro de widgets para evitar conflictos
        if '_widget_registry' in st.session_state:
            st.session_state._widget_registry.clear()
        st.rerun()

# Instancia global del gestor
_state_manager = StreamlitStateManager()

def initialize_app_state():
    """Inicializa el estado global de la aplicación."""
    _state_manager._initialize_core_state()

def set_current_module(module_name: str, clean_prefixes: List[str] = None):
    """Establece el módulo actual y limpia estado anterior si es necesario."""
    _state_manager.set_module(module_name, clean_prefixes)

def safe_widget_key(base_key: str, module_name: str = None) -> str:
    """Genera una key única y segura para widgets."""
    return _state_manager.generate_safe_key(base_key, module_name)

def clear_module_state(module_prefixes: List[str]):
    """Limpia el estado de widgets específicos de un módulo."""
    _state_manager.safe_clear_state(module_prefixes)

def display_debug_info():
    """Muestra información de debug del estado (solo para desarrollo)."""
    if st.sidebar.checkbox("🐛 Debug State", key="debug_checkbox_main"):
        st.sidebar.write("**Estado actual:**")
        
        debug_info = {
            "current_module": st.session_state.get('_current_module'),
            "total_keys": len(st.session_state.keys()),
            "cleanup_queue_size": len(st.session_state.get('_cleanup_queue', [])),
            "widget_registry_size": len(st.session_state.get('_widget_registry', {}))
        }
        
        st.sidebar.json(debug_info)
        
        if st.sidebar.button("🧹 Limpiar Todo", key="clear_all_state"):
            # Limpiar todo excepto las keys esenciales
            essential_keys = ['_state_manager_initialized', '_current_module', '_widget_registry', '_cleanup_queue']
            keys_to_remove = [k for k in st.session_state.keys() if k not in essential_keys]
            
            for key in keys_to_remove:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.sidebar.success("Estado limpiado")
            _state_manager.force_rerun_safe()
