from django.core.management.base import BaseCommand
from django.db.models import Count, Sum, Q
from django.contrib.auth import get_user_model
from apps.fintech.models import Credit
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Muestra todos los usuarios y sus créditos individuales'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='Número máximo de usuarios a mostrar'
        )
        parser.add_argument(
            '--only-pending',
            action='store_true',
            help='Mostrar solo usuarios con créditos pendientes'
        )
        parser.add_argument(
            '--format',
            choices=['table', 'simple'],
            default='table',
            help='Formato de salida (default: table)'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        only_pending = options['only_pending']
        output_format = options['format']
        
        self.stdout.write("👥 CRÉDITOS POR USUARIO")
        self.stdout.write("=" * 50)
        
        # Query optimizada para usuarios responsables de créditos
        users_query = User.objects.prefetch_related('credits_registered').annotate(
            total_credits=Count('credits_registered'),
            pending_credits=Count('credits_registered', filter=Q(credits_registered__state='pending')),
            completed_credits=Count('credits_registered', filter=Q(credits_registered__state='completed')),
            total_amount=Sum('credits_registered__price'),
            total_pending_amount=Sum('credits_registered__pending_amount'),
            total_payments=Sum('credits_registered__total_abonos')
        ).filter(
            total_credits__gt=0
        ).exclude(
            username__in=['admin', 'lorena']  # Excluir usuarios administrativos
        )
        
        if only_pending:
            users_query = users_query.filter(pending_credits__gt=0)
        
        users = users_query.order_by('-total_credits', 'username')
        
        if limit:
            users = users[:limit]
        
        total_users = users.count()
        
        self.stdout.write(f"📊 TOTAL DE USUARIOS CON CRÉDITOS: {total_users}")
        self.stdout.write("")
        
        if output_format == 'table':
            self._print_table_format(users)
        else:
            self._print_simple_format(users)
        
        # Estadísticas adicionales
        self._print_statistics(users)
        
        self.stdout.write("")
        self.stdout.write("✅ ANÁLISIS COMPLETADO")

    def _print_table_format(self, users):
        """Imprime en formato tabla detallado"""
        self.stdout.write("📋 DETALLE COMPLETO POR USUARIO:")
        self.stdout.write("-" * 100)
        self.stdout.write(f"{'Usuario':<20} {'Total':<8} {'Pend.':<8} {'Comp.':<8} {'Monto Total':<15} {'Saldo Pend.':<15}")
        self.stdout.write("-" * 100)
        
        for user in users:
            self.stdout.write(
                f"{user.username:<20} "
                f"{user.total_credits:<8} "
                f"{user.pending_credits:<8} "
                f"{user.completed_credits:<8} "
                f"${user.total_amount or 0:<14,.2f} "
                f"${user.total_pending_amount or 0:<14,.2f}"
            )

    def _print_simple_format(self, users):
        """Imprime en formato simple y legible"""
        self.stdout.write("👤 USUARIOS Y SUS CRÉDITOS:")
        self.stdout.write("")
        
        for i, user in enumerate(users, 1):
            self.stdout.write(f"{i:2d}. {user.username}")
            self.stdout.write(f"     📊 Total créditos: {user.total_credits}")
            self.stdout.write(f"     ⏳ Pendientes: {user.pending_credits}")
            self.stdout.write(f"     ✅ Completados: {user.completed_credits}")
            self.stdout.write(f"     💰 Monto total: ${user.total_amount or 0:,.2f}")
            self.stdout.write(f"     💸 Saldo pendiente: ${user.total_pending_amount or 0:,.2f}")
            
            # Mostrar créditos individuales si son pocos
            if user.total_credits <= 5:
                credits = user.credits_registered.all()
                for credit in credits:
                    status_icon = "⏳" if credit.state == 'pending' else "✅"
                    self.stdout.write(f"        {status_icon} {credit.uid[:8]}... - ${credit.price:,.2f} ({credit.state})")
            
            self.stdout.write("")

    def _print_statistics(self, users):
        """Imprime estadísticas adicionales"""
        if not users:
            return
            
        self.stdout.write("📈 ESTADÍSTICAS ADICIONALES:")
        
        # Usuarios con más créditos
        top_users = users[:5]
        self.stdout.write("   🏆 TOP 5 USUARIOS CON MÁS CRÉDITOS:")
        for i, user in enumerate(top_users, 1):
            self.stdout.write(f"      {i}. {user.username}: {user.total_credits} créditos")
        
        # Usuarios con créditos pendientes
        users_with_pending = [u for u in users if u.pending_credits > 0]
        if users_with_pending:
            self.stdout.write(f"   ⚠️  USUARIOS CON CRÉDITOS PENDIENTES: {len(users_with_pending)}")
            for user in users_with_pending[:10]:  # Mostrar solo los primeros 10
                self.stdout.write(f"      • {user.username}: {user.pending_credits} pendientes")
        
        # Distribución de créditos
        credit_distribution = {}
        for user in users:
            count = user.total_credits
            credit_distribution[count] = credit_distribution.get(count, 0) + 1
        
        self.stdout.write("   📊 DISTRIBUCIÓN DE CRÉDITOS:")
        for credit_count in sorted(credit_distribution.keys()):
            user_count = credit_distribution[credit_count]
            self.stdout.write(f"      {credit_count} crédito{'s' if credit_count > 1 else ''}: {user_count} usuario{'s' if user_count > 1 else ''}")
        
        # Totales
        total_credits = sum(user.total_credits for user in users)
        total_pending = sum(user.pending_credits for user in users)
        total_completed = sum(user.completed_credits for user in users)
        total_amount = sum(user.total_amount or 0 for user in users)
        total_pending_amount = sum(user.total_pending_amount or 0 for user in users)
        
        self.stdout.write("   💰 TOTALES:")
        self.stdout.write(f"      Total créditos: {total_credits}")
        self.stdout.write(f"      Créditos pendientes: {total_pending}")
        self.stdout.write(f"      Créditos completados: {total_completed}")
        self.stdout.write(f"      Monto total: ${total_amount:,.2f}")
        self.stdout.write(f"      Saldo pendiente total: ${total_pending_amount:,.2f}") 