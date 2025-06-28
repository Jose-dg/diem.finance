#!/usr/bin/env python
"""
Script de seguridad para migraciones en producción
Verifica que las migraciones sean seguras antes de ejecutarlas
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection
from django.apps import apps

def setup_django():
    """Configura Django para el script"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()

def check_migration_safety():
    """Verifica que las migraciones sean seguras"""
    print("🔍 Verificando seguridad de migraciones...")
    
    # 1. Verificar que no hay migraciones pendientes
    print("\n1. Verificando migraciones pendientes...")
    try:
        from django.core.management import call_command
        from io import StringIO
        
        out = StringIO()
        call_command('showmigrations', stdout=out)
        migrations_output = out.getvalue()
        
        # Buscar migraciones no aplicadas
        if '[ ]' in migrations_output:
            print("⚠️  ADVERTENCIA: Hay migraciones pendientes!")
            print("   Ejecuta: python manage.py migrate")
            return False
        else:
            print("✅ Todas las migraciones están aplicadas")
    except Exception as e:
        print(f"❌ Error verificando migraciones: {e}")
        return False
    
    # 2. Verificar integridad de la base de datos
    print("\n2. Verificando integridad de la base de datos...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Conexión a base de datos OK")
    except Exception as e:
        print(f"❌ Error de conexión a BD: {e}")
        return False
    
    # 3. Verificar que los modelos están sincronizados
    print("\n3. Verificando sincronización de modelos...")
    try:
        call_command('check', verbosity=0)
        print("✅ Modelos sincronizados correctamente")
    except Exception as e:
        print(f"❌ Error en modelos: {e}")
        return False
    
    # 4. Verificar datos críticos
    print("\n4. Verificando datos críticos...")
    try:
        from apps.fintech.models import User, Document, Credit
        
        user_count = User.objects.count()
        document_count = Document.objects.count()
        credit_count = Credit.objects.count()
        
        print(f"   Usuarios: {user_count}")
        print(f"   Documentos: {document_count}")
        print(f"   Créditos: {credit_count}")
        
        if user_count > 0 and document_count == 0:
            print("⚠️  ADVERTENCIA: Hay usuarios sin documentos!")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando datos: {e}")
        return False
    
    print("\n✅ Todas las verificaciones pasaron exitosamente!")
    return True

def backup_database():
    """Crea un backup de la base de datos"""
    print("\n💾 Creando backup de la base de datos...")
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_{timestamp}.sql"
    
    try:
        # Obtener configuración de BD
        from django.conf import settings
        db_settings = settings.DATABASES['default']
        
        if db_settings['ENGINE'] == 'django.db.backends.postgresql':
            # PostgreSQL
            import subprocess
            cmd = [
                'pg_dump',
                '-h', db_settings.get('HOST', 'localhost'),
                '-p', str(db_settings.get('PORT', 5432)),
                '-U', db_settings['USER'],
                '-d', db_settings['NAME'],
                '-f', backup_file
            ]
            
            # Configurar password si es necesario
            env = os.environ.copy()
            if 'PASSWORD' in db_settings:
                env['PGPASSWORD'] = db_settings['PASSWORD']
            
            subprocess.run(cmd, env=env, check=True)
            print(f"✅ Backup creado: {backup_file}")
            
        else:
            print("⚠️  Backup automático no soportado para este tipo de BD")
            print("   Crea un backup manual antes de continuar")
            
    except Exception as e:
        print(f"❌ Error creando backup: {e}")
        return False
    
    return True

def main():
    """Función principal"""
    print("🚀 Script de Seguridad para Migraciones")
    print("=" * 50)
    
    setup_django()
    
    # Verificar seguridad
    if not check_migration_safety():
        print("\n❌ Verificaciones fallaron. NO proceder con migraciones.")
        sys.exit(1)
    
    # Crear backup
    if not backup_database():
        print("\n❌ No se pudo crear backup. NO proceder con migraciones.")
        sys.exit(1)
    
    print("\n🎉 Todo listo para migraciones seguras!")
    print("\n📋 Próximos pasos:")
    print("1. Ejecutar: python manage.py migrate")
    print("2. Ejecutar: python manage.py normalize_documents --dry-run")
    print("3. Si todo está bien: python manage.py normalize_documents")
    print("4. Verificar: python manage.py check")

if __name__ == "__main__":
    main() 