from django.core.management.base import BaseCommand
from django.db.models import Count, Sum, Q
from apps.fintech.models import User, Credit
from decimal import Decimal

class Command(BaseCommand):
    help = 'Muestra detalle de créditos por usuario individual'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Mostrar solo un usuario específico'
        )
        parser.add_argument(
            '--only-with-credits',
            action='store_true',
            help='Mostrar solo usuarios con créditos'
        )
        parser.add_argument(
            '--format',
            choices=['simple', 'detailed', 'table'],
            default='simple',
            help='Formato de salida (default: simple)'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Número de usuarios por lote (default: 100)'
        )
        parser.add_argument(
            '--page',
            type=int,
            default=1,
            help='Página a mostrar (default: 1)'
        )

    def handle(self, *args, **options):
        specific_user = options['user']
        only_with_credits = options['only_with_credits']
        output_format = options['format']
        batch_size = options['batch_size']
        page = options['page']
        
        self.stdout.write("👤 DETALLE DE CRÉDITOS POR USUARIO")
        self.stdout.write("=" * 60)
        
        # Query optimizada para obtener usuarios con estadísticas de créditos
        users_query = User.objects.annotate(
            total_credits=Count('credits'),
            pending_credits=Count('credits', filter=Q(credits__state='pending')),
            completed_credits=Count('credits', filter=Q(credits__state='completed')),
            total_amount=Sum('credits__price'),
            total_pending_amount=Sum('credits__pending_amount'),
            total_payments=Sum('credits__total_abonos'),
            # Créditos por estado
            on_time_credits=Count('credits', filter=Q(credits__morosidad_level='on_time')),
            moderate_default_credits=Count('credits', filter=Q(credits__morosidad_level='moderate_default')),
            critical_default_credits=Count('credits', filter=Q(credits__morosidad_level='critical_default'))
        ).order_by('username')
        
        if specific_user:
            users_query = users_query.filter(username=specific_user)
        
        if only_with_credits:
            users_query = users_query.filter(total_credits__gt=0)
        
        # Calcular total de usuarios y páginas
        total_users = users_query.count()
        total_pages = (total_users + batch_size - 1) // batch_size
        
        self.stdout.write(f"📊 TOTAL DE USUARIOS: {total_users}")
        self.stdout.write(f"📄 PÁGINA: {page} de {total_pages}")
        self.stdout.write(f"📦 USUARIOS POR LOTE: {batch_size}")
        self.stdout.write("")
        
        # Calcular offset para la página
        offset = (page - 1) * batch_size
        users = list(users_query[offset:offset + batch_size])
        
        if not users:
            self.stdout.write("❌ No se encontraron usuarios que cumplan los criterios")
            return
        
        # Mostrar información de paginación
        start_user = offset + 1
        end_user = min(offset + batch_size, total_users)
        self.stdout.write(f"📋 Mostrando usuarios {start_user} a {end_user} de {total_users}")
        self.stdout.write("")
        
        if output_format == 'table':
            self._print_table_format(users)
        elif output_format == 'detailed':
            self._print_detailed_format(users)
        else:
            self._print_simple_format(users)
        
        # Estadísticas del lote actual
        self._print_batch_statistics(users, page, total_pages)
        
        # Estadísticas generales solo en la primera página
        if page == 1:
            self._print_general_statistics(users_query)
        
        self.stdout.write("")
        self.stdout.write("✅ ANÁLISIS COMPLETADO")
        
        # Mostrar comandos para navegar
        if total_pages > 1:
            self.stdout.write("")
            self.stdout.write("🔄 COMANDOS PARA NAVEGAR:")
            if page > 1:
                self.stdout.write(f"   Página anterior: --page {page-1}")
            if page < total_pages:
                self.stdout.write(f"   Página siguiente: --page {page+1}")
            self.stdout.write(f"   Primera página: --page 1")
            self.stdout.write(f"   Última página: --page {total_pages}")

    def _print_simple_format(self, users):
        """Imprime en formato simple y claro"""
        for i, user in enumerate(users, 1):
            self.stdout.write(f"{i:2d}. {user.username}")
            
            if user.total_credits > 0:
                self.stdout.write(f"     📊 Total créditos realizados: {user.total_credits}")
                self.stdout.write(f"     ⏳ Créditos con saldo pendiente: {user.pending_credits}")
                self.stdout.write(f"     ✅ Créditos completados: {user.completed_credits}")
                self.stdout.write(f"     💰 Monto total de créditos: ${user.total_amount or 0:,.2f}")
                self.stdout.write(f"     💸 Saldo pendiente total: ${user.total_pending_amount or 0:,.2f}")
                self.stdout.write(f"     💳 Total pagos realizados: ${user.total_payments or 0:,.2f}")
                
                # Estados de mora
                if user.on_time_credits > 0 or user.moderate_default_credits > 0 or user.critical_default_credits > 0:
                    self.stdout.write(f"     📈 Estados de mora:")
                    if user.on_time_credits > 0:
                        self.stdout.write(f"        ✅ Al día: {user.on_time_credits}")
                    if user.moderate_default_credits > 0:
                        self.stdout.write(f"        ⚠️  Mora moderada: {user.moderate_default_credits}")
                    if user.critical_default_credits > 0:
                        self.stdout.write(f"        🔴 Mora crítica: {user.critical_default_credits}")
            else:
                self.stdout.write(f"     ❌ Sin créditos registrados")
            
            self.stdout.write("")

    def _print_detailed_format(self, users):
        """Imprime en formato detallado"""
        for i, user in enumerate(users, 1):
            self.stdout.write(f"{i:2d}. {user.username}")
            self.stdout.write(f"     📧 Email: {user.email}")
            self.stdout.write(f"     📅 Fecha registro: {user.date_joined.strftime('%Y-%m-%d %H:%M')}")
            self.stdout.write(f"     👤 Nombre: {user.first_name or 'N/A'} {user.last_name or 'N/A'}")
            self.stdout.write(f"     🔐 Activo: {'Sí' if user.is_active else 'No'}")
            
            if user.total_credits > 0:
                self.stdout.write(f"     📊 ESTADÍSTICAS DE CRÉDITOS:")
                self.stdout.write(f"        • Total créditos realizados: {user.total_credits}")
                self.stdout.write(f"        • Créditos con saldo pendiente: {user.pending_credits}")
                self.stdout.write(f"        • Créditos completados: {user.completed_credits}")
                self.stdout.write(f"        • Monto total de créditos: ${user.total_amount or 0:,.2f}")
                self.stdout.write(f"        • Saldo pendiente total: ${user.total_pending_amount or 0:,.2f}")
                self.stdout.write(f"        • Total pagos realizados: ${user.total_payments or 0:,.2f}")
                
                # Porcentajes
                if user.total_credits > 0:
                    pending_percent = (user.pending_credits / user.total_credits) * 100
                    completed_percent = (user.completed_credits / user.total_credits) * 100
                    self.stdout.write(f"        • % Pendientes: {pending_percent:.1f}%")
                    self.stdout.write(f"        • % Completados: {completed_percent:.1f}%")
                
                # Estados de mora
                self.stdout.write(f"     📈 ESTADOS DE MORA:")
                self.stdout.write(f"        • Al día: {user.on_time_credits}")
                self.stdout.write(f"        • Mora moderada: {user.moderate_default_credits}")
                self.stdout.write(f"        • Mora crítica: {user.critical_default_credits}")
                
                # Mostrar créditos individuales si son pocos
                if user.total_credits <= 15:
                    credits = user.credits.all().order_by('-created_at')
                    self.stdout.write(f"     📋 CRÉDITOS INDIVIDUALES:")
                    for credit in credits:
                        status_icon = "⏳" if credit.state == 'pending' else "✅"
                        mora_icon = "✅" if credit.morosidad_level == 'on_time' else "⚠️" if credit.morosidad_level == 'moderate_default' else "🔴"
                        self.stdout.write(f"        {status_icon} {mora_icon} {credit.uid[:8]}... - ${credit.price:,.2f} ({credit.state}) - {credit.morosidad_level}")
            else:
                self.stdout.write(f"     ❌ Sin créditos registrados")
            
            self.stdout.write("")

    def _print_table_format(self, users):
        """Imprime en formato tabla"""
        self.stdout.write("📋 TABLA DE USUARIOS Y CRÉDITOS:")
        self.stdout.write("-" * 140)
        self.stdout.write(f"{'Usuario':<15} {'Total':<8} {'Pend.':<8} {'Comp.':<8} {'Monto Total':<15} {'Saldo Pend.':<15} {'Al Día':<8} {'Mora Mod.':<10} {'Mora Crit.':<12}")
        self.stdout.write("-" * 140)
        
        for user in users:
            self.stdout.write(
                f"{user.username:<15} "
                f"{user.total_credits:<8} "
                f"{user.pending_credits:<8} "
                f"{user.completed_credits:<8} "
                f"${user.total_amount or 0:<14,.2f} "
                f"${user.total_pending_amount or 0:<14,.2f} "
                f"{user.on_time_credits:<8} "
                f"{user.moderate_default_credits:<10} "
                f"{user.critical_default_credits:<12}"
            )

    def _print_batch_statistics(self, users, page, total_pages):
        """Imprime estadísticas del lote actual"""
        users_with_credits = [u for u in users if u.total_credits > 0]
        
        if not users_with_credits:
            return
        
        self.stdout.write("")
        self.stdout.write(f"📊 ESTADÍSTICAS DEL LOTE {page}:")
        
        # Totales del lote
        total_credits = sum(user.total_credits for user in users_with_credits)
        total_pending = sum(user.pending_credits for user in users_with_credits)
        total_completed = sum(user.completed_credits for user in users_with_credits)
        total_amount = sum(user.total_amount or 0 for user in users_with_credits)
        total_pending_amount = sum(user.total_pending_amount or 0 for user in users_with_credits)
        total_payments = sum(user.total_payments or 0 for user in users_with_credits)
        
        self.stdout.write(f"   💰 TOTALES DEL LOTE:")
        self.stdout.write(f"      • Usuarios con créditos: {len(users_with_credits)}")
        self.stdout.write(f"      • Total créditos: {total_credits}")
        self.stdout.write(f"      • Créditos pendientes: {total_pending}")
        self.stdout.write(f"      • Créditos completados: {total_completed}")
        self.stdout.write(f"      • Monto total: ${total_amount:,.2f}")
        self.stdout.write(f"      • Saldo pendiente: ${total_pending_amount:,.2f}")
        self.stdout.write(f"      • Total pagos: ${total_payments:,.2f}")
        
        # Promedios del lote
        if users_with_credits:
            avg_credits = total_credits / len(users_with_credits)
            avg_amount = total_amount / len(users_with_credits)
            self.stdout.write(f"   📊 PROMEDIOS DEL LOTE:")
            self.stdout.write(f"      • Promedio créditos por usuario: {avg_credits:.1f}")
            self.stdout.write(f"      • Promedio monto por usuario: ${avg_amount:,.2f}")

    def _print_general_statistics(self, users_query):
        """Imprime estadísticas generales"""
        users_with_credits = users_query.filter(total_credits__gt=0)
        total_users_with_credits = users_with_credits.count()
        
        if not total_users_with_credits:
            return
        
        self.stdout.write("")
        self.stdout.write("📈 ESTADÍSTICAS GENERALES (TODOS LOS USUARIOS):")
        
        # Totales generales
        total_credits = sum(user.total_credits for user in users_with_credits)
        total_pending = sum(user.pending_credits for user in users_with_credits)
        total_completed = sum(user.completed_credits for user in users_with_credits)
        total_amount = sum(user.total_amount or 0 for user in users_with_credits)
        total_pending_amount = sum(user.total_pending_amount or 0 for user in users_with_credits)
        total_payments = sum(user.total_payments or 0 for user in users_with_credits)
        
        self.stdout.write(f"   💰 TOTALES GENERALES:")
        self.stdout.write(f"      • Usuarios con créditos: {total_users_with_credits}")
        self.stdout.write(f"      • Total créditos: {total_credits}")
        self.stdout.write(f"      • Créditos pendientes: {total_pending}")
        self.stdout.write(f"      • Créditos completados: {total_completed}")
        self.stdout.write(f"      • Monto total: ${total_amount:,.2f}")
        self.stdout.write(f"      • Saldo pendiente: ${total_pending_amount:,.2f}")
        self.stdout.write(f"      • Total pagos: ${total_payments:,.2f}")
        
        # Promedios generales
        if total_users_with_credits:
            avg_credits = total_credits / total_users_with_credits
            avg_amount = total_amount / total_users_with_credits
            self.stdout.write(f"   📊 PROMEDIOS GENERALES:")
            self.stdout.write(f"      • Promedio créditos por usuario: {avg_credits:.1f}")
            self.stdout.write(f"      • Promedio monto por usuario: ${avg_amount:,.2f}")
        
        # Top usuarios generales
        top_by_credits = users_with_credits.order_by('-total_credits')[:3]
        self.stdout.write(f"   🏆 TOP 3 USUARIOS CON MÁS CRÉDITOS:")
        for i, user in enumerate(top_by_credits, 1):
            self.stdout.write(f"      {i}. {user.username}: {user.total_credits} créditos")
        
        # Usuarios con más saldo pendiente
        top_by_pending = users_with_credits.order_by('-total_pending_amount')[:3]
        self.stdout.write(f"   💸 TOP 3 USUARIOS CON MÁS SALDO PENDIENTE:")
        for i, user in enumerate(top_by_pending, 1):
            self.stdout.write(f"      {i}. {user.username}: ${user.total_pending_amount or 0:,.2f}") 