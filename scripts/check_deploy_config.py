#!/usr/bin/env python3
"""
Script para verificar la configuración de deploy
"""
import os
import sys
import django
from pathlib import Path

# Agregar el directorio del proyecto al path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings
from django.db import connection

def check_database_config():
    """Verifica la configuración de la base de datos"""
    print("🔍 Verificando configuración de base de datos...")
    
    try:
        # Verificar que DATABASES esté configurado
        if not hasattr(settings, 'DATABASES'):
            print("❌ DATABASES no está configurado")
            return False
        
        db_config = settings.DATABASES.get('default', {})
        
        print(f"📊 Configuración de base de datos:")
        print(f"   ENGINE: {db_config.get('ENGINE', 'No configurado')}")
        print(f"   NAME: {db_config.get('NAME', 'No configurado')}")
        print(f"   HOST: {db_config.get('HOST', 'No configurado')}")
        print(f"   PORT: {db_config.get('PORT', 'No configurado')}")
        print(f"   USER: {db_config.get('USER', 'No configurado')}")
        
        # Verificar que ENGINE esté configurado
        if not db_config.get('ENGINE'):
            print("❌ ENGINE no está configurado")
            return False
        
        # Intentar conectar a la base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Conexión a base de datos exitosa")
            return True
            
    except Exception as e:
        print(f"❌ Error al verificar base de datos: {e}")
        return False

def check_environment_variables():
    """Verifica las variables de entorno críticas"""
    print("\n🔍 Verificando variables de entorno...")
    
    critical_vars = [
        'DATABASE_URL',
        'SECRET_KEY',
        'DEBUG',
    ]
    
    all_good = True
    for var in critical_vars:
        value = os.environ.get(var)
        if value:
            # Ocultar valores sensibles
            if 'SECRET' in var or 'PASSWORD' in var or 'KEY' in var:
                display_value = f"{value[:10]}..." if len(value) > 10 else "***"
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"⚠️  {var}: No configurada")
            all_good = False
    
    return all_good

def check_django_settings():
    """Verifica configuraciones críticas de Django"""
    print("\n🔍 Verificando configuraciones de Django...")
    
    checks = [
        ('DEBUG', settings.DEBUG),
        ('SECRET_KEY', bool(settings.SECRET_KEY)),
        ('ALLOWED_HOSTS', bool(settings.ALLOWED_HOSTS)),
        ('INSTALLED_APPS', bool(settings.INSTALLED_APPS)),
    ]
    
    all_good = True
    for name, value in checks:
        if value:
            print(f"✅ {name}: Configurado")
        else:
            print(f"❌ {name}: No configurado")
            all_good = False
    
    return all_good

def main():
    """Función principal de verificación"""
    print("🚀 Iniciando verificación de configuración de deploy...")
    print("=" * 60)
    
    checks = [
        ("Variables de Entorno", check_environment_variables),
        ("Configuración de Django", check_django_settings),
        ("Configuración de Base de Datos", check_database_config),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Verificando {name}...")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error durante verificación de {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 Resumen de Verificación:")
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"  {name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las verificaciones pasaron! La configuración está lista para deploy.")
        return 0
    else:
        print("⚠️ Algunas verificaciones fallaron. Revisa los errores arriba.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 