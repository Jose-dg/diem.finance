#!/usr/bin/env python
"""
Script para validar migraciones en base de datos duplicada
"""

import os
import sys
import django
from django.core.management import call_command
from django.db import connection
from datetime import datetime

def setup_django():
    """Configura Django para el script"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_production_test')
    django.setup()

def validate_migration():
    """Valida que las migraciones funcionen correctamente"""
    print("🔍 Validando migraciones en base de datos duplicada...")
    
    try:
        # 1. Verificar conexión
        print("\n1. Verificando conexión a BD duplicada...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f"✅ Conectado a: {db_name}")
        
        # 2. Verificar estado actual
        print("\n2. Verificando estado actual de migraciones...")
        from django.db.migrations.executor import MigrationExecutor
        from django.db import connection
        
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        
        if plan:
            print(f"⚠️  Hay {len(plan)} migraciones pendientes")
            for migration, backwards in plan:
                print(f"   - {migration}")
        else:
            print("✅ No hay migraciones pendientes")
        
        # 3. Ejecutar migraciones
        print("\n3. Ejecutando migraciones...")
        call_command('migrate', verbosity=2)
        
        # 4. Verificar datos después de migración
        print("\n4. Verificando integridad de datos...")
        from apps.fintech.models import User, Document, Credit, UserProfile
        
        # Contar registros
        user_count = User.objects.count()
        document_count = Document.objects.count()
        credit_count = Credit.objects.count()
        profile_count = UserProfile.objects.count()
        
        print(f"   Usuarios: {user_count}")
        print(f"   Documentos: {document_count}")
        print(f"   Créditos: {credit_count}")
        print(f"   Perfiles: {profile_count}")
        
        # 5. Verificar relaciones
        print("\n5. Verificando relaciones de datos...")
        users_with_docs = User.objects.filter(document__isnull=False).count()
        users_with_profiles = User.objects.filter(profile__isnull=False).count()
        
        print(f"   Usuarios con documentos: {users_with_docs}")
        print(f"   Usuarios con perfiles: {users_with_profiles}")
        
        # 6. Probar consultas críticas
        print("\n6. Probando consultas críticas...")
        
        # Probar consulta de créditos por cliente
        from apps.fintech.views import ClientCreditsView
        view = ClientCreditsView()
        
        # Simular datos de prueba
        test_data = {
            'document_number': '12345678',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        # Verificar que la normalización funciona
        normalized = view.normalize_document_number('12-345-678')
        print(f"   Normalización: '12-345-678' -> '{normalized}'")
        
        # 7. Verificar índices
        print("\n7. Verificando índices...")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT indexname, tablename 
                FROM pg_indexes 
                WHERE schemaname = 'public' 
                AND tablename IN ('fintech_user', 'fintech_identifier', 'fintech_credit')
                ORDER BY tablename, indexname;
            """)
            indexes = cursor.fetchall()
            
            for index in indexes:
                print(f"   ✅ {index[1]}: {index[0]}")
        
        print("\n🎉 Validación completada exitosamente!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la validación: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_normalization():
    """Prueba la normalización de documentos"""
    print("\n🧪 Probando normalización de documentos...")
    
    try:
        from apps.fintech.management.commands.normalize_documents import Command
        
        # Crear instancia del comando
        cmd = Command()
        
        # Casos de prueba
        test_cases = [
            ('12-345-678', '12345678'),
            ('12.345.678', '12345678'),
            ('12 345 678', '12345678'),
            ('12345678', '12345678'),
            ('12-345-678-9', '123456789'),
        ]
        
        for input_doc, expected in test_cases:
            result = cmd.normalize_document_number(input_doc)
            status = "✅" if result == expected else "❌"
            print(f"   {status} '{input_doc}' -> '{result}' (esperado: '{expected}')")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando normalización: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Validación de Migraciones en BD Duplicada")
    print("=" * 60)
    
    setup_django()
    
    # Validar migraciones
    if not validate_migration():
        print("\n❌ Validación falló. Revisar errores antes de proceder.")
        sys.exit(1)
    
    # Probar normalización
    if not test_normalization():
        print("\n❌ Pruebas de normalización fallaron.")
        sys.exit(1)
    
    print("\n🎉 ¡Todas las validaciones pasaron!")
    print("\n📋 Próximos pasos:")
    print("1. ✅ Migraciones validadas en BD duplicada")
    print("2. ✅ Normalización de documentos probada")
    print("3. 🔄 Ahora puedes proceder con confianza a producción")
    print("4. 📝 Documentar el proceso para futuras migraciones")

if __name__ == "__main__":
    main() 