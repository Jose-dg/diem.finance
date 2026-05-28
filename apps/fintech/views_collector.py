from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    AccountMethodAmount,
    FeeDecision,
    Installment,
    Seller,
    Transaction as FinTransaction,
)


GRACE_DAYS = 3


def _installment_priority(days_since_due: int, due_date) -> str:
    today = date.today()
    days_until = (due_date - today).days if due_date else None

    if days_since_due > 30:
        return 'urgent'
    if days_since_due > 7 or (days_until is not None and days_until == 0):
        return 'high'
    if days_since_due > 1 or (days_until is not None and 0 < days_until <= 3):
        return 'medium'
    return 'low'


def _grace_days_remaining(days_since_due: int) -> int:
    if days_since_due <= 0:
        return 0
    remaining = GRACE_DAYS - days_since_due
    return max(0, remaining)


def _installment_to_dict(inst: Installment, today: date) -> dict:
    days_since_due = (today - inst.due_date).days if inst.due_date and inst.due_date < today else 0
    calculated_fee = inst.calculate_late_fee()
    total_due = (inst.remaining_amount or Decimal('0')) + calculated_fee
    priority = _installment_priority(days_since_due, inst.due_date)
    grace_remaining = _grace_days_remaining(days_since_due)

    client = inst.credit.user
    client_name = f"{client.first_name} {client.last_name}".strip() or client.username

    return {
        'installment_id': inst.id,
        'credit_uid': str(inst.credit.uid),
        'client_name': client_name,
        'client_id': client.id,
        'installment_number': inst.number,
        'amount_due': str(inst.amount or '0.00'),
        'amount_paid': str(inst.amount_paid),
        'remaining_amount': str(inst.remaining_amount),
        'late_fee': str(calculated_fee),
        'total_due': str(total_due.quantize(Decimal('0.01'))),
        'days_overdue': days_since_due,
        'grace_days_remaining': grace_remaining,
        'status': inst.status,
        'priority': priority,
        'credit_morosidad_level': inst.credit.morosidad_level,
    }


PRIORITY_ORDER = {'urgent': 0, 'high': 1, 'medium': 2, 'low': 3}


class CollectorPortfolioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, seller_id):
        seller = get_object_or_404(
            Seller.objects.select_related('user'),
            id=seller_id,
        )

        # Verificar autorización
        is_own_portfolio = (
            hasattr(request.user, 'seller_profile') and
            request.user.seller_profile.id == seller.id
        )
        has_global_perm = request.user.has_perm('fintech.view_all_portfolios')

        if not is_own_portfolio and not has_global_perm:
            return Response(
                {'detail': 'No tiene permiso para ver esta cartera.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        today = date.today()
        horizon = today + timedelta(days=30)

        # Cuotas relevantes: vencidas (sin límite) + próximas 30 días
        installments = (
            Installment.objects
            .filter(
                credit__seller=seller,
                status__in=['pending', 'partial', 'overdue'],
            )
            .filter(
                # vencidas sin límite de antigüedad O que vencen en los próximos 30 días
                due_date__lte=horizon
            )
            .exclude(status='cancelled')
            .select_related(
                'credit__user',
                'credit__seller',
                'credit__periodicity',
            )
            .order_by('due_date')
        )

        # Summary
        total_clients = set()
        clients_overdue = set()
        clients_critical = set()
        total_pending = 0
        total_overdue_count = 0
        total_amount_pending = Decimal('0')
        total_late_fees = Decimal('0')

        schedule: dict[str, list] = defaultdict(list)

        for inst in installments:
            credit = inst.credit
            client_id = credit.user_id
            total_clients.add(client_id)

            if inst.status == 'overdue':
                clients_overdue.add(client_id)
                total_overdue_count += 1
            if credit.morosidad_level == 'critical_default':
                clients_critical.add(client_id)

            total_pending += 1
            total_amount_pending += inst.remaining_amount or Decimal('0')
            fee = inst.calculate_late_fee()
            total_late_fees += fee

            key = inst.due_date.isoformat() if inst.due_date else 'sin-fecha'
            schedule[key].append((inst, today))

        # Ordenar schedule por fecha, dentro de cada fecha por prioridad y nombre
        ordered_schedule = {}
        for key in sorted(schedule.keys()):
            items = schedule[key]
            entries = [_installment_to_dict(inst, today) for inst, _ in items]
            entries.sort(
                key=lambda x: (PRIORITY_ORDER.get(x['priority'], 99), x['client_name'])
            )
            ordered_schedule[key] = entries

        clients_on_time = len(total_clients) - len(clients_overdue)

        seller_name = f"{seller.user.first_name} {seller.user.last_name}".strip() or seller.user.username

        return Response({
            'seller': {
                'id': seller.id,
                'name': seller_name,
                'username': seller.user.username,
            },
            'summary': {
                'total_clients': len(total_clients),
                'clients_on_time': clients_on_time,
                'clients_overdue': len(clients_overdue),
                'clients_critical': len(clients_critical),
                'total_installments_pending': total_pending,
                'total_installments_overdue': total_overdue_count,
                'total_amount_pending': str(total_amount_pending.quantize(Decimal('0.01'))),
                'total_late_fees_pending': str(total_late_fees.quantize(Decimal('0.01'))),
            },
            'schedule': ordered_schedule,
        })


class FeeDecisionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        installment_id = data.get('installment_id')
        decision_value = data.get('decision')
        applied_fee_raw = data.get('applied_fee')
        reason = data.get('reason', '').strip()

        # --- Validaciones básicas ---
        if not installment_id:
            return Response({'detail': 'installment_id es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        installment = get_object_or_404(
            Installment.objects.select_related('credit__seller__user'),
            id=installment_id,
        )

        # Verificar autorización
        credit = installment.credit
        is_own_credit = (
            credit.seller and
            hasattr(request.user, 'seller_profile') and
            credit.seller.id == request.user.seller_profile.id
        )
        has_global_perm = request.user.has_perm('fintech.manage_all_fee_decisions')

        if not is_own_credit and not has_global_perm:
            return Response(
                {'detail': 'No tiene permiso para gestionar recargos de esta cuota.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        valid_decisions = ('applied', 'partial', 'waived')
        if decision_value not in valid_decisions:
            return Response(
                {'detail': f"decision debe ser uno de: {', '.join(valid_decisions)}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if applied_fee_raw is None:
            return Response({'detail': 'applied_fee es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            applied_fee = Decimal(str(applied_fee_raw)).quantize(Decimal('0.01'))
        except Exception:
            return Response({'detail': 'applied_fee debe ser un número válido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Calcular recargo actual en tiempo real
        calculated_fee = installment.calculate_late_fee()

        # Validaciones por tipo de decisión
        if decision_value in ('partial', 'waived') and not reason:
            return Response(
                {'detail': 'reason es obligatorio cuando decision es partial o waived.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if decision_value == 'applied':
            if abs(applied_fee - calculated_fee) > Decimal('0.01'):
                return Response(
                    {
                        'detail': (
                            f"Para aplicar el recargo completo, applied_fee debe coincidir con "
                            f"el recargo calculado actualmente. Recargo actual: {calculated_fee}."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if decision_value == 'partial':
            if not (Decimal('0') < applied_fee < calculated_fee):
                return Response(
                    {'detail': 'Para partial, applied_fee debe ser mayor a 0 y menor al recargo calculado.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if decision_value == 'waived':
            if applied_fee != Decimal('0'):
                return Response(
                    {'detail': 'Para waived, applied_fee debe ser 0.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # --- Seller del request ---
        seller = getattr(request.user, 'seller_profile', None)

        with transaction.atomic():
            # 1. Registrar decisión
            fee_decision = FeeDecision.objects.create(
                installment=installment,
                seller=seller,
                calculated_fee=calculated_fee,
                applied_fee=applied_fee,
                decision=decision_value,
                reason=reason or None,
            )

            # 2. Cobrar el recargo si applied_fee > 0
            if applied_fee > Decimal('0'):
                fee_transaction = FinTransaction.objects.create(
                    transaction_type='income',
                    user=credit.user,
                    category=credit.subcategory,
                    status='confirmed',
                    source='mobile',
                    description=f"Recargo por mora — cuota #{installment.number} crédito {credit.uid}",
                )
                today_str = date.today().isoformat()
                AccountMethodAmount.objects.create(
                    payment_method=credit.payment,
                    payment_code=f"FEE-{installment.id}-{today_str}",
                    amount=applied_fee,
                    amount_paid=applied_fee,
                    currency=credit.currency,
                    credit=credit,
                    transaction=fee_transaction,
                )

            # 3. Actualizar late_fee de la cuota con lo efectivamente cobrado
            installment.late_fee = applied_fee
            installment.save(update_fields=['late_fee'])

        return Response(
            {
                'fee_decision_id': fee_decision.id,
                'installment_id': installment.id,
                'calculated_fee': str(calculated_fee),
                'applied_fee': str(applied_fee),
                'decision': decision_value,
                'message': 'Decisión registrada correctamente.',
            },
            status=status.HTTP_201_CREATED,
        )
