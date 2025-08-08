from django.db import transaction
from django.utils import timezone
from decimal import Decimal
import logging
from typing import List

from apps.fintech.models import User, Credit
from ..models import CreditRecommendation, CustomerLifetimeValue

logger = logging.getLogger(__name__)

class RecommendationService:
    @staticmethod
    def generate_for_user(user: User) -> List[CreditRecommendation]:
        recs: List[CreditRecommendation] = []
        with transaction.atomic():
            clv = CustomerLifetimeValue.objects.filter(user=user).first()
            active_credits = Credit.objects.filter(user=user, pending_amount__gt=0)
            has_defaults = active_credits.filter(is_in_default=True).exists()

            if clv and clv.current_clv >= Decimal('5000') and not has_defaults:
                recs.append(CreditRecommendation.objects.create(
                    user=user,
                    recommendation_type='credit_limit_increase',
                    priority='high',
                    title='Elegible para aumento de límite',
                    description='Buen historial y alto CLV. Sugerimos evaluar aumento de límite.',
                    suggested_amount=None,
                    influencing_factors={'clv': float(clv.current_clv)},
                    confidence_score=Decimal('80.0')
                ))

            if has_defaults:
                recs.append(CreditRecommendation.objects.create(
                    user=user,
                    recommendation_type='payment_plan',
                    priority='urgent',
                    title='Proponer plan de pagos',
                    description='Créditos en mora detectados. Sugerir plan estructurado.',
                    suggested_amount=None,
                    influencing_factors={'defaults': True},
                    confidence_score=Decimal('90.0')
                ))

            last_credit = Credit.objects.filter(user=user).order_by('-created_at').first()
            if last_credit:
                days = (timezone.now() - last_credit.created_at).days
                if days > 120 and not has_defaults:
                    recs.append(CreditRecommendation.objects.create(
                        user=user,
                        recommendation_type='new_credit_offer',
                        priority='medium',
                        title='Nueva oferta de crédito',
                        description='Hace más de 4 meses del último crédito. Presentar nueva oferta.',
                        suggested_amount=None,
                        influencing_factors={'days_since_last': days},
                        confidence_score=Decimal('70.0')
                    ))

            return recs

    @staticmethod
    def deactivate_expired() -> int:
        count = 0
        from django.utils import timezone
        for rec in CreditRecommendation.objects.filter(is_active=True, expires_at__lt=timezone.now()):
            rec.is_active = False
            rec.save(update_fields=['is_active'])
            count += 1
        return count 