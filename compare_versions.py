"""
Script de comparación entre versiones del curso Streamlit
Muestra las diferencias y recomendaciones de uso.
"""

import os
import streamlit

def check_file_exists(filepath):
    """Verifica si un archivo existe."""
    return "✅ Existe" if os.path.exists(filepath) else "❌ No existe"

def get_file_size(filepath):
    """Obtiene el tamaño del archivo."""
    try:
        size = os.path.getsize(filepath)
        return f"{size} bytes"
    except:
        return "N/A"

def analyze_versions():
    """Analiza todas las versiones disponibles."""
    print("🔍 ANÁLISIS COMPARATIVO DE VERSIONES")
    print("=" * 60)
    
    versions = [
        {
            "name": "main.py",
            "description": "Versión original",
            "features": ["Módulos integrados", "Navegación completa"],
            "issues": ["Errores DOM", "Keys duplicados", "Sin contenedores seguros"]
        },
        {
            "name": "main_v3.py", 
            "description": "Arquitectura DOM-safe",
            "features": ["Sin errores DOM", "Keys únicos", "Contenedores seguros", "Sistema de locks"],
            "issues": ["Sin módulos integrados", "Navegación limitada"]
        },
        {
            "name": "main_v4.py",
            "description": "Solución definitiva",
            "features": ["Sin errores DOM", "Módulos integrados", "Navegación completa", "Arquitectura robusta"],
            "issues": ["Ninguno conocido"]
        }
    ]
    
    for version in versions:
        print(f"\n📁 {version['name'].upper()}")
        print("-" * 40)
        print(f"📝 Descripción: {version['description']}")
        print(f"📂 Archivo: {check_file_exists(version['name'])}")
        print(f"📏 Tamaño: {get_file_size(version['name'])}")
        
        print("✅ Características:")
        for feature in version['features']:
            print(f"   • {feature}")
        
        print("⚠️ Problemas:")
        for issue in version['issues']:
            print(f"   • {issue}")

def show_recommendations():
    """Muestra recomendaciones de uso."""
    print("\n🎯 RECOMENDACIONES DE USO")
    print("=" * 60)
    
    scenarios = [
        {
            "scenario": "🚀 Producción / Uso General",
            "recommended": "main_v4.py",
            "reason": "Combina estabilidad DOM con funcionalidad completa"
        },
        {
            "scenario": "🧪 Testing / Debugging",
            "recommended": "main_v3.py", 
            "reason": "Arquitectura DOM-safe pura para pruebas de estabilidad"
        },
        {
            "scenario": "📚 Referencia / Comparación",
            "recommended": "main.py",
            "reason": "Versión original para entender la evolución"
        },
        {
            "scenario": "🎓 Aprendizaje de Streamlit",
            "recommended": "main_v4.py",
            "reason": "Experiencia de usuario óptima para el curso"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{scenario['scenario']}")
        print(f"   ➡️ Recomendado: {scenario['recommended']}")
        print(f"   📋 Razón: {scenario['reason']}")

def show_migration_guide():
    """Muestra guía de migración."""
    print("\n📋 GUÍA DE MIGRACIÓN")
    print("=" * 60)
    
    print("\n🔄 De main.py a main_v4.py:")
    print("   1. ✅ Detener main.py")
    print("   2. ✅ Ejecutar: streamlit run main_v4.py")
    print("   3. ✅ Verificar funcionamiento sin errores DOM")
    print("   4. ✅ Confirmar navegación entre todos los módulos")
    
    print("\n🔄 De main_v3.py a main_v4.py:")
    print("   1. ✅ Detener main_v3.py") 
    print("   2. ✅ Ejecutar: streamlit run main_v4.py")
    print("   3. ✅ Verificar que todos los módulos estén disponibles")
    print("   4. ✅ Confirmar que mantiene estabilidad DOM")

def show_technical_details():
    """Muestra detalles técnicos."""
    print("\n🔧 DETALLES TÉCNICOS")
    print("=" * 60)
    
    print(f"\n📦 Streamlit versión: {streamlit.__version__}")
    print("🎯 Compatibilidad: v1.46.0+")
    
    print("\n🏗️ Arquitectura main_v4.py:")
    print("   • DOMSafeRenderer class")
    print("   • Contenedores aislados con st.empty()")
    print("   • Keys únicos por hashing MD5")
    print("   • Sistema de locks para navegación")
    print("   • Integración dinámica de módulos")
    print("   • Gestión de errores robusta")
    
    print("\n📁 Estructura de módulos:")
    modules = [
        "modulo_01_fundamentos/hello_world.py",
        "modulo_01_fundamentos/widgets_basicos.py", 
        "modulo_01_fundamentos/sidebar_layout.py"
    ]
    
    for module in modules:
        status = check_file_exists(module)
        print(f"   • {module}: {status}")

def main():
    """Función principal."""
    print("🚀 COMPARACIÓN DE VERSIONES - CURSO STREAMLIT")
    print("Por Daniel Mardones")
    print("=" * 60)
    
    analyze_versions()
    show_recommendations()
    show_migration_guide()
    show_technical_details()
    
    print("\n🏆 CONCLUSIÓN")
    print("=" * 60)
    print("✅ USAR main_v4.py para la mejor experiencia")
    print("🚫 Sin errores DOM + Navegación completa")
    print("🎓 Ideal para aprender Streamlit")
    print("⚡ Optimizado para Streamlit 1.46.0")

if __name__ == "__main__":
    main()
