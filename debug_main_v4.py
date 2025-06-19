"""
Script de debug para main_v4.py
Verifica problemas de importación y navegación.
"""

import sys
import os

# Agregar el directorio de módulos al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modulo_01_fundamentos'))

def test_imports():
    """Prueba las importaciones paso a paso."""
    print("🔍 DEBUGGING IMPORTACIONES")
    print("=" * 40)
    
    # 1. Verificar path
    module_path = os.path.join(os.path.dirname(__file__), 'modulo_01_fundamentos')
    print(f"📁 Path de módulos: {module_path}")
    print(f"📂 Existe: {os.path.exists(module_path)}")
    
    # 2. Listar archivos en el directorio
    if os.path.exists(module_path):
        files = os.listdir(module_path)
        print(f"📋 Archivos encontrados: {files}")
    
    # 3. Verificar sys.path
    print(f"🛤️ Module path en sys.path: {module_path in sys.path}")
    
    # 4. Intentar importaciones
    modules_to_test = ['hello_world', 'widgets_basicos', 'sidebar_layout']
    
    for module_name in modules_to_test:
        try:
            module = __import__(module_name)
            print(f"✅ {module_name}: IMPORTADO")
            
            # Verificar función run
            if hasattr(module, 'run'):
                print(f"   • Función run(): ✅ EXISTE")
            else:
                print(f"   • Función run(): ❌ NO EXISTE")
                
        except ImportError as e:
            print(f"❌ {module_name}: ERROR - {e}")
    
    return True

def test_streamlit_imports():
    """Prueba las importaciones de Streamlit."""
    print("\n🔍 DEBUGGING STREAMLIT")
    print("=" * 40)
    
    try:
        import streamlit as st
        print(f"✅ Streamlit versión: {st.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Error importando Streamlit: {e}")
        return False

def test_main_v4_structure():
    """Analiza la estructura de main_v4.py."""
    print("\n🔍 DEBUGGING MAIN_V4.PY")
    print("=" * 40)
    
    try:
        with open('main_v4.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar patrones problemáticos
        issues = []
        
        # 1. Verificar imports
        if 'import hello_world' not in content:
            issues.append("Falta import hello_world")
        if 'import widgets_basicos' not in content:
            issues.append("Falta import widgets_basicos")
        if 'import sidebar_layout' not in content:
            issues.append("Falta import sidebar_layout")
        
        # 2. Verificar función render_content_v4
        if 'def render_content_v4' not in content:
            issues.append("Falta función render_content_v4")
        
        # 3. Verificar mapeo de clases
        if 'class_mapping' not in content:
            issues.append("Falta class_mapping")
        
        # 4. Verificar llamada a módulos
        if 'current_module.run()' not in content:
            issues.append("Falta llamada current_module.run()")
        
        if issues:
            print("⚠️ Problemas encontrados:")
            for issue in issues:
                print(f"   • {issue}")
        else:
            print("✅ Estructura parece correcta")
        
        return len(issues) == 0
        
    except Exception as e:
        print(f"❌ Error leyendo main_v4.py: {e}")
        return False

def simulate_navigation():
    """Simula el proceso de navegación."""
    print("\n🔍 SIMULANDO NAVEGACIÓN")
    print("=" * 40)
    
    # Simular estado de navegación
    nav_state = {
        'current_module': 'Módulo 1: Fundamentos',
        'current_class': 'Clase 1: Hello, Streamlit',
        'render_lock': False
    }
    
    print(f"📍 Módulo actual: {nav_state['current_module']}")
    print(f"📍 Clase actual: {nav_state['current_class']}")
    
    # Simular mapeo
    try:
        import hello_world
        import widgets_basicos
        import sidebar_layout
        
        class_mapping = {
            "Clase 1: Hello, Streamlit": {
                "container": "hello_world_main",
                "module": hello_world
            },
            "Clase 2: Widgets básicos": {
                "container": "widgets_main", 
                "module": widgets_basicos
            },
            "Clase 3: Sidebar y layout": {
                "container": "sidebar_main",
                "module": sidebar_layout
            }
        }
        
        current_class = nav_state['current_class']
        if current_class in class_mapping:
            current_module = class_mapping[current_class]["module"]
            print(f"✅ Módulo mapeado: {current_module.__name__}")
            print(f"✅ Función run disponible: {hasattr(current_module, 'run')}")
        else:
            print(f"❌ Clase no encontrada en mapeo: {current_class}")
            
    except ImportError as e:
        print(f"❌ Error en simulación: {e}")

def main():
    """Ejecuta todos los tests de debug."""
    print("🚀 DEBUG COMPLETO - MAIN_V4.PY")
    print("Por Daniel Mardones")
    print("=" * 50)
    
    results = []
    
    # Ejecutar tests
    results.append(("Importaciones de módulos", test_imports()))
    results.append(("Importaciones de Streamlit", test_streamlit_imports()))
    results.append(("Estructura de main_v4", test_main_v4_structure()))
    
    # Simular navegación
    simulate_navigation()
    
    print("\n🎯 RESUMEN DE RESULTADOS")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASADO" if result else "❌ FALLIDO"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 TODOS LOS TESTS PASARON")
        print("El problema podría estar en la lógica de renderizado de Streamlit")
    else:
        print("\n⚠️ SE ENCONTRARON PROBLEMAS")
        print("Revisa los errores arriba para identificar la causa")

if __name__ == "__main__":
    main()
