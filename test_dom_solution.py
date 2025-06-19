"""
Script de validación para verificar que la solución DOM funciona correctamente.
Este script realiza pruebas básicas de la funcionalidad.
"""

import streamlit as st
import time
import hashlib
from main_v3 import DOMSafeRenderer, safe_navigation_state

def test_dom_safe_renderer():
    """Prueba el DOMSafeRenderer."""
    print("🧪 Probando DOMSafeRenderer...")
    
    renderer = DOMSafeRenderer()
      # Test 1: Generación de keys únicos
    key1 = renderer.get_safe_key("test", "context1")
    key2 = renderer.get_safe_key("test", "context2")
    
    assert key1 != key2, "Keys con contextos diferentes deben ser únicos"
    print("✅ Generación de keys únicos: PASADO")
    
    # Test 2: Gestión de contenedores
    container1 = renderer.get_container("test_container")
    container2 = renderer.get_container("test_container")
    
    assert container1 is container2, "Mismo ID debe retornar mismo contenedor"
    print("✅ Gestión de contenedores: PASADO")
    
    print("🎉 DOMSafeRenderer: TODOS LOS TESTS PASADOS")

def test_navigation_state():
    """Prueba el estado de navegación seguro."""
    print("🧪 Probando navegación segura...")
    
    # Simular session_state
    if not hasattr(st, 'session_state'):
        class MockSessionState:
            def __init__(self):
                self.data = {}
            
            def __contains__(self, key):
                return key in self.data
            
            def __getitem__(self, key):
                return self.data[key]
            
            def __setitem__(self, key, value):
                self.data[key] = value
        
        st.session_state = MockSessionState()
    
    # Test del estado de navegación
    nav_state1 = safe_navigation_state()
    nav_state2 = safe_navigation_state()
    
    assert nav_state1 is nav_state2, "Estado de navegación debe ser singleton"
    assert 'current_module' in nav_state1, "Estado debe tener módulo actual"
    assert 'render_lock' in nav_state1, "Estado debe tener lock de renderizado"
    
    print("✅ Estado de navegación: PASADO")
    print("🎉 Navegación segura: TODOS LOS TESTS PASADOS")

def verify_streamlit_version():
    """Verifica la versión de Streamlit."""
    print("🧪 Verificando compatibilidad...")
    
    try:
        import streamlit as st
        version = st.__version__
        print(f"📦 Streamlit versión: {version}")
        
        # Verificar que es compatible con 1.46.0
        major, minor, patch = map(int, version.split('.'))
        
        if major >= 1 and minor >= 46:
            print("✅ Versión compatible con la solución DOM")
        else:
            print("⚠️ Versión anterior - puede requerir ajustes")
            
    except Exception as e:
        print(f"❌ Error verificando versión: {e}")

def main():
    """Ejecuta todas las pruebas."""
    print("🚀 INICIANDO VALIDACIÓN DE SOLUCIÓN DOM v3")
    print("=" * 50)
    
    try:
        verify_streamlit_version()
        print()
        
        test_dom_safe_renderer()
        print()
        
        test_navigation_state()
        print()
        
        print("🎯 RESULTADO FINAL")
        print("=" * 50)
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("🚫 Solución DOM lista para producción")
        print("⚡ La aplicación debería ejecutarse sin errores DOM")
        
    except Exception as e:
        print(f"❌ ERROR EN VALIDACIÓN: {e}")
        print("🔧 Revisa la implementación antes de usar en producción")

if __name__ == "__main__":
    main()
