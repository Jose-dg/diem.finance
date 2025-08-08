from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta, date

from apps.fintech.models import Credit, User
from apps.forecasting.models import CreditPrediction, RiskAssessment, SeasonalPattern
from apps.forecasting.services import PredictionService, RiskService, SeasonalService
from apps.insights.models import CustomerLifetimeValue, CreditRecommendation
from apps.insights.services import CLVService, RecommendationService
from apps.revenue.services import EarningsService

class Command(BaseCommand):
    help = 'Valida forecasting, insights y revenue con datos existentes (muestra y métricas)'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=10, help='Cantidad de créditos/usuarios a muestrear (aleatorio)')
        parser.add_argument('--months', type=int, default=6, help='Meses hacia atrás para patrones estacionales')

    def handle(self, *args, **options):
        limit = max(1, min(10, options['limit']))
        months = options['months']

        self.stdout.write(self.style.NOTICE('Iniciando validación de forecasting, insights y revenue...'))

        # 1) Forecasting (aleatorio)
        credits = list(Credit.objects.filter(pending_amount__gt=0).order_by('?')[:limit])
        self.stdout.write(f"Créditos seleccionados (aleatorio): {len(credits)}")

        preds_created = 0
        risks_created = 0

        for credit in credits:
            for ptype in ['payment_date', 'completion_date', 'default_risk', 'payment_amount']:
                existing = CreditPrediction.objects.filter(
                    credit=credit,
                    prediction_type=ptype,
                    expires_at__gt=timezone.now()
                ).first()
                if not existing:
                    try:
                        PredictionService.create_credit_prediction(credit, ptype)
                        preds_created += 1
                    except Exception:
                        continue
            try:
                RiskService.assess_credit_default_risk(credit)
                risks_created += 1
            except Exception:
                continue

        self.stdout.write(self.style.SUCCESS(f"Predicciones creadas: {preds_created}"))
        self.stdout.write(self.style.SUCCESS(f"Evaluaciones de riesgo creadas: {risks_created}"))

        # 2) Revenue: calcular/validar ganancias para estos créditos
        revenue_updated = 0
        revenue_inconsistent = 0
        for credit in credits:
            try:
                earnings = EarningsService.create_or_update_earnings(credit)
                # Validación de consistencia
                try:
                    EarningsService.validate_earnings_consistency(earnings)
                except Exception:
                    revenue_inconsistent += 1
                revenue_updated += 1
            except Exception:
                continue
        self.stdout.write(self.style.SUCCESS(f"Registros de ganancias actualizados: {revenue_updated}"))
        self.stdout.write(self.style.WARNING(f"Registros de ganancias inconsistentes: {revenue_inconsistent}"))

        # 3) Patrones estacionales
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=months * 30)
        patterns_created = 0
        try:
            SeasonalService.identify_monthly_patterns(start_date, end_date, 'payments')
            SeasonalService.identify_monthly_patterns(start_date, end_date, 'credits')
            SeasonalService.identify_quarterly_patterns(start_date, end_date, 'payments')
            SeasonalService.identify_quarterly_patterns(start_date, end_date, 'credits')
            SeasonalService.identify_weekly_patterns(start_date, end_date, 'payments')
            SeasonalService.identify_weekly_patterns(start_date, end_date, 'credits')
            patterns_created = SeasonalPattern.objects.filter(identified_to=end_date).count()
        except Exception:
            pass
        self.stdout.write(self.style.SUCCESS(f"Patrones estacionales identificados (aprox): {patterns_created}"))

        # 4) Insights (usuarios aleatorios)
        users = list(User.objects.filter(credits__isnull=False).distinct().order_by('?')[:limit])
        clv_updated = 0
        recs_created = 0
        for user in users:
            try:
                CLVService.calculate_clv(user)
                clv_updated += 1
            except Exception:
                continue
            try:
                recs = RecommendationService.generate_for_user(user)
                recs_created += len(recs)
            except Exception:
                continue
        self.stdout.write(self.style.SUCCESS(f"CLV calculado/actualizado para usuarios: {clv_updated}"))
        self.stdout.write(self.style.SUCCESS(f"Recomendaciones generadas: {recs_created}"))

        # 5) Resumen
        self.stdout.write('--- Resumen ---')
        self.stdout.write(f"Créditos muestreados: {len(credits)}")
        self.stdout.write(f"Usuarios muestreados: {len(users)}")
        self.stdout.write(f"Predicciones activas totales: {CreditPrediction.objects.filter(expires_at__gt=timezone.now()).count()}")
        self.stdout.write(f"Riesgos activos totales: {RiskAssessment.objects.filter(valid_until__gt=timezone.now()).count()}")
        self.stdout.write(f"Patrones estacionales totales: {SeasonalPattern.objects.count()}")
        self.stdout.write(f"Usuarios con CLV: {CustomerLifetimeValue.objects.count()}")
        self.stdout.write(f"Recomendaciones activas: {CreditRecommendation.objects.filter(is_active=True).count()}")
        self.stdout.write(self.style.SUCCESS('Validación completada.')) 