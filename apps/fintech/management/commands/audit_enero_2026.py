"""
Auditoría Técnica-Financiera: Ganancia Enero 2026
Rango: 2026-01-01 00:00:00 a 2026-02-01 00:00:00 (America/Bogota, exclusivo)
"""
import json
from decimal import Decimal
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db.models import Sum, Count, Q, F, Avg, Max, Min, Case, When, Value, DecimalField
from django.utils import timezone
import pytz

from apps.fintech.models import (
    Credit, Transaction, Expense, CreditAdjustment, Installment,
    Currency, AccountMethodAmount, Adjustment
)


class Command(BaseCommand):
    help = 'Auditoría de ganancia Enero 2026'

    def handle(self, *args, **options):
        bogota = pytz.timezone('America/Bogota')
        start = bogota.localize(datetime(2026, 1, 1, 0, 0, 0))
        end = bogota.localize(datetime(2026, 2, 1, 0, 0, 0))

        self.stdout.write("=" * 80)
        self.stdout.write("AUDITORÍA GANANCIA ENERO 2026")
        self.stdout.write(f"Rango: {start} a {end} (exclusivo)")
        self.stdout.write("=" * 80)

        # =====================================================================
        # SECCIÓN 0: Conteos generales
        # =====================================================================
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("SECCIÓN 0: CONTEOS GENERALES")
        self.stdout.write("=" * 80)

        total_credits = Credit.objects.filter(created_at__gte=start, created_at__lt=end).count()
        total_expenses = Expense.objects.filter(created_at__gte=start, created_at__lt=end).count()
        total_transactions = Transaction.objects.filter(date__gte=start, date__lt=end).count()
        total_adjustments = CreditAdjustment.objects.filter(created_at__gte=start, created_at__lt=end).count()
        total_installments_paid = Installment.objects.filter(
            paid_on__gte=start.date(), paid_on__lt=end.date()
        ).count()

        self.stdout.write(f"Créditos creados en enero: {total_credits}")
        self.stdout.write(f"Gastos en enero: {total_expenses}")
        self.stdout.write(f"Transacciones en enero: {total_transactions}")
        self.stdout.write(f"Ajustes en enero: {total_adjustments}")
        self.stdout.write(f"Cuotas pagadas en enero: {total_installments_paid}")

        # =====================================================================
        # SECCIÓN 1A: GANANCIA DEVENGO
        # =====================================================================
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("SECCIÓN 1A: GANANCIA DEVENGO (Acumulación)")
        self.stdout.write("=" * 80)

        # 1) Earnings de créditos creados en enero
        credits_jan = Credit.objects.filter(created_at__gte=start, created_at__lt=end)
        earnings_agg = credits_jan.aggregate(
            total_earnings=Sum('earnings'),
            total_price=Sum('price'),
            total_cost=Sum('cost'),
            count=Count('id')
        )
        total_earnings = earnings_agg['total_earnings'] or Decimal('0.00')
        total_price = earnings_agg['total_price'] or Decimal('0.00')
        total_cost = earnings_agg['total_cost'] or Decimal('0.00')

        self.stdout.write(f"\n--- Créditos creados en Enero ---")
        self.stdout.write(f"  Cantidad: {earnings_agg['count']}")
        self.stdout.write(f"  Suma price: {total_price:,.2f}")
        self.stdout.write(f"  Suma cost: {total_cost:,.2f}")
        self.stdout.write(f"  Suma earnings (price - cost): {total_earnings:,.2f}")
        self.stdout.write(f"  Verificación (price - cost): {total_price - total_cost:,.2f}")

        # Desglose por estado
        by_state = credits_jan.values('state').annotate(
            cnt=Count('id'),
            sum_earnings=Sum('earnings'),
            sum_price=Sum('price'),
            sum_cost=Sum('cost')
        ).order_by('state')
        self.stdout.write(f"\n  Desglose por estado:")
        for row in by_state:
            self.stdout.write(f"    {row['state']}: count={row['cnt']}, earnings={row['sum_earnings']:,.2f}, price={row['sum_price']:,.2f}, cost={row['sum_cost']:,.2f}")

        # 2) Ajustes (CreditAdjustment) del mes
        adjustments_jan = CreditAdjustment.objects.filter(
            created_at__gte=start, created_at__lt=end
        ).select_related('type')

        adj_positive = adjustments_jan.filter(type__is_positive=True).aggregate(s=Sum('amount'))['s'] or Decimal('0.00')
        adj_negative = adjustments_jan.filter(type__is_positive=False).aggregate(s=Sum('amount'))['s'] or Decimal('0.00')
        adj_null_type = adjustments_jan.filter(type__isnull=True).aggregate(s=Sum('amount'))['s'] or Decimal('0.00')

        self.stdout.write(f"\n--- Ajustes (CreditAdjustment) en Enero ---")
        self.stdout.write(f"  Total ajustes: {adjustments_jan.count()}")
        self.stdout.write(f"  Suma ajustes positivos: +{adj_positive:,.2f}")
        self.stdout.write(f"  Suma ajustes negativos: -{adj_negative:,.2f}")
        self.stdout.write(f"  Ajustes sin tipo (type=null): {adj_null_type:,.2f}")
        self.stdout.write(f"  Neto ajustes: {adj_positive - adj_negative:,.2f}")

        # 3) Gastos (Expense) del mes
        expenses_jan = Expense.objects.filter(created_at__gte=start, created_at__lt=end)
        total_expense_amount = expenses_jan.aggregate(s=Sum('amount'))['s'] or Decimal('0.00')
        expense_count = expenses_jan.count()

        self.stdout.write(f"\n--- Gastos (Expense) en Enero ---")
        self.stdout.write(f"  Cantidad: {expense_count}")
        self.stdout.write(f"  Suma gastos: {total_expense_amount:,.2f}")

        # Desglose por subcategoría
        exp_by_subcat = expenses_jan.values('subcategory__name', 'subcategory__category__name').annotate(
            cnt=Count('id'),
            total=Sum('amount')
        ).order_by('-total')[:10]
        self.stdout.write(f"\n  Top subcategorías de gasto:")
        for row in exp_by_subcat:
            self.stdout.write(f"    {row['subcategory__category__name']}/{row['subcategory__name']}: count={row['cnt']}, total={row['total']:,.2f}")

        # 4) Transacciones del mes
        txns_jan = Transaction.objects.filter(date__gte=start, date__lt=end)
        txn_confirmed = txns_jan.filter(status='confirmed')

        self.stdout.write(f"\n--- Transacciones en Enero ---")
        self.stdout.write(f"  Total transacciones: {txns_jan.count()}")
        self.stdout.write(f"  Confirmadas: {txn_confirmed.count()}")

        # Transaction NO tiene campo amount. Los montos están en AccountMethodAmount.
        # Calcular montos via AccountMethodAmount
        ama_jan = AccountMethodAmount.objects.filter(
            transaction__date__gte=start,
            transaction__date__lt=end,
            transaction__status='confirmed'
        )
        income_ama = ama_jan.filter(transaction__transaction_type='income')
        expense_ama = ama_jan.filter(transaction__transaction_type='expense')

        income_amount = income_ama.aggregate(s=Sum('amount_paid'))['s'] or Decimal('0.00')
        expense_amount = expense_ama.aggregate(s=Sum('amount_paid'))['s'] or Decimal('0.00')

        self.stdout.write(f"  ⚠️  Transaction NO tiene campo 'amount'.")
        self.stdout.write(f"  Montos via AccountMethodAmount (amount_paid):")
        self.stdout.write(f"    Income confirmado: +{income_amount:,.2f}")
        self.stdout.write(f"    Expense confirmado: -{expense_amount:,.2f}")
        self.stdout.write(f"    Neto transacciones: {income_amount - expense_amount:,.2f}")

        # Desglose transacciones por status
        txn_by_status = txns_jan.values('status', 'transaction_type').annotate(
            cnt=Count('id')
        ).order_by('status', 'transaction_type')
        self.stdout.write(f"\n  Desglose por status/tipo:")
        for row in txn_by_status:
            self.stdout.write(f"    {row['status']}/{row['transaction_type']}: {row['cnt']}")

        # CÁLCULO GANANCIA DEVENGO
        ganancia_devengo = total_earnings + (adj_positive - adj_negative) - total_expense_amount + (income_amount - expense_amount)

        self.stdout.write(f"\n{'=' * 60}")
        self.stdout.write(f"GANANCIA DEVENGO ENERO 2026:")
        self.stdout.write(f"  + Earnings créditos:        {total_earnings:>15,.2f}")
        self.stdout.write(f"  + Ajustes positivos:        {adj_positive:>15,.2f}")
        self.stdout.write(f"  - Ajustes negativos:        {adj_negative:>15,.2f}")
        self.stdout.write(f"  - Gastos (Expense):         {total_expense_amount:>15,.2f}")
        self.stdout.write(f"  + Income transacciones:     {income_amount:>15,.2f}")
        self.stdout.write(f"  - Expense transacciones:    {expense_amount:>15,.2f}")
        self.stdout.write(f"  ─────────────────────────────────────────")
        self.stdout.write(f"  = TOTAL DEVENGO:            {ganancia_devengo:>15,.2f}")
        self.stdout.write(f"{'=' * 60}")

        # =====================================================================
        # SECCIÓN 1B: GANANCIA CAJA
        # =====================================================================
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("SECCIÓN 1B: GANANCIA CAJA (Flujo de caja)")
        self.stdout.write("=" * 80)

        # Abonos/pagos realizados en enero (via Installment.paid_on)
        installments_paid_jan = Installment.objects.filter(
            paid_on__gte=start.date(),
            paid_on__lt=end.date(),
            status__in=['paid', 'partial']
        )
        total_installments_paid_amount = installments_paid_jan.aggregate(
            s=Sum('amount_paid')
        )['s'] or Decimal('0.00')

        # También via AccountMethodAmount para transacciones de income en enero
        # (estos son los pagos reales que entraron)
        ama_income_jan = AccountMethodAmount.objects.filter(
            transaction__date__gte=start,
            transaction__date__lt=end,
            transaction__status='confirmed',
            transaction__transaction_type='income'
        )
        total_income_ama = ama_income_jan.aggregate(s=Sum('amount_paid'))['s'] or Decimal('0.00')

        self.stdout.write(f"\n--- Pagos recibidos en Enero ---")
        self.stdout.write(f"  Via Installment.paid_on (paid/partial): {total_installments_paid_amount:,.2f}")
        self.stdout.write(f"  Via AccountMethodAmount (income conf.): {total_income_ama:,.2f}")
        self.stdout.write(f"  ⚠️  Estos pueden superponerse. Usar AMA como fuente primaria.")

        # Para ganancia caja, necesitamos calcular qué porcentaje del pago es ganancia
        # Ganancia = pago * (earnings / price) por cada crédito
        # Lo haré crédito por crédito para los pagos de enero via Installments
        caja_earnings = Decimal('0.00')
        installments_for_caja = Installment.objects.filter(
            paid_on__gte=start.date(),
            paid_on__lt=end.date(),
            status__in=['paid', 'partial']
        ).select_related('credit')

        caja_details_count = 0
        caja_credits_with_issues = 0
        for inst in installments_for_caja:
            credit = inst.credit
            if credit and credit.price and credit.price > 0:
                earnings_rate = (credit.earnings or Decimal('0.00')) / credit.price
                inst_earnings = (inst.amount_paid or Decimal('0.00')) * earnings_rate
                caja_earnings += inst_earnings
                caja_details_count += 1
            else:
                caja_credits_with_issues += 1

        self.stdout.write(f"\n  Ganancia caja via cuotas (proporcional): {caja_earnings:,.2f}")
        self.stdout.write(f"  Cuotas procesadas: {caja_details_count}")
        self.stdout.write(f"  Cuotas con issues (credit null/price 0): {caja_credits_with_issues}")

        # Gastos pagados en enero (como caja)
        expenses_paid_jan = Expense.objects.filter(created_at__gte=start, created_at__lt=end)
        total_exp_paid = expenses_paid_jan.aggregate(s=Sum('amount'))['s'] or Decimal('0.00')

        ganancia_caja = caja_earnings - total_exp_paid

        self.stdout.write(f"\n{'=' * 60}")
        self.stdout.write(f"GANANCIA CAJA ENERO 2026:")
        self.stdout.write(f"  + Earnings proporcionales:  {caja_earnings:>15,.2f}")
        self.stdout.write(f"  - Gastos pagados:           {total_exp_paid:>15,.2f}")
        self.stdout.write(f"  ─────────────────────────────────────────")
        self.stdout.write(f"  = TOTAL CAJA:               {ganancia_caja:>15,.2f}")
        self.stdout.write(f"{'=' * 60}")

        # =====================================================================
        # SECCIÓN 2: TOP 20 REGISTROS QUE MÁS IMPACTARON
        # =====================================================================
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("SECCIÓN 2: TOP 20 REGISTROS MÁS IMPACTANTES")
        self.stdout.write("=" * 80)

        # 2.1 Créditos con earnings negativos o más extremos
        self.stdout.write(f"\n--- 2.1 Top 10 créditos por |earnings| (creados en enero) ---")
        top_credits = credits_jan.annotate(
            abs_earnings=Case(
                When(earnings__lt=0, then=F('earnings') * -1),
                default=F('earnings'),
                output_field=DecimalField()
            )
        ).order_by('-abs_earnings')[:10]
        for c in top_credits:
            self.stdout.write(
                f"  UID: {c.uid} | state: {c.state} | cost: {c.cost:,.2f} | price: {c.price:,.2f} | "
                f"earnings: {c.earnings:,.2f} | currency_id: {c.currency_id} | "
                f"pending: {c.pending_amount:,.2f} | total_abonos: {c.total_abonos:,.2f}"
            )

        # 2.2 Créditos con earnings negativos
        self.stdout.write(f"\n--- 2.2 Créditos con earnings NEGATIVOS (enero) ---")
        neg_earnings = credits_jan.filter(earnings__lt=0)
        for c in neg_earnings:
            self.stdout.write(
                f"  UID: {c.uid} | cost: {c.cost:,.2f} | price: {c.price:,.2f} | "
                f"earnings: {c.earnings:,.2f} | state: {c.state} | subcategory: {c.subcategory}"
            )
        if not neg_earnings.exists():
            self.stdout.write("  (Ninguno encontrado)")

        # 2.3 Top 10 gastos más altos
        self.stdout.write(f"\n--- 2.3 Top 10 gastos más altos (enero) ---")
        top_expenses = expenses_jan.order_by('-amount')[:10]
        for e in top_expenses:
            self.stdout.write(
                f"  UID: {e.uid} | amount: {e.amount:,.2f} | subcategory: {e.subcategory} | "
                f"account: {e.account} | created_at: {e.created_at} | desc: {(e.description or '')[:50]}"
            )

        # 2.4 Top 10 ajustes más altos
        self.stdout.write(f"\n--- 2.4 Top 10 ajustes más altos (enero) ---")
        top_adj = adjustments_jan.order_by('-amount')[:10]
        for a in top_adj:
            signo = '+' if a.type and a.type.is_positive else '-'
            self.stdout.write(
                f"  ID: {a.id} | {signo}{a.amount:,.2f} | type: {a.type} | "
                f"credit_id: {a.credit_id} | added_on: {a.added_on} | reason: {(a.reason or '')[:50]}"
            )
        if not top_adj.exists():
            self.stdout.write("  (No hay ajustes en enero)")

        # 2.5 Top AccountMethodAmount (transacciones)
        self.stdout.write(f"\n--- 2.5 Top 10 AccountMethodAmount más altos (enero) ---")
        top_ama = ama_jan.order_by('-amount_paid')[:10]
        for a in top_ama:
            self.stdout.write(
                f"  ID: {a.id} | amount_paid: {a.amount_paid:,.2f} | amount: {a.amount:,.2f} | "
                f"txn_type: {a.transaction.transaction_type} | txn_status: {a.transaction.status} | "
                f"credit_id: {a.credit_id} | currency_id: {a.currency_id}"
            )

        # =====================================================================
        # SECCIÓN 3: RED FLAGS Y VALIDACIONES
        # =====================================================================
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("SECCIÓN 3: RED FLAGS Y VALIDACIONES")
        self.stdout.write("=" * 80)

        # 3.1 Credits con cost > price
        self.stdout.write(f"\n--- 3.1 Créditos con cost > price (enero) ---")
        cost_gt_price = credits_jan.filter(cost__gt=F('price'))
        self.stdout.write(f"  Cantidad: {cost_gt_price.count()}")
        for c in cost_gt_price[:20]:
            self.stdout.write(
                f"  UID: {c.uid} | cost: {c.cost:,.2f} | price: {c.price:,.2f} | "
                f"earnings: {c.earnings:,.2f} | state: {c.state} | subcategory: {c.subcategory} | "
                f"currency_id: {c.currency_id}"
            )

        # 3.2 Credits con currency null o exchange_rate 0
        self.stdout.write(f"\n--- 3.2 Créditos con currency NULL (enero) ---")
        null_currency = credits_jan.filter(currency__isnull=True)
        self.stdout.write(f"  Cantidad: {null_currency.count()}")
        for c in null_currency[:10]:
            self.stdout.write(f"  UID: {c.uid} | cost: {c.cost:,.2f} | price: {c.price:,.2f} | earnings: {c.earnings:,.2f}")

        self.stdout.write(f"\n--- 3.2b Créditos con exchange_rate = 0 (enero) ---")
        zero_exchange = credits_jan.filter(currency__exchange_rate=0)
        self.stdout.write(f"  Cantidad: {zero_exchange.count()}")
        for c in zero_exchange[:10]:
            self.stdout.write(
                f"  UID: {c.uid} | currency: {c.currency} | exchange_rate: {c.currency.exchange_rate if c.currency else 'N/A'} | "
                f"earnings: {c.earnings:,.2f}"
            )

        # 3.3 Credits con interest calculado extraño
        self.stdout.write(f"\n--- 3.3 Créditos con interest > 100% o < 0 (enero) ---")
        weird_interest = credits_jan.filter(Q(interest__gt=100) | Q(interest__lt=0))
        self.stdout.write(f"  Cantidad: {weird_interest.count()}")
        for c in weird_interest[:10]:
            self.stdout.write(
                f"  UID: {c.uid} | interest: {c.interest} | credit_days: {c.credit_days} | "
                f"cost: {c.cost:,.2f} | price: {c.price:,.2f} | earnings: {c.earnings:,.2f}"
            )

        # 3.4 Credits con pending_amount < 0 o total_abonos > price
        self.stdout.write(f"\n--- 3.4 Créditos con pending_amount < 0 (enero) ---")
        neg_pending = credits_jan.filter(pending_amount__lt=0)
        self.stdout.write(f"  Cantidad: {neg_pending.count()}")
        for c in neg_pending[:10]:
            self.stdout.write(
                f"  UID: {c.uid} | pending_amount: {c.pending_amount:,.2f} | total_abonos: {c.total_abonos:,.2f} | "
                f"price: {c.price:,.2f}"
            )

        self.stdout.write(f"\n--- 3.4b Créditos con total_abonos > price (enero) ---")
        overpaid = credits_jan.filter(total_abonos__gt=F('price'))
        self.stdout.write(f"  Cantidad: {overpaid.count()}")
        for c in overpaid[:10]:
            self.stdout.write(
                f"  UID: {c.uid} | total_abonos: {c.total_abonos:,.2f} | price: {c.price:,.2f} | "
                f"pending_amount: {c.pending_amount:,.2f}"
            )

        # 3.5 Installments con amount null, status inconsistente
        self.stdout.write(f"\n--- 3.5 Installments con issues (todo el sistema) ---")
        null_amount_inst = Installment.objects.filter(amount__isnull=True).count()
        paid_no_date = Installment.objects.filter(status='paid', paid_on__isnull=True).count()
        overdue_paid = Installment.objects.filter(status='overdue', paid=True).count()
        self.stdout.write(f"  Cuotas con amount NULL: {null_amount_inst}")
        self.stdout.write(f"  Cuotas paid pero paid_on NULL: {paid_no_date}")
        self.stdout.write(f"  Cuotas overdue pero paid=True: {overdue_paid}")

        # 3.6 Expense duplicados
        self.stdout.write(f"\n--- 3.6 Posibles gastos duplicados (enero) ---")
        from django.db.models import Count as Count2
        dupes = expenses_jan.values(
            'amount', 'account_id', 'description'
        ).annotate(cnt=Count2('id')).filter(cnt__gt=1).order_by('-cnt')[:10]
        if dupes:
            for d in dupes:
                self.stdout.write(
                    f"  amount: {d['amount']:,.2f} | account_id: {d['account_id']} | "
                    f"desc: {(d['description'] or '')[:40]} | count: {d['cnt']}"
                )
        else:
            self.stdout.write("  (No se encontraron duplicados)")

        # 3.7 Transacciones no confirmadas incluidas (validación de exclusión)
        self.stdout.write(f"\n--- 3.7 Transacciones no-confirmed en enero ---")
        non_confirmed = txns_jan.exclude(status='confirmed')
        self.stdout.write(f"  Cantidad: {non_confirmed.count()}")
        nc_by_status = non_confirmed.values('status', 'transaction_type').annotate(cnt=Count('id'))
        for row in nc_by_status:
            self.stdout.write(f"    {row['status']}/{row['transaction_type']}: {row['cnt']}")

        # 3.8 Currencies en uso - verificar exchange_rate
        self.stdout.write(f"\n--- 3.8 Currencies usadas en créditos de enero ---")
        currencies_used = credits_jan.values(
            'currency__id', 'currency__id_currency', 'currency__currency',
            'currency__exchange_rate', 'currency__asset_type'
        ).annotate(cnt=Count('id'), sum_earnings=Sum('earnings')).order_by('-cnt')
        for cu in currencies_used:
            self.stdout.write(
                f"  {cu['currency__id_currency']} ({cu['currency__currency']}) | "
                f"exchange_rate: {cu['currency__exchange_rate']} | asset_type: {cu['currency__asset_type']} | "
                f"credits: {cu['cnt']} | sum_earnings: {cu['sum_earnings']:,.2f}"
            )

        # =====================================================================
        # SECCIÓN 4: DIAGNÓSTICO - ¿POR QUÉ -58,000?
        # =====================================================================
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("SECCIÓN 4: DIAGNÓSTICO DEL -58,000")
        self.stdout.write("=" * 80)

        # Verificar si hay créditos de meses anteriores que se
        # completaron/actualizaron en enero
        credits_completed_jan = Credit.objects.filter(
            state='completed',
            updated_at__gte=start,
            updated_at__lt=end
        ).exclude(created_at__gte=start, created_at__lt=end)
        self.stdout.write(f"\n  Créditos completados en enero pero creados ANTES: {credits_completed_jan.count()}")
        comp_agg = credits_completed_jan.aggregate(
            total_earnings=Sum('earnings'),
            total_price=Sum('price'),
            total_cost=Sum('cost')
        )
        self.stdout.write(f"    Earnings de esos: {comp_agg['total_earnings'] or 0:,.2f}")

        # Créditos con earnings negativos ALL TIME
        self.stdout.write(f"\n  Créditos con earnings negativos (ALL TIME):")
        neg_earns_all = Credit.objects.filter(earnings__lt=0)
        self.stdout.write(f"    Total: {neg_earns_all.count()}")
        neg_earns_sum = neg_earns_all.aggregate(s=Sum('earnings'))['s'] or Decimal('0.00')
        self.stdout.write(f"    Suma: {neg_earns_sum:,.2f}")

        # Créditos con earnings negativos creados en enero
        neg_earns_jan = credits_jan.filter(earnings__lt=0)
        neg_earns_jan_sum = neg_earns_jan.aggregate(s=Sum('earnings'))['s'] or Decimal('0.00')
        self.stdout.write(f"\n  Créditos con earnings negativos (ENERO):")
        self.stdout.write(f"    Total: {neg_earns_jan.count()}")
        self.stdout.write(f"    Suma: {neg_earns_jan_sum:,.2f}")

        # Resumen final
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("RESUMEN FINAL")
        self.stdout.write("=" * 80)
        self.stdout.write(f"  Ganancia DEVENGO: {ganancia_devengo:>15,.2f}")
        self.stdout.write(f"  Ganancia CAJA:    {ganancia_caja:>15,.2f}")
        self.stdout.write(f"\n  Valor reportado:  {Decimal('-58000'):>15,.2f}")
        self.stdout.write(f"  Diferencia DEVENGO vs reportado: {ganancia_devengo - Decimal('-58000'):>15,.2f}")

        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("FIN DE AUDITORÍA")
        self.stdout.write("=" * 80)
