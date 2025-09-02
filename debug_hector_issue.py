#!/usr/bin/env python3
"""
Script de test para simular exactamente lo que está pasando en CreditsAPIView
con el usuario HectorAA
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.fintech.models import User, Seller, Credit
from apps.fintech.services.credit.credit_query_service import CreditQueryService
from django.db import connection

def test_hector_credits_view():
    """Test que simula exactamente lo que hace CreditsAPIView"""
    print("🧪 TESTEANDO CREDITSAPIVIEW CON HECTORAA")
    print("=" * 60)
    
    # 1. Obtener el usuario HectorAA
    try:
        user = User.objects.get(username='NovioSelene')  # Username real
        print(f"✅ Usuario encontrado: {user.username}")
        print(f"   ID: {user.id}")
        print(f"   is_superuser: {user.is_superuser}")
        print(f"   is_staff: {user.is_staff}")
        print(f"   is_active: {user.is_active}")
        
        # 2. Verificar si tiene seller_profile
        if hasattr(user, 'seller_profile'):
            seller_profile = user.seller_profile
            print(f"✅ Tiene seller_profile: {seller_profile}")
            print(f"   Seller ID: {seller_profile.id}")
            print(f"   Role: {seller_profile.role}")
            
            # 3. Verificar créditos vendidos por este seller
            credits_vendidos = Credit.objects.filter(seller=seller_profile)
            print(f"   Créditos vendidos por este seller: {credits_vendidos.count()}")
            
            if credits_vendidos.exists():
                print("   Lista de créditos vendidos:")
                for credit in credits_vendidos[:5]:
                    print(f"     - ID: {credit.id}, Cliente: {credit.user.username}, Monto: {credit.price}")
            else:
                print("   ❌ NO HAY CRÉDITOS VENDIDOS POR ESTE SELLER")
                
        else:
            print("❌ NO tiene seller_profile")
        
        # 4. SIMULAR EXACTAMENTE LO QUE HACE CREDITSAPIVIEW
        print(f"\n🔍 SIMULANDO CREDITSAPIVIEW")
        print("-" * 40)
        
        # Simular el método GET sin filtros de fecha
        print("📋 Método GET (sin filtros de fecha):")
        base_qs = CreditQueryService.get_user_credits(user).order_by('-created_at')
        print(f"   Créditos retornados por CreditQueryService: {base_qs.count()}")
        
        if base_qs.exists():
            print("   ✅ CreditQueryService retornó créditos")
            print("   Primeros 3 créditos:")
            for credit in base_qs[:3]:
                seller_info = f"Seller: {credit.seller.user.username if credit.seller else 'SIN SELLER'}"
                print(f"     - ID: {credit.id}, Cliente: {credit.user.username}, {seller_info}")
        else:
            print("   ❌ CreditQueryService NO retornó créditos")
            
            # Verificar qué está pasando
            print(f"\n🔍 INVESTIGANDO POR QUÉ NO RETORNA CRÉDITOS")
            print("-" * 40)
            
            # Verificar la consulta manual
            manual_query = Credit.objects.filter(seller__user=user)
            print(f"   Consulta manual seller__user=user: {manual_query.count()}")
            
            # Verificar si hay algún problema con la relación
            print(f"   Verificando relación seller__user:")
            print(f"     - user.id: {user.id}")
            print(f"     - seller_profile.id: {seller_profile.id if hasattr(user, 'seller_profile') else 'N/A'}")
            
            # Verificar si hay créditos con seller null que podrían estar causando el problema
            credits_sin_seller = Credit.objects.filter(seller__isnull=True)
            print(f"   Créditos sin seller: {credits_sin_seller.count()}")
            
            if credits_sin_seller.exists():
                print("   Primeros 3 créditos sin seller:")
                for credit in credits_sin_seller[:3]:
                    print(f"     - ID: {credit.id}, Cliente: {credit.user.username}, Estado: {credit.state}")
        
        # 5. VERIFICAR SI HAY ALGÚN FALLBACK EN LA VISTA
        print(f"\n🔍 VERIFICANDO POSIBLES FALLBACKS")
        print("-" * 40)
        
        # Verificar si el usuario es staff o superuser
        if user.is_superuser:
            print("   ⚠️  Usuario es SUPERUSER - debería ver TODO")
        elif user.is_staff:
            print("   ⚠️  Usuario es STAFF - debería ver TODO")
        else:
            print("   ✅ Usuario NO es staff ni superuser")
        
        # Verificar si hay algún problema con el filtro
        print(f"\n🔍 VERIFICANDO FILTRO SELLER__USER")
        print("-" * 40)
        
        # Probar diferentes variaciones del filtro
        filters_to_test = [
            ('seller__user', user),
            ('seller__user__id', user.id),
            ('seller', seller_profile if hasattr(user, 'seller_profile') else None),
        ]
        
        for filter_name, filter_value in filters_to_test:
            if filter_value is not None:
                try:
                    test_qs = Credit.objects.filter(**{filter_name: filter_value})
                    print(f"   Filtro {filter_name}={filter_value}: {test_qs.count()} créditos")
                except Exception as e:
                    print(f"   ❌ Error con filtro {filter_name}={filter_value}: {e}")
            else:
                print(f"   ⚠️  Filtro {filter_name}: valor None")
        
    except User.DoesNotExist:
        print("❌ Usuario NovioSelene no encontrado")
    except Exception as e:
        print(f"❌ Error durante el test: {str(e)}")
        import traceback
        traceback.print_exc()

def test_credit_query_service_edge_cases():
    """Test de casos edge del CreditQueryService"""
    print(f"\n🧪 TESTEANDO CASOS EDGE DEL CREDITQUERYSERVICE")
    print("=" * 60)
    
    # Buscar usuarios con diferentes roles
    users_to_test = []
    
    # Superuser
    try:
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            users_to_test.append(('SUPERUSER', superuser))
    except:
        pass
    
    # Staff sin seller_profile
    try:
        staff_user = User.objects.filter(is_staff=True, seller_profile__isnull=True).first()
        if staff_user:
            users_to_test.append(('STAFF SIN SELLER', staff_user))
    except:
        pass
    
    # Vendedor con créditos
    try:
        seller_with_credits = User.objects.filter(seller_profile__isnull=False).first()
        if seller_with_credits:
            users_to_test.append(('VENDEDOR CON CRÉDITOS', seller_with_credits))
    except:
        pass
    
    # Cliente normal
    try:
        normal_client = User.objects.filter(
            is_superuser=False, 
            is_staff=False, 
            seller_profile__isnull=True
        ).first()
        if normal_client:
            users_to_test.append(('CLIENTE NORMAL', normal_client))
    except:
        pass
    
    # Testear cada tipo de usuario
    for user_type, user in users_to_test:
        print(f"\n🔍 Testeando {user_type}: {user.username}")
        print("-" * 40)
        
        try:
            credits = CreditQueryService.get_user_credits(user)
            print(f"   Créditos retornados: {credits.count()}")
            
            if credits.exists():
                print("   Primer crédito:")
                first_credit = credits.first()
                seller_info = f"Seller: {first_credit.seller.user.username if first_credit.seller else 'SIN SELLER'}"
                print(f"     - ID: {first_credit.id}, Cliente: {first_credit.user.username}, {seller_info}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_hector_aa_authentication():
    """Test específico para el problema de autenticación de HectorAA"""
    print(f"\n🧪 TESTEANDO AUTENTICACIÓN DE HECTORAA")
    print("=" * 60)
    
    # Verificar la inconsistencia en la base de datos
    print("🔍 VERIFICANDO INCONSISTENCIA EN BASE DE DATOS")
    print("-" * 40)
    
    with connection.cursor() as cursor:
        # Verificar la tabla Seller
        cursor.execute("""
            SELECT s.id, s.user_id, u.username, u.id as user_table_id
            FROM fintech_seller s 
            JOIN fintech_user u ON s.user_id = u.id 
            WHERE s.id = 2
        """)
        
        seller_data = cursor.fetchone()
        if seller_data:
            seller_id, user_id, username, user_table_id = seller_data
            print(f"✅ Seller encontrado:")
            print(f"   - Seller ID: {seller_id}")
            print(f"   - User ID en Seller: {user_id}")
            print(f"   - Username en User: {username}")
            print(f"   - User ID en User table: {user_table_id}")
            
            if user_id != user_table_id:
                print(f"   ❌ INCONSISTENCIA: User ID en Seller ({user_id}) != User ID en User table ({user_table_id})")
            else:
                print(f"   ✅ IDs coinciden")
        
        # Verificar si hay algún problema con la autenticación
        print(f"\n🔍 VERIFICANDO AUTENTICACIÓN")
        print("-" * 40)
        
        # Simular login con username "HectorAA"
        try:
            # Buscar por username en Seller
            seller_by_username = Seller.objects.filter(user__username='HectorAA').first()
            if seller_by_username:
                print(f"✅ Seller encontrado por username 'HectorAA': {seller_by_username}")
                print(f"   - Seller ID: {seller_by_username.id}")
                print(f"   - User ID: {seller_by_username.user.id}")
                print(f"   - Username real: {seller_by_username.user.username}")
                
                # Verificar si este seller tiene créditos
                credits_count = Credit.objects.filter(seller=seller_by_username).count()
                print(f"   - Créditos vendidos: {credits_count}")
                
                # Simular CreditQueryService con este seller
                print(f"\n🧪 SIMULANDO CREDITQUERYSERVICE CON SELLER HECTORAA")
                print("-" * 40)
                
                # Crear un usuario mock para simular la autenticación
                class MockUser:
                    def __init__(self, username, is_superuser=False, is_staff=False):
                        self.username = username
                        self.is_superuser = is_superuser
                        self.is_staff = is_staff
                        self.seller_profile = seller_by_username
                
                mock_user = MockUser('HectorAA')
                print(f"   Usuario mock creado: {mock_user.username}")
                print(f"   Tiene seller_profile: {hasattr(mock_user, 'seller_profile')}")
                
                # Probar el servicio
                try:
                    credits = CreditQueryService.get_user_credits(mock_user)
                    print(f"   Créditos retornados por CreditQueryService: {credits.count()}")
                    
                    if credits.exists():
                        print("   ✅ CreditQueryService retornó créditos")
                        print("   Primeros 3 créditos:")
                        for credit in credits[:3]:
                            seller_info = f"Seller: {credit.seller.user.username if credit.seller else 'SIN SELLER'}"
                            print(f"     - ID: {credit.id}, Cliente: {credit.user.username}, {seller_info}")
                    else:
                        print("   ❌ CreditQueryService NO retornó créditos")
                        
                except Exception as e:
                    print(f"   ❌ Error en CreditQueryService: {e}")
                
            else:
                print("❌ No se encontró seller con username 'HectorAA'")
                
        except Exception as e:
            print(f"❌ Error durante la verificación: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_hector_credits_view()
    test_credit_query_service_edge_cases()
    test_hector_aa_authentication()
