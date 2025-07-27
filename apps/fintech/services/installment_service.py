from decimal import Decimal
from django.db.models import Sum, Count, Avg, F, Q
from django.utils import timezone
from django.db import transaction
from datetime import timedelta, date, datetime

from apps.fintech.models import Installment, Credit


class InstallmentService:
    """Servicio para gestionar la lógica de negocio de las cuotas"""
    
    @staticmethod
    def generate_installments_for_credit(credit):
        """
        Genera cuotas automáticamente para un crédito - OPTIMIZADO
        """
        try:
            # Eliminar cuotas existentes si las hay
            credit.installments.all().delete()
            
            # Calcular número de cuotas
            periodicity_days = credit.periodicity.days
            installment_number = credit.installment_number
            
            if not installment_number or installment_number <= 0:
                return False, "Número de cuotas inválido"
            
            # Calcular monto por cuota
            installment_value = credit.installment_value
            
            # Generar cuotas
            installments = []
            current_date = credit.first_date_payment
            
            for i in range(1, installment_number + 1):
                installment = Installment(
                    credit=credit,
                    number=i,
                    due_date=current_date,
                    amount=installment_value,
                    principal_amount=installment_value,
                    interest_amount=Decimal('0.00'),
                    remaining_amount=installment_value,
                    # Programar notificación 3 días antes
                    next_reminder_date=timezone.make_aware(
                        datetime.combine(current_date - timedelta(days=3), datetime.min.time())
                    )
                )
                installments.append(installment)
                
                # Calcular siguiente fecha
                current_date = current_date + timedelta(days=periodicity_days)
            
            # Crear todas las cuotas de una vez
            Installment.objects.bulk_create(installments)
            
            return True, f"Se generaron {len(installments)} cuotas exitosamente"
            
        except Exception as e:
            return False, f"Error generando cuotas: {str(e)}"
    
    @staticmethod
    def get_pending_installments_summary():
        """
        Obtiene resumen de cuotas pendientes
        """
        try:
            summary = {
                'total_pending': Installment.objects.pending_installments().count(),
                'total_overdue': Installment.objects.overdue_installments().count(),
                'due_today': Installment.objects.due_today().count(),
                'due_this_week': Installment.objects.due_this_week().count(),
                'high_risk': Installment.objects.high_risk_overdue().count(),
            }
            
            # Agregar montos
            overdue_summary = Installment.objects.overdue_summary()
            summary.update({
                'total_amount_overdue': float(overdue_summary['total_amount_overdue'] or 0),
                'total_fees': float(overdue_summary['total_fees'] or 0),
                'avg_days_overdue': float(overdue_summary['avg_days_overdue'] or 0),
            })
            
            return True, summary
            
        except Exception as e:
            return False, f"Error obteniendo resumen: {str(e)}"
    
    @staticmethod
    def get_expected_collection(start_date, end_date):
        """
        Calcula recaudo esperado en un período
        """
        try:
            installments = Installment.objects.for_expected_collection(start_date, end_date)
            
            summary = installments.aggregate(
                total_expected=Sum('amount'),
                total_remaining=Sum('remaining_amount'),
                count_installments=Count('id')
            )
            
            return True, {
                'total_expected': float(summary['total_expected'] or 0),
                'total_remaining': float(summary['total_remaining'] or 0),
                'count_installments': summary['count_installments'] or 0,
                'collection_rate': (
                    (summary['total_remaining'] / summary['total_expected'] * 100)
                    if summary['total_expected'] and summary['total_expected'] > 0
                    else 0
                )
            }
            
        except Exception as e:
            return False, f"Error calculando recaudo esperado: {str(e)}"
    
    @staticmethod
    def update_all_installment_statuses():
        """
        Actualiza el estado de todas las cuotas pendientes - OPTIMIZADO
        """
        try:
            today = timezone.now().date()
            
            # Actualización masiva con queries optimizadas
            with transaction.atomic():
                # 1. Marcar como vencidas las cuotas pendientes que pasaron la fecha
                overdue_count = Installment.objects.filter(
                    status__in=['pending', 'partial'],
                    due_date__lt=today
                ).update(
                    status='overdue',
                    days_overdue=F('days_overdue') + 1
                )
                
                # 2. Calcular recargos por mora en batch
                overdue_installments = Installment.objects.filter(
                    status='overdue'
                ).annotate(
                    calculated_days=F('days_overdue')
                )
                
                for installment in overdue_installments:
                    # Calcular recargo (5% por mes)
                    months_overdue = installment.calculated_days / 30
                    late_fee = installment.remaining_amount * Decimal('0.05') * Decimal(str(months_overdue))
                    installment.late_fee = late_fee
                    installment.save(update_fields=['late_fee'])
                
                # 3. Marcar como parciales las que tienen pagos
                partial_count = Installment.objects.filter(
                    status='pending',
                    amount_paid__gt=0
                ).update(status='partial')
            
            return True, f"Se actualizaron {overdue_count + partial_count} cuotas"
            
        except Exception as e:
            return False, f"Error actualizando estados: {str(e)}"
    
    @staticmethod
    def send_overdue_notifications():
        """
        Envía notificaciones de cuotas vencidas - OPTIMIZADO
        """
        try:
            overdue_installments = Installment.objects.filter(
                status='overdue',
                notification_sent=False
            ).select_related('credit__user')
            
            sent_count = 0
            for installment in overdue_installments:
                # Actualizar contadores sin llamar métodos del modelo
                installment.reminder_count += 1
                installment.last_reminder_date = timezone.now()
                installment.notification_sent = True
                installment.save(update_fields=['reminder_count', 'last_reminder_date', 'notification_sent'])
                sent_count += 1
                
                # Aquí se integraría con el sistema de notificaciones
                # send_notification(installment.credit.user, installment)
            
            return True, f"Se enviaron {sent_count} notificaciones"
            
        except Exception as e:
            return False, f"Error enviando notificaciones: {str(e)}"
    
    @staticmethod
    def get_installments_by_credit(credit_id):
        """
        Obtiene todas las cuotas de un crédito específico
        """
        try:
            installments = Installment.objects.filter(
                credit_id=credit_id
            ).order_by('number')
            
            return True, installments
            
        except Exception as e:
            return False, f"Error obteniendo cuotas: {str(e)}"
    
    @staticmethod
    def get_overdue_installments_by_user(user_id):
        """
        Obtiene cuotas vencidas de un usuario específico
        """
        try:
            overdue_installments = Installment.objects.filter(
                credit__user_id=user_id,
                status='overdue'
            ).select_related('credit', 'credit__user')
            
            return True, overdue_installments
            
        except Exception as e:
            return False, f"Error obteniendo cuotas vencidas: {str(e)}"
    
    @staticmethod
    def calculate_credit_morosidad(credit):
        """
        Calcula la morosidad de un crédito basado en sus cuotas
        """
        try:
            installments = credit.installments.all()
            
            if not installments.exists():
                return 0
            
            overdue_installments = installments.filter(status='overdue')
            total_installments = installments.count()
            
            if total_installments == 0:
                return 0
            
            morosidad_rate = (overdue_installments.count() / total_installments) * 100
            return round(morosidad_rate, 2)
            
        except Exception as e:
            return 0

    @staticmethod
    def bulk_update_remaining_amounts():
        """
        Actualiza montos restantes de todas las cuotas en batch
        """
        try:
            with transaction.atomic():
                # Actualizar remaining_amount para todas las cuotas
                Installment.objects.update(
                    remaining_amount=F('amount') - F('amount_paid')
                )
            
            return True, "Montos restantes actualizados"
        except Exception as e:
            return False, f"Error actualizando montos: {str(e)}"

    @staticmethod
    def schedule_payment_reminders():
        """
        Programa recordatorios de pago para cuotas que vencen pronto
        """
        try:
            today = timezone.now().date()
            reminder_date = today + timedelta(days=3)
            
            # Obtener cuotas que necesitan recordatorio
            installments_needing_reminder = Installment.objects.filter(
                status='pending',
                due_date__lte=reminder_date,
                due_date__gte=today,
                notification_sent=False
            )
            
            # Actualizar en batch
            updated_count = installments_needing_reminder.update(
                next_reminder_date=today
            )
            
            return True, f"Se programaron {updated_count} recordatorios"
        except Exception as e:
            return False, f"Error programando recordatorios: {str(e)}"

    @staticmethod
    def get_installment_analytics():
        """
        Obtiene analytics detallados de cuotas
        """
        try:
            today = timezone.now().date()
            
            analytics = {
                'summary': Installment.objects.summary_by_status(),
                'overdue_summary': Installment.objects.overdue_summary(),
                'due_today': Installment.objects.due_today().count(),
                'due_this_week': Installment.objects.due_this_week().count(),
                'high_risk': Installment.objects.high_risk_overdue().count(),
                'collection_this_month': InstallmentService.get_expected_collection(
                    today.replace(day=1),
                    (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                )[1] if InstallmentService.get_expected_collection(
                    today.replace(day=1),
                    (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                )[0] else {}
            }
            
            return True, analytics
        except Exception as e:
            return False, f"Error obteniendo analytics: {str(e)}" 