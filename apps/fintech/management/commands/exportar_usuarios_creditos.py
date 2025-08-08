from django.core.management.base import BaseCommand
from django.db.models import Count, Sum, Q
from apps.fintech.models import User, Credit
from decimal import Decimal

class Command(BaseCommand):
    help = 'Exporta datos de créditos por usuario en formato CSV'

    def handle(self, *args, **options):
        # Query optimizada para obtener usuarios con estadísticas de créditos
        users_query = User.objects.annotate(
            total_credits=Count('credits'),
            pending_credits=Count('credits', filter=Q(credits__state='pending')),
            completed_credits=Count('credits', filter=Q(credits__state='completed')),
            total_amount=Sum('credits__price'),
            total_pending_amount=Sum('credits__pending_amount'),
            total_payments=Sum('credits__total_abonos'),
            # Créditos por estado de mora
            on_time_credits=Count('credits', filter=Q(credits__morosidad_level='on_time')),
            moderate_default_credits=Count('credits', filter=Q(credits__morosidad_level='moderate_default')),
            critical_default_credits=Count('credits', filter=Q(credits__morosidad_level='critical_default'))
        ).order_by('username')
        
        users = list(users_query)
        
        if not users:
            self.stdout.write("No se encontraron usuarios")
            return
        
        # Imprimir leyenda
        self.stdout.write("LEYENDA:")
        self.stdout.write("Usuario: Nombre del usuario")
        self.stdout.write("TC: Total Créditos")
        self.stdout.write("CP: Créditos Pendientes")
        self.stdout.write("CC: Créditos Completados")
        self.stdout.write("MT: Monto Total ($)")
        self.stdout.write("SP: Saldo Pendiente ($)")
        self.stdout.write("TP: Total Pagos ($)")
        self.stdout.write("AD: Al Día")
        self.stdout.write("MM: Mora Moderada")
        self.stdout.write("MC: Mora Crítica")
        self.stdout.write("")
        
        # Imprimir encabezado
        headers = [
            "Usuario",
            "TC",
            "CP",
            "CC",
            "MT",
            "SP",
            "TP",
            "AD",
            "MM",
            "MC"
        ]
        self.stdout.write(",".join(headers))
        
        # Imprimir datos
        for user in users:
            values = [
                user.username,
                str(user.total_credits),
                str(user.pending_credits),
                str(user.completed_credits),
                f"{user.total_amount or 0:.2f}",
                f"{user.total_pending_amount or 0:.2f}",
                f"{user.total_payments or 0:.2f}",
                str(user.on_time_credits),
                str(user.moderate_default_credits),
                str(user.critical_default_credits)
            ]
            self.stdout.write(",".join(values))
        
        # Imprimir estadísticas
        self.stdout.write("\nESTADÍSTICAS:")
        users_with_credits = [u for u in users if u.total_credits > 0]
        
        # Totales
        total_credits = sum(user.total_credits for user in users_with_credits)
        total_pending = sum(user.pending_credits for user in users_with_credits)
        total_completed = sum(user.completed_credits for user in users_with_credits)
        total_amount = sum(user.total_amount or 0 for user in users_with_credits)
        total_pending_amount = sum(user.total_pending_amount or 0 for user in users_with_credits)
        total_payments = sum(user.total_payments or 0 for user in users_with_credits)
        total_on_time = sum(user.on_time_credits for user in users_with_credits)
        total_moderate = sum(user.moderate_default_credits for user in users_with_credits)
        total_critical = sum(user.critical_default_credits for user in users_with_credits)
        
        stats = [
            "TOTALES",
            str(total_credits),
            str(total_pending),
            str(total_completed),
            f"{total_amount:.2f}",
            f"{total_pending_amount:.2f}",
            f"{total_payments:.2f}",
            str(total_on_time),
            str(total_moderate),
            str(total_critical)
        ]
        self.stdout.write(",".join(stats)) 