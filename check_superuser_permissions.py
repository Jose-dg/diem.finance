#!/usr/bin/env python3
"""
Script para verificar permisos del superusuario
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from apps.fintech.models import User, Credit, Installment
from apps.revenue.models import CreditEarnings

def check_superuser_permissions():
    """Verificar permisos del superusuario"""
    
    print("🔍 VERIFICANDO PERMISOS DEL SUPERUSUARIO")
    print("=" * 50)
    
    # 1. Obtener superusuario
    superuser = User.objects.filter(is_superuser=True).first()
    if not superuser:
        print("❌ No hay superusuario")
        return
    
    print(f"Superusuario: {superuser.username}")
    print(f"is_superuser: {superuser.is_superuser}")
    print(f"is_staff: {superuser.is_staff}")
    
    # 2. Verificar permisos específicos
    modelos_a_verificar = [
        ('Credit', Credit),
        ('Installment', Installment),
        ('CreditEarnings', CreditEarnings),
    ]
    
    print(f"\n📋 Permisos específicos:")
    for nombre, modelo in modelos_a_verificar:
        content_type = ContentType.objects.get_for_model(modelo)
        
        # Verificar permiso de eliminación
        permiso_delete = Permission.objects.filter(
            content_type=content_type,
            codename='delete_' + modelo._meta.model_name
        ).first()
        
        if permiso_delete:
            tiene_permiso = superuser.has_perm(f'fintech.delete_{modelo._meta.model_name}')
            print(f"   - {nombre}: {'✅' if tiene_permiso else '❌'}")
        else:
            print(f"   - {nombre}: ❌ Permiso no existe")
    
    # 3. Verificar todos los permisos del superusuario
    print(f"\n🔑 Todos los permisos del superusuario:")
    permisos_usuario = superuser.user_permissions.all()
    print(f"   - Permisos explícitos: {permisos_usuario.count()}")
    
    for perm in permisos_usuario[:10]:  # Mostrar primeros 10
        print(f"     * {perm.content_type.app_label}.{perm.codename}")
    
    if permisos_usuario.count() > 10:
        print(f"     ... y {permisos_usuario.count() - 10} más")
    
    # 4. Verificar permisos de grupos
    print(f"\n👥 Permisos de grupos:")
    grupos = superuser.groups.all()
    print(f"   - Grupos: {grupos.count()}")
    
    for grupo in grupos:
        permisos_grupo = grupo.permissions.all()
        print(f"     * {grupo.name}: {permisos_grupo.count()} permisos")
    
    # 5. Explicar el problema
    print(f"\n💡 EXPLICACIÓN DEL PROBLEMA:")
    print(f"   - is_superuser=True significa que puede hacer 'cualquier cosa'")
    print(f"   - PERO Django Admin requiere permisos explícitos para eliminación en cascada")
    print(f"   - Cuando eliminas un Credit, Django verifica permisos para cada objeto relacionado")
    print(f"   - Si falta UNO solo, bloquea toda la eliminación")

if __name__ == "__main__":
    check_superuser_permissions()
