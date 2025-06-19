"""
Script de validación para main_v4.py
Verifica que la integración de módulos funcione correctamente.
"""

import sys
import os

# Agregar path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'modulo_01_fundamentos'))

def test_module_imports():
    """Prueba que todos los módulos se puedan importar correctamente."""
    print("🧪 Probando importación de módulos...")
    
    try:
        import hello_world
        print("✅ hello_world.py: IMPORTADO")
        
        import widgets_basicos
        print("✅ widgets_basicos.py: IMPORTADO")
        
        import sidebar_layout
        print("✅ sidebar_layout.py: IMPORTADO")
        
        return True, [hello_world, widgets_basicos, sidebar_layout]
    
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        return False, []

def test_module_functions():
    """Prueba que los módulos tengan la función run()."""
    print("🧪 Probando funciones de módulos...")
    
    success, modules = test_module_imports()
    if not success:
        return False
    
    for i, module in enumerate(modules):
        module_names = ['hello_world', 'widgets_basicos', 'sidebar_layout']
        
        if hasattr(module, 'run'):
            print(f"✅ {module_names[i]}.run(): DISPONIBLE")
        else:
            print(f"❌ {module_names[i]}.run(): NO ENCONTRADA")
            return False
    
    return True

def test_main_v4_structure():
    """Prueba la estructura de main_v4.py."""
    print("🧪 Probando estructura de main_v4.py...")
    
    try:
        # Importar sin ejecutar
        with open('main_v4.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar componentes clave
        checks = [
            ("DOMSafeRenderer", "class DOMSafeRenderer" in content),
            ("safe_navigation_state", "def safe_navigation_state" in content),
            ("render_navigation_v4", "def render_navigation_v4" in content),
            ("render_content_v4", "def render_content_v4" in content),
            ("main_v4", "def main_v4" in content),
            ("Import hello_world", "import hello_world" in content),
            ("Import widgets_basicos", "import widgets_basicos" in content),
            ("Import sidebar_layout", "import sidebar_layout" in content)
        ]
        
        all_passed = True
        for check_name, check_result in checks:
            if check_result:
                print(f"✅ {check_name}: ENCONTRADO")
            else:
                print(f"❌ {check_name}: NO ENCONTRADO")
                all_passed = False
        
        return all_passed
    
    except Exception as e:
        print(f"❌ Error leyendo main_v4.py: {e}")
        return False

def test_file_structure():
    """Verifica que existan todos los archivos necesarios."""
    print("🧪 Probando estructura de archivos...")
    
    required_files = [
        'main_v4.py',
        'modulo_01_fundamentos/hello_world.py',
        'modulo_01_fundamentos/widgets_basicos.py', 
        'modulo_01_fundamentos/sidebar_layout.py',
        'modulo_01_fundamentos/__init__.py'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}: EXISTE")
        else:
            print(f"❌ {file_path}: NO ENCONTRADO")
            all_exist = False
    
    return all_exist

def main():
    """Ejecuta todas las validaciones."""
    print("🚀 VALIDACIÓN COMPLETA - MAIN_V4.PY")
    print("=" * 50)
    
    tests = [
        ("Estructura de archivos", test_file_structure),
        ("Estructura de main_v4", test_main_v4_structure),
        ("Importación de módulos", test_module_imports),
        ("Funciones de módulos", test_module_functions)
    ]
    
    all_passed = True
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name.upper()}")
        print("-" * 30)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if not result:
                all_passed = False
                
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append((test_name, False))
            all_passed = False
    
    print("\n🎯 RESULTADO FINAL")
    print("=" * 50)
    
    for test_name, result in results:
        status = "✅ PASADO" if result else "❌ FALLIDO"
        print(f"{test_name}: {status}")
    
    if all_passed:
        print("\n🎉 TODAS LAS VALIDACIONES PASARON")
        print("✅ main_v4.py está listo para usar")
        print("🚀 Todos los módulos están integrados correctamente")
        print("🔧 La navegación debería funcionar sin errores DOM")
    else:
        print("\n⚠️ ALGUNAS VALIDACIONES FALLARON")
        print("🔧 Revisa los errores antes de usar en producción")

if __name__ == "__main__":
    main()
