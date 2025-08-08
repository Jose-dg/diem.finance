from django.db import transaction
from django.utils import timezone
from decimal import Decimal
import logging
from datetime import timedelta, date
from typing import List, Optional

from apps.fintech.models import Credit, User
from apps.revenue.models import CreditEarnings
from ..models import CustomerLifetimeValue

logger = logging.getLogger(__name__)

class CLVService:
    @staticmethod
    def calculate_clv(user: User) -> CustomerLifetimeValue:
        try:
            with transaction.atomic():
                credits = Credit.objects.filter(user=user)
                if not credits.exists():
                    clv, _ = CustomerLifetimeValue.objects.get_or_create(user=user)
                    return clv

                total_credits = credits.count()
                total_amount = sum(c.price for c in credits)

                total_revenue = Decimal('0.00')
                for c in credits:
                    earnings = getattr(c, 'earnings_detail', None)
                    if earnings:
                        total_revenue += earnings.realized_earnings

                first_credit = credits.order_by('created_at').first()
                last_credit = credits.order_by('created_at').last()
                first_credit_date = first_credit.created_at if first_credit else None
                last_credit_date = last_credit.created_at if last_credit else None

                if first_credit_date and last_credit_date and first_credit_date != last_credit_date:
                    days_between = (last_credit_date - first_credit_date).days or 1
                    avg_credit_frequency = Decimal(str((total_credits * 365) / days_between))
                else:
                    avg_credit_frequency = Decimal('0.00')

                avg_credit_amount = Decimal(str(total_amount / total_credits)) if total_credits else Decimal('0.00')
                current_clv = total_revenue

                predicted_clv = CLVService._predict_future_clv(user, current_clv, avg_credit_frequency, avg_credit_amount)
                clv_tier = CLVService._determine_clv_tier(current_clv)
                churn_probability = CLVService._calculate_churn_probability(user, credits)
                next_credit_prediction = CLVService._predict_next_credit_date(credits)

                clv, _ = CustomerLifetimeValue.objects.update_or_create(
                    user=user,
                    defaults={
                        'current_clv': current_clv,
                        'predicted_clv': predicted_clv,
                        'clv_tier': clv_tier,
                        'total_revenue': total_revenue,
                        'total_credits': total_credits,
                        'avg_credit_amount': avg_credit_amount,
                        'avg_credit_frequency': avg_credit_frequency,
                        'first_credit_date': first_credit_date,
                        'last_credit_date': last_credit_date,
                        'next_credit_prediction': next_credit_prediction,
                        'churn_probability': churn_probability,
                        'calculation_metadata': {
                            'method': 'revenue_based',
                            'generated_at': timezone.now().isoformat()
                        }
                    }
                )
                return clv
        except Exception as e:
            logger.error(f"Error calculating CLV for {user.username}: {e}")
            raise

    @staticmethod
    def _predict_future_clv(user: User, current_clv: Decimal, avg_frequency: Decimal, avg_amount: Decimal) -> Decimal:
        growth_factor = min(avg_frequency * Decimal('0.1'), Decimal('2.0'))
        predicted = current_clv * (Decimal('1.0') + (growth_factor / Decimal('10.0')))
        if user.credits.filter(is_in_default=True).exists():
            predicted *= Decimal('0.7')
        return max(predicted, current_clv)

    @staticmethod
    def _determine_clv_tier(current_clv: Decimal) -> str:
        if current_clv < 1000:
            return 'bronze'
        if current_clv < 5000:
            return 'silver'
        if current_clv < 15000:
            return 'gold'
        return 'platinum'

    @staticmethod
    def _calculate_churn_probability(user: User, credits) -> Decimal:
        score = Decimal('0')
        defaults = credits.filter(is_in_default=True).count()
        score += Decimal(str(min(defaults * 15, 45)))
        last = credits.order_by('created_at').last()
        if last:
            days = (timezone.now() - last.created_at).days
            if days > 365:
                score += Decimal('30')
            elif days > 180:
                score += Decimal('20')
            elif days > 90:
                score += Decimal('10')
        return min(score, Decimal('100'))

    @staticmethod
    def _predict_next_credit_date(credits) -> Optional[date]:
        dates = [c.created_at for c in credits.order_by('created_at')]
        if len(dates) < 2:
            return None
        intervals = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
        if not intervals:
            return None
        avg = sum(intervals) / len(intervals)
        return (dates[-1] + timedelta(days=int(avg))).date()

    @staticmethod
    def recalculate_all() -> int:
        count = 0
        for user in User.objects.all():
            try:
                CLVService.calculate_clv(user)
                count += 1
            except Exception:
                continue
        return count 