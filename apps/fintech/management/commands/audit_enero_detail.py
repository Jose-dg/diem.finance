"""Deep investigation of January 2026 anomalies"""
from decimal import Decimal
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db.models import Sum, Count, Q, F
import pytz

from apps.fintech.models import (
    Credit, Transaction, Expense, CreditAdjustment, Installment,
    AccountMethodAmount
)


class Command(BaseCommand):
    help = 'Deep investigation of January 2026'

    def handle(self, *args, **options):
        bogota = pytz.timezone('America/Bogota')
        start = bogota.localize(datetime(2026, 1, 1, 0, 0, 0))
        end = bogota.localize(datetime(2026, 2, 1, 0, 0, 0))

        # ======================================
        # 1. Credits with negative earnings ALL TIME
        # ======================================
        self.stdout.write("=" * 80)
        self.stdout.write("CRÉDITOS CON EARNINGS NEGATIVOS (ALL TIME)")
        self.stdout.write("=" * 80)
        neg = Credit.objects.filter(earnings__lt=0).select_related('currency', 'subcategory', 'user')
        for c in neg:
            self.stdout.write(f"  ID: {c.id} | UID: {c.uid}")
            self.stdout.write(f"    cost: {c.cost:,.2f} | price: {c.price:,.2f} | earnings: {c.earnings:,.2f}")
            self.stdout.write(f"    state: {c.state} | created_at: {c.created_at}")
            self.stdout.write(f"    pending_amount: {c.pending_amount} | total_abonos: {c.total_abonos}")
            self.stdout.write(f"    currency: {c.currency} (id={c.currency_id})")
            self.stdout.write(f"    subcategory: {c.subcategory}")
            self.stdout.write(f"    user: {c.user}")
            self.stdout.write(f"    credit_days: {c.credit_days} | interest: {c.interest}")
            self.stdout.write("")

        # ======================================
        # 2. Expense transactions analysis
        # ======================================
        self.stdout.write("=" * 80)
        self.stdout.write("EXPENSE TRANSACTIONS EN ENERO")
        self.stdout.write("=" * 80)

        exp_ama = AccountMethodAmount.objects.filter(
            transaction__date__gte=start,
            transaction__date__lt=end,
            transaction__status='confirmed',
            transaction__transaction_type='expense'
        ).select_related('transaction', 'credit')

        for a in exp_ama[:20]:
            credit = a.credit
            self.stdout.write(
                f"  AMA ID: {a.id} | amount_paid: {a.amount_paid} | "
                f"credit_id: {a.credit_id} | "
                f"credit.cost: {credit.cost if credit else 'N/A'} | "
                f"credit.price: {credit.price if credit else 'N/A'} | "
                f"credit.created_at: {credit.created_at if credit else 'N/A'}"
            )

        self.stdout.write(f"\n  Total expense AMA count: {exp_ama.count()}")
        self.stdout.write(f"  Total expense AMA amount_paid: {exp_ama.aggregate(s=Sum('amount_paid'))['s']}")

        # Check patterns
        matches_cost = 0
        matches_price = 0
        neither = 0
        for a in exp_ama:
            if a.credit:
                if a.amount_paid == a.credit.cost:
                    matches_cost += 1
                elif a.amount_paid == a.credit.price:
                    matches_price += 1
                else:
                    neither += 1

        self.stdout.write(f"\n  amount_paid == credit.cost: {matches_cost}")
        self.stdout.write(f"  amount_paid == credit.price: {matches_price}")
        self.stdout.write(f"  neither: {neither}")

        # ======================================
        # 3. Income transactions analysis
        # ======================================
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("INCOME TRANSACTIONS EN ENERO")
        self.stdout.write("=" * 80)

        inc_ama = AccountMethodAmount.objects.filter(
            transaction__date__gte=start,
            transaction__date__lt=end,
            transaction__status='confirmed',
            transaction__transaction_type='income'
        ).select_related('transaction', 'credit')

        self.stdout.write(f"  Count: {inc_ama.count()}")
        self.stdout.write(f"  Total amount_paid: {inc_ama.aggregate(s=Sum('amount_paid'))['s']}")

        income_credits_before = inc_ama.filter(credit__created_at__lt=start).count()
        income_credits_during = inc_ama.filter(credit__created_at__gte=start, credit__created_at__lt=end).count()
        self.stdout.write(f"  Linked to credits created BEFORE January: {income_credits_before}")
        self.stdout.write(f"  Linked to credits created DURING January: {income_credits_during}")

        inc_before_sum = inc_ama.filter(credit__created_at__lt=start).aggregate(s=Sum('amount_paid'))['s'] or Decimal('0')
        inc_during_sum = inc_ama.filter(credit__created_at__gte=start, credit__created_at__lt=end).aggregate(s=Sum('amount_paid'))['s'] or Decimal('0')
        self.stdout.write(f"  Amount from credits BEFORE January: {inc_before_sum:,.2f}")
        self.stdout.write(f"  Amount from credits DURING January: {inc_during_sum:,.2f}")

        # ======================================
        # 4. Do expense transactions represent credit costs?
        # ======================================
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("ARE EXPENSE TXNS = CREDIT CREATION COSTS?")
        self.stdout.write("=" * 80)

        # Check if expense transactions are created at same time as credits
        exp_credits_during = exp_ama.filter(credit__created_at__gte=start, credit__created_at__lt=end)
        exp_credits_before = exp_ama.filter(credit__created_at__lt=start)
        self.stdout.write(f"  Expense AMA linked to credits created DURING January: {exp_credits_during.count()}")
        self.stdout.write(f"  Expense AMA linked to credits created BEFORE January: {exp_credits_before.count()}")
        self.stdout.write(f"  Amount for DURING: {exp_credits_during.aggregate(s=Sum('amount_paid'))['s'] or 0}")
        self.stdout.write(f"  Amount for BEFORE: {exp_credits_before.aggregate(s=Sum('amount_paid'))['s'] or 0}")

        # ======================================
        # 5. Understanding the full transaction picture
        # ======================================
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("FULL PICTURE: NET CASH FLOW FORMULA")
        self.stdout.write("=" * 80)

        # If expense txns = cost of creating credits, and income txns = payments received
        # Then: Net = Income received - Cost paid
        # This is already captured in the CAJA calculation
        # BUT: the -58,000 might be looking at ALL credits, not just January

        # Try: What if someone calculated ALL credit earnings + ALL expenses + ALL transactions?
        # for the period of January
        all_credits_sum = Credit.objects.aggregate(s=Sum('earnings'))['s'] or Decimal('0')
        self.stdout.write(f"  Total earnings ALL credits EVER: {all_credits_sum:,.2f}")

        # Or: What if they're looking at EarningsMetrics or similar stored calculations?
        try:
            from apps.revenue.models import EarningsMetrics
            jan_metrics = EarningsMetrics.objects.filter(
                period_start__gte=start,
                period_end__lte=end
            )
            for m in jan_metrics:
                self.stdout.write(f"  EarningsMetrics: {m}")
            if not jan_metrics.exists():
                self.stdout.write("  No EarningsMetrics found for January")
        except Exception as e:
            self.stdout.write(f"  Error reading EarningsMetrics: {e}")

        # ======================================
        # 6. Alternative calculation: What about using Transaction net flow directly?
        # ======================================
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("ALTERNATIVE: NETO FLUJO = Income AMA - Expense AMA (todo enero)")
        self.stdout.write("=" * 80)
        
        all_ama_jan = AccountMethodAmount.objects.filter(
            transaction__date__gte=start,
            transaction__date__lt=end
        )
        income_total = all_ama_jan.filter(
            transaction__transaction_type='income'
        ).aggregate(s=Sum('amount_paid'))['s'] or Decimal('0')
        expense_total = all_ama_jan.filter(
            transaction__transaction_type='expense'
        ).aggregate(s=Sum('amount_paid'))['s'] or Decimal('0')
        
        self.stdout.write(f"  Income total (all statuses): {income_total:,.2f}")
        self.stdout.write(f"  Expense total (all statuses): {expense_total:,.2f}")
        self.stdout.write(f"  NET: {income_total - expense_total:,.2f}")

        # What about the units? Values are very small (17,000 range)
        # but -58,000 is expected. Check if there's a multiplier/exchange
        # Or if the values might be in thousands (USD vs COP?)
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("CURRENCY CHECK")
        self.stdout.write("=" * 80)

        from apps.fintech.models import Currency
        for cur in Currency.objects.all():
            self.stdout.write(
                f"  {cur.id_currency} | {cur.currency} | exchange_rate: {cur.exchange_rate} | "
                f"asset_type: {cur.asset_type}"
            )

        # Check if -58,000 could be in COP (Colombian Pesos)
        # If exchange_rate is around 4000 COP/USD:
        # $5,708 earnings * -1 ~= not -58,000
        # Let's check: 17,643 - 12,565 = 5,078 * some factor?
        # 5,078 * ~11.4 ~= 58,000? No.
        # Or: are the December metrics wrong and bleeding into January?

        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("DECEMBER 2025 vs JANUARY 2026 COMPARISON")
        self.stdout.write("=" * 80)

        dec_start = bogota.localize(datetime(2025, 12, 1, 0, 0, 0))
        dec_end = bogota.localize(datetime(2026, 1, 1, 0, 0, 0))

        dec_credits = Credit.objects.filter(created_at__gte=dec_start, created_at__lt=dec_end)
        dec_agg = dec_credits.aggregate(
            total_earnings=Sum('earnings'),
            total_price=Sum('price'),
            total_cost=Sum('cost'),
            count=Count('id')
        )
        self.stdout.write(f"  December 2025 credits: {dec_agg['count']}")
        self.stdout.write(f"    Total earnings: {dec_agg['total_earnings'] or 0:,.2f}")
        self.stdout.write(f"    Total price: {dec_agg['total_price'] or 0:,.2f}")
        self.stdout.write(f"    Total cost: {dec_agg['total_cost'] or 0:,.2f}")

        # Check if there's a management command that calculates metrics
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("CHECK: Existing FinancialControlMetrics for January")
        self.stdout.write("=" * 80)
        try:
            from apps.insights.models import FinancialControlMetrics
            fcm = FinancialControlMetrics.objects.all()
            for m in fcm[:10]:
                self.stdout.write(f"  FCM: {m.__dict__}")
        except Exception as e:
            self.stdout.write(f"  Error: {e}")

        # ======================================
        # 7. Check the dashboard service / insights calculation
        # ======================================
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("CHECK: What the dashboard likely calculates")
        self.stdout.write("=" * 80)
        
        # Possible formula: earnings - expenses (from Expense model) - cost of credits
        # Since Expense is 0 for January, and earnings = 5,708
        # The -58,000 likely comes from including expense transactions (AMA) incorrectly
        
        # Let's check: What if someone uses earnings_of_all_credits_with_payments_in_jan 
        # MINUS cost_of_all_credits_with_payments_in_jan ?

        credits_with_payments_jan = Credit.objects.filter(
            installments__paid_on__gte=start.date(),
            installments__paid_on__lt=end.date()
        ).distinct()
        
        cpj_agg = credits_with_payments_jan.aggregate(
            total_earnings=Sum('earnings'),
            total_price=Sum('price'),
            total_cost=Sum('cost'),
            count=Count('id')
        )
        self.stdout.write(f"  Credits with payments in January: {cpj_agg['count']}")
        self.stdout.write(f"    Total earnings: {cpj_agg['total_earnings'] or 0:,.2f}")
        self.stdout.write(f"    Total price: {cpj_agg['total_price'] or 0:,.2f}")
        self.stdout.write(f"    Total cost: {cpj_agg['total_cost'] or 0:,.2f}")
