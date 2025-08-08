from celery import shared_task
import logging

from apps.fintech.models import User
from .services import CLVService, RecommendationService

logger = logging.getLogger(__name__)

@shared_task(bind=True, retry_backoff=True, acks_late=True)
def recalculate_all_clv(self):
    try:
        total = CLVService.recalculate_all()
        logger.info(f"CLV recalculado para {total} usuarios")
        return total
    except Exception as e:
        logger.error(f"Error in recalculate_all_clv: {e}")
        raise self.retry(exc=e, countdown=120)

@shared_task(bind=True, retry_backoff=True, acks_late=True)
def generate_recommendations(self, user_id: int = None):
    try:
        users = User.objects.filter(id=user_id) if user_id else User.objects.all()
        created = 0
        for user in users:
            recs = RecommendationService.generate_for_user(user)
            created += len(recs)
        logger.info(f"Recomendaciones generadas: {created}")
        return created
    except Exception as e:
        logger.error(f"Error in generate_recommendations: {e}")
        raise self.retry(exc=e, countdown=180)

@shared_task(bind=True, retry_backoff=True, acks_late=True)
def deactivate_expired_recommendations(self):
    try:
        count = RecommendationService.deactivate_expired()
        logger.info(f"Recomendaciones desactivadas: {count}")
        return count
    except Exception as e:
        logger.error(f"Error in deactivate_expired_recommendations: {e}")
        raise self.retry(exc=e, countdown=180) 