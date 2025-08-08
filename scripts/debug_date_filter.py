#!/usr/bin/env python3
"""
Script para debuggear filtros de fecha.
Ejecutar con: python3 manage.py shell < scripts/debug_date_filter.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.fintech.models import Seller, Credit
from apps.fintech.services.credit_query_service import CreditQueryService
from datetime import datetime, timedelta

User = get_user_model()

print("🔍 Debuggeando filtros de fecha para danielojeda...")

# Obtener usuario
daniel_user = User.objects.get(username='danielojeda')
seller = daniel_user.seller_profile

# Obtener el crédito de daniel
daniel_credit = Credit.objects.filter(seller=seller).first()
if daniel_credit:
    print(f"Crédito de daniel: {daniel_credit.uid}")
    print(f"Fecha de creación: {daniel_credit.created_at}")
    print(f"Fecha de creación (date): {daniel_credit.created_at.date()}")
    
    # Verificar diferentes rangos de fecha
    today = datetime.now().date()
    ranges = [
        (today - timedelta(days=30), today, "Últimos 30 días"),
        (today - timedelta(days=365), today, "Último año"),
        (today - timedelta(days=1000), today, "Últimos 1000 días"),
        (None, None, "Sin filtro de fecha")
    ]
    
    for start_date, end_date, description in ranges:
        if start_date and end_date:
            credits = CreditQueryService.get_user_credits_by_date_range(daniel_user, start_date, end_date)
        else:
            credits = CreditQueryService.get_user_credits(daniel_user)
        
        print(f"\n{description}: {credits.count()} créditos")
        for credit in credits:
            print(f"  - {credit.uid}: {credit.created_at.date()}")

print("✅ Debug completado!") 