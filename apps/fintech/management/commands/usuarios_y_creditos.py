from django.core.management.base import BaseCommand
from django.db.models import Count, Sum, Q
from django.contrib.auth import get_user_model
from apps.fintech.models import Credit
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Muestra todos los usuarios del modelo User y sus créditos asociados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='Número máximo de usuarios a mostrar'
        )
        parser.add_argument(
            '--only-with-credits',
            action='store_true',
            help='Mostrar solo usuarios que tienen créditos'
        )
        parser.add_argument(
            '--format',
            choices=['table', 'simple', 'detailed'],
            default='simple',
            help='Formato de salida (default: simple)'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        only_with_credits = options['only_with_credits']
        output_format = options['format']
        
        self.stdout.write("👥 USUARIOS Y SUS CRÉDITOS ASOCIADOS")
        self.stdout.write("=" * 60)
        
        # Obtener todos los usuarios con información de créditos
        users_query = User.objects.annotate(
            total_credits=Count('credits_registered'),
            pending_credits=Count('credits_registered', filter=Q(credits_registered__state='pending')),
            completed_credits=Count('credits_registered', filter=Q(credits_registered__state='completed')),
            total_amount=Sum('credits_registered__price'),
            total_pending_amount=Sum('credits_registered__pending_amount'),
            total_payments=Sum('credits_registered__total_abonos')
        ).order_by('-total_credits', 'username')
        
        if only_with_credits:
            users_query = users_query.filter(total_credits__gt=0)
        
        if limit:
            users_query = users_query[:limit]
        
        users = list(users_query)
        total_users = len(users)
        users_with_credits = [u for u in users if u.total_credits > 0]
        
        self.stdout.write(f"📊 ESTADÍSTICAS:")
        self.stdout.write(f"   Total usuarios: {total_users}")
        self.stdout.write(f"   Usuarios con créditos: {len(users_with_credits)}")
        self.stdout.write(f"   Usuarios sin créditos: {total_users - len(users_with_credits)}")
        self.stdout.write("")
        
        if output_format == 'table':
            self._print_table_format(users)
        elif output_format == 'detailed':
            self._print_detailed_format(users)
        else:
            self._print_simple_format(users)
        
        # Estadísticas adicionales
        if users_with_credits:
            self._print_statistics(users_with_credits)
        
        self.stdout.write("")
        self.stdout.write("✅ ANÁLISIS COMPLETADO")

    def _print_simple_format(self, users):
        """Imprime en formato simple"""
        self.stdout.write("👤 USUARIOS Y SUS CRÉDITOS:")
        self.stdout.write("")
        
        for i, user in enumerate(users, 1):
            if user.total_credits > 0:
                self.stdout.write(f"{i:2d}. {user.username}")
                self.stdout.write(f"     📊 Total créditos: {user.total_credits}")
                self.stdout.write(f"     ⏳ Pendientes: {user.pending_credits}")
                self.stdout.write(f"     ✅ Completados: {user.completed_credits}")
                self.stdout.write(f"     💰 Monto total: ${user.total_amount or 0:,.2f}")
                self.stdout.write(f"     💸 Saldo pendiente: ${user.total_pending_amount or 0:,.2f}")
                self.stdout.write("")
            else:
                self.stdout.write(f"{i:2d}. {user.username} - Sin créditos")
                self.stdout.write("")

    def _print_detailed_format(self, users):
        """Imprime en formato detallado con información completa"""
        self.stdout.write("📋 DETALLE COMPLETO DE USUARIOS:")
        self.stdout.write("")
        
        for i, user in enumerate(users, 1):
            self.stdout.write(f"{i:2d}. {user.username}")
            self.stdout.write(f"     📧 Email: {user.email}")
            self.stdout.write(f"     📅 Fecha registro: {user.date_joined.strftime('%Y-%m-%d')}")
            self.stdout.write(f"     👤 Nombre: {user.first_name} {user.last_name}")
            self.stdout.write(f"     🔐 Activo: {'Sí' if user.is_active else 'No'}")
            self.stdout.write(f"     👑 Staff: {'Sí' if user.is_staff else 'No'}")
            self.stdout.write(f"     📊 Total créditos: {user.total_credits}")
            
            if user.total_credits > 0:
                self.stdout.write(f"     ⏳ Pendientes: {user.pending_credits}")
                self.stdout.write(f"     ✅ Completados: {user.completed_credits}")
                self.stdout.write(f"     💰 Monto total: ${user.total_amount or 0:,.2f}")
                self.stdout.write(f"     💸 Saldo pendiente: ${user.total_pending_amount or 0:,.2f}")
                self.stdout.write(f"     💳 Total pagos: ${user.total_payments or 0:,.2f}")
                
                # Mostrar créditos individuales si son pocos
                if user.total_credits <= 10:
                    credits = user.credits_registered.all()
                    self.stdout.write(f"     📋 Créditos individuales:")
                    for credit in credits:
                        status_icon = "⏳" if credit.state == 'pending' else "✅"
                        self.stdout.write(f"        {status_icon} {credit.uid[:8]}... - ${credit.price:,.2f} ({credit.state})")
            
            self.stdout.write("")

    def _print_table_format(self, users):
        """Imprime en formato tabla"""
        self.stdout.write("📋 TABLA DE USUARIOS Y CRÉDITOS:")
        self.stdout.write("-" * 120)
        self.stdout.write(f"{'Usuario':<20} {'Email':<25} {'Total':<8} {'Pend.':<8} {'Comp.':<8} {'Monto Total':<15} {'Saldo Pend.':<15}")
        self.stdout.write("-" * 120)
        
        for user in users:
            email_display = user.email[:24] + "..." if len(user.email) > 25 else user.email
            self.stdout.write(
                f"{user.username:<20} "
                f"{email_display:<25} "
                f"{user.total_credits:<8} "
                f"{user.pending_credits:<8} "
                f"{user.completed_credits:<8} "
                f"${user.total_amount or 0:<14,.2f} "
                f"${user.total_pending_amount or 0:<14,.2f}"
            )

    def _print_statistics(self, users_with_credits):
        """Imprime estadísticas de usuarios con créditos"""
        if not users_with_credits:
            return
            
        self.stdout.write("📈 ESTADÍSTICAS DE USUARIOS CON CRÉDITOS:")
        
        # Usuarios con más créditos
        top_users = sorted(users_with_credits, key=lambda x: x.total_credits, reverse=True)[:5]
        self.stdout.write("   🏆 TOP 5 USUARIOS CON MÁS CRÉDITOS:")
        for i, user in enumerate(top_users, 1):
            self.stdout.write(f"      {i}. {user.username}: {user.total_credits} créditos")
        
        # Usuarios con créditos pendientes
        users_with_pending = [u for u in users_with_credits if u.pending_credits > 0]
        if users_with_pending:
            self.stdout.write(f"   ⚠️  USUARIOS CON CRÉDITOS PENDIENTES: {len(users_with_pending)}")
            for user in users_with_pending[:10]:
                self.stdout.write(f"      • {user.username}: {user.pending_credits} pendientes")
        
        # Distribución de créditos
        credit_distribution = {}
        for user in users_with_credits:
            count = user.total_credits
            credit_distribution[count] = credit_distribution.get(count, 0) + 1
        
        self.stdout.write("   📊 DISTRIBUCIÓN DE CRÉDITOS:")
        for credit_count in sorted(credit_distribution.keys()):
            user_count = credit_distribution[credit_count]
            self.stdout.write(f"      {credit_count} crédito{'s' if credit_count > 1 else ''}: {user_count} usuario{'s' if user_count > 1 else ''}")
        
        # Totales
        total_credits = sum(user.total_credits for user in users_with_credits)
        total_pending = sum(user.pending_credits for user in users_with_credits)
        total_completed = sum(user.completed_credits for user in users_with_credits)
        total_amount = sum(user.total_amount or 0 for user in users_with_credits)
        total_pending_amount = sum(user.total_pending_amount or 0 for user in users_with_credits)
        total_payments = sum(user.total_payments or 0 for user in users_with_credits)
        
        self.stdout.write("   💰 TOTALES:")
        self.stdout.write(f"      Total créditos: {total_credits}")
        self.stdout.write(f"      Créditos pendientes: {total_pending}")
        self.stdout.write(f"      Créditos completados: {total_completed}")
        self.stdout.write(f"      Monto total: ${total_amount:,.2f}")
        self.stdout.write(f"      Saldo pendiente total: ${total_pending_amount:,.2f}")
        self.stdout.write(f"      Total pagos: ${total_payments:,.2f}") 