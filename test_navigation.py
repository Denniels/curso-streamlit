"""
Test específico para validar navegación en main_v4_fixed.py
"""

import subprocess
import time
import sys
import os

def test_streamlit_app():
    """Prueba la aplicación Streamlit."""
    print("🧪 TESTING NAVEGACIÓN - MAIN_V4_FIXED.PY")
    print("=" * 50)
    
    # 1. Verificar estructura de archivos
    print("\n📁 VERIFICANDO ESTRUCTURA DE ARCHIVOS")
    print("-" * 30)
    
    required_files = [
        'main_v4_fixed.py',
        'modulo_01_fundamentos/hello_world.py',
        'modulo_01_fundamentos/widgets_basicos.py',
        'modulo_01_fundamentos/sidebar_layout.py'
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NO ENCONTRADO")
            all_files_exist = False
    
    if not all_files_exist:
        print("\n❌ FALTAN ARCHIVOS NECESARIOS")
        return False
    
    # 2. Verificar imports
    print("\n🔍 VERIFICANDO IMPORTS")
    print("-" * 30)
    
    # Agregar path para imports
    module_dir = os.path.join(os.path.dirname(__file__), 'modulo_01_fundamentos')
    sys.path.insert(0, module_dir)
    
    try:
        import hello_world
        print("✅ hello_world.py importado")
        
        import widgets_basicos
        print("✅ widgets_basicos.py importado")
        
        import sidebar_layout
        print("✅ sidebar_layout.py importado")
        
        # Verificar función run
        modules = [hello_world, widgets_basicos, sidebar_layout]
        for module in modules:
            if hasattr(module, 'run'):
                print(f"✅ {module.__name__}.run() disponible")
            else:
                print(f"❌ {module.__name__}.run() NO disponible")
                return False
                
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    
    # 3. Verificar sintaxis de main_v4_fixed.py
    print("\n📝 VERIFICANDO SINTAXIS")
    print("-" * 30)
    
    try:
        with open('main_v4_fixed.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Compilar para verificar sintaxis
        compile(content, 'main_v4_fixed.py', 'exec')
        print("✅ Sintaxis de main_v4_fixed.py es válida")
        
    except SyntaxError as e:
        print(f"❌ Error de sintaxis: {e}")
        return False
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")
        return False
    
    # 4. Verificar componentes clave
    print("\n🔧 VERIFICANDO COMPONENTES CLAVE")
    print("-" * 30)
    
    key_components = [
        ('import_modules', '@st.cache_resource'),
        ('render_sidebar_navigation', 'def render_sidebar_navigation'),
        ('render_main_content', 'def render_main_content'),
        ('class_to_module mapping', 'class_to_module = {'),
        ('module execution', 'current_module.run()')
    ]
    
    for component_name, search_string in key_components:
        if search_string in content:
            print(f"✅ {component_name}")
        else:
            print(f"❌ {component_name} - NO ENCONTRADO")
            return False
    
    print("\n🎉 TODAS LAS VERIFICACIONES PASARON")
    print("✅ main_v4_fixed.py debería funcionar correctamente")
    return True

def run_quick_test():
    """Ejecuta un test rápido del código."""
    print("\n🚀 EJECUTANDO TEST RÁPIDO")
    print("-" * 30)
    
    try:
        # Test de importación directa
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modulo_01_fundamentos'))
        
        import hello_world
        import widgets_basicos
        import sidebar_layout
        
        modules = {
            'hello_world': hello_world,
            'widgets_basicos': widgets_basicos,
            'sidebar_layout': sidebar_layout
        }
        
        class_to_module = {
            "Clase 1: Hello, Streamlit": modules['hello_world'],
            "Clase 2: Widgets básicos": modules['widgets_basicos'],
            "Clase 3: Sidebar y layout": modules['sidebar_layout']
        }
        
        print("✅ Mapeo de clases creado exitosamente")
        
        # Test de acceso a funciones
        for class_name, module in class_to_module.items():
            if hasattr(module, 'run'):
                print(f"✅ {class_name} -> {module.__name__}.run()")
            else:
                print(f"❌ {class_name} -> {module.__name__} SIN run()")
                return False
        
        print("✅ Todas las funciones run() están disponibles")
        return True
        
    except Exception as e:
        print(f"❌ Error en test rápido: {e}")
        return False

def main():
    """Ejecuta todos los tests."""
    print("🎯 VALIDACIÓN COMPLETA - MAIN_V4_FIXED.PY")
    print("Por Daniel Mardones")
    print("=" * 60)
    
    success1 = test_streamlit_app()
    success2 = run_quick_test()
    
    print("\n🏆 RESULTADO FINAL")
    print("=" * 60)
    
    if success1 and success2:
        print("🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ La navegación debería funcionar correctamente")
        print("🚀 Puedes ejecutar: streamlit run main_v4_fixed.py")
        print("🌐 URL: http://localhost:8501")
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        print("🔧 Revisa los errores antes de ejecutar")

if __name__ == "__main__":
    main()
