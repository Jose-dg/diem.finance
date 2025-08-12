from django.db.models import Q, Count, Sum, Avg, Max, Min
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from datetime import datetime, date
from decimal import Decimal
from apps.fintech.models import Credit, User, AccountMethodAmount, Transaction
import logging

logger = logging.getLogger(__name__)

class CreditAnalysisService:
    """Servicio para análisis detallado de créditos con tabla de detalles"""
    
    @staticmethod
    def get_credit_analysis_summary(start_date, end_date):
        """
        Obtiene resumen general del análisis de créditos
        """
        try:
            creditos_periodo = Credit.objects.filter(
                created_at__date__range=[start_date, end_date]
            )
            
            total_creditos = creditos_periodo.count()
            total_solicitado = creditos_periodo.aggregate(total=Sum('price'))['total'] or Decimal('0.00')
            total_abonado = creditos_periodo.aggregate(total=Sum('total_abonos'))['total'] or Decimal('0.00')
            total_pendiente = creditos_periodo.aggregate(total=Sum('pending_amount'))['total'] or Decimal('0.00')
            
            # Clientes únicos
            clientes_unicos = creditos_periodo.values('user__username').distinct().count()
            
            # Clientes sin abonos
            clientes_sin_abonos = creditos_periodo.filter(
                total_abonos=0.00
            ).values('user__username').distinct().count()
            
            # Clientes con créditos atrasados
            clientes_atrasados = creditos_periodo.filter(
                Q(is_in_default=True) | 
                Q(morosidad_level__in=['mild_default', 'moderate_default', 'severe_default', 'recurrent_default', 'critical_default'])
            ).values('user__username').distinct().count()
            
            # Porcentaje de pago
            porcentaje_pago = (total_abonado / total_solicitado * 100) if total_solicitado > 0 else 0
            
            return {
                'period': {
                    'start_date': start_date,
                    'end_date': end_date
                },
                'summary': {
                    'total_credits': total_creditos,
                    'total_requested': float(total_solicitado),
                    'total_paid': float(total_abonado),
                    'total_pending': float(total_pendiente),
                    'unique_clients': clientes_unicos,
                    'clients_without_payments': clientes_sin_abonos,
                    'clients_in_default': clientes_atrasados,
                    'payment_percentage': round(porcentaje_pago, 2)
                }
            }
        except Exception as e:
            logger.error(f"Error getting credit analysis summary: {e}")
            return {}
    
    @staticmethod
    def get_detailed_clients_table(start_date, end_date, limit=None):
        """
        Obtiene tabla detallada de clientes con información completa
        """
        try:
            creditos_periodo = Credit.objects.filter(
                created_at__date__range=[start_date, end_date]
            ).select_related('user', 'subcategory', 'currency')
            
            # Agrupar por cliente con información detallada
            clientes_detalle = creditos_periodo.values(
                'user__id',
                'user__username',
                'user__first_name',
                'user__last_name',
                'user__email'
            ).annotate(
                total_credits=Count('id'),
                credits_without_payment=Count('id', filter=Q(total_abonos=0.00)),
                credits_in_default=Count('id', filter=Q(is_in_default=True)),
                total_requested=Sum('price'),
                total_paid=Sum('total_abonos'),
                total_pending=Sum('pending_amount'),
                first_credit_date=Min('created_at'),
                last_credit_date=Max('created_at'),
                avg_credit_amount=Avg('price'),
                max_credit_amount=Max('price'),
                min_credit_amount=Min('price')
            ).order_by('-total_requested')
            
            # Aplicar límite si se especifica
            if limit:
                clientes_detalle = clientes_detalle[:limit]
            
            # Procesar cada cliente para agregar información adicional
            clientes_procesados = []
            for cliente in clientes_detalle:
                # Calcular porcentaje de pago
                porcentaje_pago = 0
                if cliente['total_requested'] and cliente['total_requested'] > 0:
                    porcentaje_pago = (cliente['total_paid'] / cliente['total_requested']) * 100
                
                # Obtener nombre completo
                nombre_completo = f"{cliente['user__first_name']} {cliente['user__last_name']}".strip()
                if not nombre_completo:
                    nombre_completo = cliente['user__username']
                
                # Obtener créditos específicos del cliente
                creditos_cliente = creditos_periodo.filter(user_id=cliente['user__id'])
                
                # Información de morosidad
                creditos_morosos = creditos_cliente.filter(
                    Q(is_in_default=True) | 
                    Q(morosidad_level__in=['mild_default', 'moderate_default', 'severe_default', 'recurrent_default', 'critical_default'])
                )
                
                # Días promedio de mora
                dias_mora_promedio = 0
                if creditos_morosos.exists():
                    hoy = timezone.now().date()
                    total_dias_mora = 0
                    creditos_con_mora = 0
                    
                    for credito in creditos_morosos:
                        if credito.first_date_payment:
                            dias_mora = (hoy - credito.first_date_payment).days
                            if dias_mora > 0:
                                total_dias_mora += dias_mora
                                creditos_con_mora += 1
                    
                    if creditos_con_mora > 0:
                        dias_mora_promedio = total_dias_mora / creditos_con_mora
                
                # Información de pagos
                pagos_cliente = AccountMethodAmount.objects.filter(
                    credit__user_id=cliente['user__id'],
                    credit__created_at__date__range=[start_date, end_date],
                    transaction__transaction_type='income',
                    transaction__status='confirmed'
                )
                
                total_pagos_realizados = pagos_cliente.count()
                monto_total_pagado = pagos_cliente.aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
                
                # Promedio por pago
                promedio_por_pago = 0
                if total_pagos_realizados > 0:
                    promedio_por_pago = float(monto_total_pagado / total_pagos_realizados)
                
                cliente_procesado = {
                    'client_id': cliente['user__id'],
                    'username': cliente['user__username'],
                    'full_name': nombre_completo,
                    'email': cliente['user__email'],
                    'total_credits': cliente['total_credits'],
                    'credits_without_payment': cliente['credits_without_payment'],
                    'credits_in_default': cliente['credits_in_default'],
                    'total_requested': float(cliente['total_requested']),
                    'total_paid': float(cliente['total_paid']),
                    'total_pending': float(cliente['total_pending']),
                    'payment_percentage': round(porcentaje_pago, 2),
                    'avg_credit_amount': float(cliente['avg_credit_amount']),
                    'max_credit_amount': float(cliente['max_credit_amount']),
                    'min_credit_amount': float(cliente['min_credit_amount']),
                    'first_credit_date': cliente['first_credit_date'],
                    'last_credit_date': cliente['last_credit_date'],
                    'total_payments_made': total_pagos_realizados,
                    'total_amount_paid': float(monto_total_pagado),
                    'avg_payment_amount': promedio_por_pago,
                    'avg_days_overdue': round(dias_mora_promedio, 1),
                    'risk_level': CreditAnalysisService._calculate_risk_level(
                        cliente['credits_in_default'], 
                        porcentaje_pago, 
                        dias_mora_promedio
                    )
                }
                
                clientes_procesados.append(cliente_procesado)
            
            return clientes_procesados
            
        except Exception as e:
            logger.error(f"Error getting detailed clients table: {e}")
            return []
    
    @staticmethod
    def _calculate_risk_level(credits_in_default, payment_percentage, avg_days_overdue):
        """
        Calcula el nivel de riesgo del cliente
        """
        risk_score = 0
        
        # Factor por créditos en mora
        if credits_in_default > 0:
            risk_score += credits_in_default * 20
        
        # Factor por porcentaje de pago
        if payment_percentage < 50:
            risk_score += 30
        elif payment_percentage < 75:
            risk_score += 15
        elif payment_percentage < 90:
            risk_score += 5
        
        # Factor por días de mora promedio
        if avg_days_overdue > 30:
            risk_score += 25
        elif avg_days_overdue > 15:
            risk_score += 15
        elif avg_days_overdue > 7:
            risk_score += 5
        
        # Clasificar nivel de riesgo
        if risk_score >= 50:
            return 'HIGH'
        elif risk_score >= 25:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    @staticmethod
    def get_payment_analysis(start_date, end_date):
        """
        Análisis detallado de pagos
        """
        try:
            # Pagos realizados en el período
            pagos_creditos = AccountMethodAmount.objects.filter(
                credit__created_at__date__range=[start_date, end_date],
                transaction__transaction_type='income',
                transaction__status='confirmed'
            )
            
            total_pagos = pagos_creditos.count()
            total_monto_pagado = pagos_creditos.aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
            
            # Análisis por mes
            pagos_por_mes = pagos_creditos.extra(
                select={'mes': "EXTRACT(month FROM fintech_transaction.date)"}
            ).values('mes').annotate(
                count=Count('id'),
                total_pagado=Sum('amount_paid'),
                promedio_pago=Avg('amount_paid')
            ).order_by('mes')
            
            # Top clientes con más pagos
            top_clientes_pagos = pagos_creditos.values(
                'credit__user__username',
                'credit__user__first_name',
                'credit__user__last_name'
            ).annotate(
                pagos_count=Count('id'),
                total_pagado=Sum('amount_paid'),
                promedio_pago=Avg('amount_paid')
            ).order_by('-total_pagado')[:10]
            
            return {
                'payment_summary': {
                    'total_payments': total_pagos,
                    'total_amount_paid': float(total_monto_pagado),
                    'avg_payment_amount': float(total_monto_pagado / total_pagos) if total_pagos > 0 else 0
                },
                'payments_by_month': list(pagos_por_mes),
                'top_paying_clients': list(top_clientes_pagos)
            }
            
        except Exception as e:
            logger.error(f"Error getting payment analysis: {e}")
            return {}
    
    @staticmethod
    def get_default_analysis(start_date, end_date):
        """
        Análisis de morosidad y créditos en default
        """
        try:
            creditos_periodo = Credit.objects.filter(
                created_at__date__range=[start_date, end_date]
            )
            
            # Créditos en mora
            creditos_morosos = creditos_periodo.filter(
                Q(is_in_default=True) | 
                Q(morosidad_level__in=['mild_default', 'moderate_default', 'severe_default', 'recurrent_default', 'critical_default'])
            )
            
            total_morosos = creditos_morosos.count()
            monto_moroso = creditos_morosos.aggregate(total=Sum('pending_amount'))['total'] or Decimal('0.00')
            
            # Análisis por nivel de morosidad
            morosidad_por_nivel = creditos_morosos.values('morosidad_level').annotate(
                count=Count('id'),
                total_amount=Sum('pending_amount'),
                avg_amount=Avg('pending_amount')
            ).order_by('morosidad_level')
            
            # Clientes con mayor morosidad
            clientes_morosos = creditos_morosos.values(
                'user__username',
                'user__first_name',
                'user__last_name'
            ).annotate(
                creditos_morosos=Count('id'),
                total_moroso=Sum('pending_amount'),
                avg_moroso=Avg('pending_amount')
            ).order_by('-total_moroso')[:10]
            
            return {
                'default_summary': {
                    'total_defaulted_credits': total_morosos,
                    'total_defaulted_amount': float(monto_moroso),
                    'default_rate': (total_morosos * 100 / creditos_periodo.count()) if creditos_periodo.count() > 0 else 0
                },
                'default_by_level': list(morosidad_por_nivel),
                'top_defaulted_clients': list(clientes_morosos)
            }
            
        except Exception as e:
            logger.error(f"Error getting default analysis: {e}")
            return {}
