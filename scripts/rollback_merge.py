#!/usr/bin/env python
"""
Script de rollback automático para merges fallidos
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"   Comando: {command}")
        print(f"   Error: {e.stderr}")
        return None

def check_git_status():
    """Verifica el estado de git"""
    print("🔍 Verificando estado de Git...")
    
    # Verificar si estamos en main
    branch = run_command("git branch --show-current", "Obteniendo rama actual")
    if not branch or "main" not in branch:
        print("❌ No estás en la rama main")
        return False
    
    # Verificar si hay cambios sin commit
    status = run_command("git status --porcelain", "Verificando cambios pendientes")
    if status and status.strip():
        print("⚠️  Hay cambios sin commit. Haciendo stash...")
        run_command("git stash", "Guardando cambios en stash")
    
    return True

def create_backup():
    """Crea backup de la base de datos"""
    print("💾 Creando backup de la base de datos...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_main_{timestamp}.sql"
    
    # Configuración de BD (ajustar según tu configuración)
    db_name = os.environ.get('DB_NAME', 'fintech_production')
    db_user = os.environ.get('DB_USER', 'postgres')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '5432')
    
    # Crear backup
    backup_cmd = f"pg_dump -h {db_host} -p {db_port} -U {db_user} {db_name} > {backup_file}"
    
    if run_command(backup_cmd, f"Creando backup: {backup_file}"):
        print(f"✅ Backup creado: {backup_file}")
        return backup_file
    else:
        print("❌ No se pudo crear backup")
        return None

def create_git_tag():
    """Crea un tag del estado actual"""
    print("🏷️  Creando tag del estado actual...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tag_name = f"v1.0.0-stable-{timestamp}"
    
    tag_cmd = f'git tag -a {tag_name} -m "Versión estable antes del merge - {timestamp}"'
    
    if run_command(tag_cmd, f"Creando tag: {tag_name}"):
        print(f"✅ Tag creado: {tag_name}")
        return tag_name
    else:
        print("❌ No se pudo crear tag")
        return None

def rollback_merge(merge_commit_hash, backup_file):
    """Hace rollback del merge"""
    print("🔄 Iniciando rollback del merge...")
    
    # 1. Revertir el merge
    revert_cmd = f"git revert -m 1 {merge_commit_hash}"
    if not run_command(revert_cmd, "Revertiendo merge"):
        print("❌ No se pudo revertir el merge")
        return False
    
    # 2. Restaurar base de datos
    if backup_file and os.path.exists(backup_file):
        restore_cmd = f"psql {os.environ.get('DB_NAME', 'fintech_production')} < {backup_file}"
        if not run_command(restore_cmd, "Restaurando base de datos"):
            print("❌ No se pudo restaurar la base de datos")
            return False
    else:
        print("⚠️  No se encontró archivo de backup")
        return False
    
    # 3. Verificar Django
    if not run_command("python manage.py check", "Verificando Django"):
        print("❌ Error en verificación de Django")
        return False
    
    # 4. Verificar migraciones
    if not run_command("python manage.py migrate --plan", "Verificando migraciones"):
        print("❌ Error en verificación de migraciones")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Script de rollback para merges fallidos')
    parser.add_argument('--prepare', action='store_true', help='Preparar para merge (crear backup y tag)')
    parser.add_argument('--rollback', metavar='COMMIT_HASH', help='Hacer rollback del merge especificado')
    parser.add_argument('--backup-file', metavar='FILE', help='Archivo de backup para restaurar')
    
    args = parser.parse_args()
    
    print("🚀 Script de Rollback para Merges")
    print("=" * 50)
    
    if args.prepare:
        print("📋 PREPARANDO PARA MERGE...")
        
        if not check_git_status():
            sys.exit(1)
        
        backup_file = create_backup()
        if not backup_file:
            sys.exit(1)
        
        tag_name = create_git_tag()
        if not tag_name:
            sys.exit(1)
        
        print("\n🎉 Preparación completada!")
        print(f"📁 Backup: {backup_file}")
        print(f"🏷️  Tag: {tag_name}")
        print("\n📋 Ahora puedes hacer el merge con seguridad")
        
    elif args.rollback:
        print("🔄 HACIENDO ROLLBACK...")
        
        if not args.backup_file:
            print("❌ Debes especificar el archivo de backup con --backup-file")
            sys.exit(1)
        
        if not os.path.exists(args.backup_file):
            print(f"❌ No se encontró el archivo de backup: {args.backup_file}")
            sys.exit(1)
        
        if not check_git_status():
            sys.exit(1)
        
        if rollback_merge(args.rollback, args.backup_file):
            print("\n🎉 Rollback completado exitosamente!")
            print("✅ Código y base de datos restaurados")
        else:
            print("\n❌ Rollback falló")
            sys.exit(1)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 