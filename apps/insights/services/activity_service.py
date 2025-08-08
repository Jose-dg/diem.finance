from django.db import transaction
import logging
from typing import Optional

from apps.fintech.models import Credit, Transaction, User
from ..models import CustomerActivity

logger = logging.getLogger(__name__)

class ActivityService:
    @staticmethod
    def log(
        user: User,
        activity_type: str,
        description: str = '',
        *,
        credit: Optional[Credit] = None,
        transaction: Optional[Transaction] = None,
        amount: Optional[float] = None,
        metadata: Optional[dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> CustomerActivity:
        with transaction.atomic():
            activity = CustomerActivity.objects.create(
                user=user,
                activity_type=activity_type,
                credit=credit,
                transaction=transaction,
                description=description or '',
                amount=amount,
                activity_metadata=metadata or {},
                ip_address=ip_address,
                user_agent=user_agent or ''
            )
            logger.info(f"Activity logged: {activity_type} for {user.username}")
            return activity 