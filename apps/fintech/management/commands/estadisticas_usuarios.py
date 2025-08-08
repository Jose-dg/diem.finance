from django.core.management.base import BaseCommand
from django.db.models import Count, Sum, Q
from django.contrib.auth import get_user_model
from apps.fintech.models import Credit
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Muestra estadísticas de créditos por usuario'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='Número máximo de usuarios a mostrar'
        )
        parser.add_argument(
            '--min-credits',
            type=int,
            default=1,
            help='Mostrar solo usuarios con mínimo de créditos (default: 1)'
        )
        parser.add_argument(
            '--format',
            choices=['table', 'json', 'csv'],
            default='table',
            help='Formato de salida (default: table)'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        min_credits = options['min_credits']
        output_format = options['format']
        
        self.stdout.write("📊 ESTADÍSTICAS DE CRÉDITOS POR USUARIO")
        self.stdout.write("=" * 60)
        
        # Obtener usuarios con créditos (excluyendo admin)
        users_with_credits = User.objects.annotate(
            total_credits=Count('credits_registered'),
            pending_credits=Count('credits_registered', filter=Q(credits_registered__state='pending')),
            completed_credits=Count('credits_registered', filter=Q(credits_registered__state='completed')),
            total_amount=Sum('credits_registered__price'),
            total_pending=Sum('credits_registered__pending_amount'),
            total_payments=Sum('credits_registered__total_abonos')
        ).filter(
            total_credits__gte=min_credits
        ).exclude(
            username='admin'
        ).order_by('-total_credits', '-total_amount')
        
        if limit:
            users_with_credits = users_with_credits[:limit]
        
        total_users = users_with_credits.count()
        
        self.stdout.write(f"📈 ESTADÍSTICAS GENERALES:")
        self.stdout.write(f"   Total usuarios con créditos: {total_users}")
        
        # Estadísticas generales
        total_credits = sum(user.total_credits for user in users_with_credits)
        total_pending = sum(user.pending_credits for user in users_with_credits)
        total_completed = sum(user.completed_credits for user in users_with_credits)
        total_amount = sum(user.total_amount or 0 for user in users_with_credits)
        total_pending_amount = sum(user.total_pending or 0 for user in users_with_credits)
        total_payments = sum(user.total_payments or 0 for user in users_with_credits)
        
        self.stdout.write(f"   Total créditos: {total_credits}")
        self.stdout.write(f"   Créditos pendientes: {total_pending}")
        self.stdout.write(f"   Créditos completados: {total_completed}")
        self.stdout.write(f"   Monto total: ${total_amount:,.2f}")
        self.stdout.write(f"   Saldo pendiente total: ${total_pending_amount:,.2f}")
        self.stdout.write(f"   Total pagos: ${total_payments:,.2f}")
        self.stdout.write("")
        
        if output_format == 'table':
            self._print_table_format(users_with_credits)
        elif output_format == 'json':
            self._print_json_format(users_with_credits)
        elif output_format == 'csv':
            self._print_csv_format(users_with_credits)
        
        # Top 5 usuarios con más créditos
        self.stdout.write("")
        self.stdout.write("🏆 TOP 5 USUARIOS CON MÁS CRÉDITOS:")
        top_users = users_with_credits[:5]
        
        for i, user in enumerate(top_users, 1):
            self.stdout.write(f"   {i}. {user.username}")
            self.stdout.write(f"      Créditos: {user.total_credits}")
            self.stdout.write(f"      Pendientes: {user.pending_credits}")
            self.stdout.write(f"      Completados: {user.completed_credits}")
            self.stdout.write(f"      Monto total: ${user.total_amount or 0:,.2f}")
            self.stdout.write("")
        
        # Usuarios con créditos pendientes
        users_with_pending = users_with_credits.filter(pending_credits__gt=0)
        if users_with_pending.exists():
            self.stdout.write("⚠️  USUARIOS CON CRÉDITOS PENDIENTES:")
            for user in users_with_pending[:10]:  # Mostrar solo los primeros 10
                self.stdout.write(f"   {user.username}: {user.pending_credits} créditos pendientes")
        
        self.stdout.write("")
        self.stdout.write("✅ ANÁLISIS COMPLETADO")

    def _print_table_format(self, users):
        """Imprime en formato tabla"""
        self.stdout.write("📋 DETALLE POR USUARIO:")
        self.stdout.write("-" * 120)
        self.stdout.write(f"{'Usuario':<20} {'Total':<8} {'Pend.':<8} {'Comp.':<8} {'Monto Total':<15} {'Saldo Pend.':<15} {'Pagos':<15}")
        self.stdout.write("-" * 120)
        
        for user in users:
            self.stdout.write(
                f"{user.username:<20} "
                f"{user.total_credits:<8} "
                f"{user.pending_credits:<8} "
                f"{user.completed_credits:<8} "
                f"${user.total_amount or 0:<14,.2f} "
                f"${user.total_pending or 0:<14,.2f} "
                f"${user.total_payments or 0:<14,.2f}"
            )

    def _print_json_format(self, users):
        """Imprime en formato JSON"""
        import json
        
        data = []
        for user in users:
            user_data = {
                'username': user.username,
                'email': user.email,
                'total_credits': user.total_credits,
                'pending_credits': user.pending_credits,
                'completed_credits': user.completed_credits,
                'total_amount': float(user.total_amount or 0),
                'total_pending_amount': float(user.total_pending or 0),
                'total_payments': float(user.total_payments or 0)
            }
            data.append(user_data)
        
        self.stdout.write(json.dumps(data, indent=2))

    def _print_csv_format(self, users):
        """Imprime en formato CSV"""
        self.stdout.write("username,email,total_credits,pending_credits,completed_credits,total_amount,total_pending_amount,total_payments")
        
        for user in users:
            self.stdout.write(
                f"{user.username},"
                f"{user.email},"
                f"{user.total_credits},"
                f"{user.pending_credits},"
                f"{user.completed_credits},"
                f"{user.total_amount or 0},"
                f"{user.total_pending or 0},"
                f"{user.total_payments or 0}"
            ) 