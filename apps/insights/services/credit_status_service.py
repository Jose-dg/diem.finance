"""
Service layer para la vista de estado de créditos.
Encapsula la lógica de filtrado, paginación y cálculo de KPIs.
"""
from datetime import date, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional

from django.core.paginator import Paginator
from django.db.models import Count, DecimalField, Q, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

import logging

from apps.fintech.models import Credit, Seller

logger = logging.getLogger(__name__)


class CreditStatusService:
    """
    Servicio para obtener el estado de créditos con filtros dinámicos
    y KPIs calculados en tiempo real sobre el mismo queryset filtrado.
    """

    # ------------------------------------------------------------------ #
    #  PUBLIC API                                                         #
    # ------------------------------------------------------------------ #

    @staticmethod
    def get_credit_status_data(
        date_from: date,
        date_to: date,
        seller_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """
        Punto de entrada principal.  Construye un único queryset filtrado
        y lo usa tanto para la tabla como para los KPIs.

        Args:
            date_from: Fecha inicio del periodo (inclusive).
            date_to:   Fecha fin del periodo (inclusive).
            seller_id: ID del vendedor (Seller.pk) — opcional.
            page:      Número de página para paginación.
            page_size: Registros por página (máx 100).

        Returns:
            Dict con keys: kpis, credits, pagination, available_sellers.
        """
        try:
            # 1. Un solo queryset base filtrado
            base_qs = CreditStatusService._build_base_queryset(
                date_from, date_to, seller_id
            )

            # 2. KPIs calculados sobre TODO el queryset filtrado (sin paginar)
            kpis = CreditStatusService._calculate_kpis(base_qs)

            # 3. Ordenar antes de paginar
            ordered_qs = base_qs.order_by('-created_at')

            # 4. Paginar
            paginator = Paginator(ordered_qs, page_size)
            page_obj = paginator.get_page(page)

            # 5. Serializar filas de la página actual
            credits_rows = CreditStatusService._build_table_rows(page_obj)

            # 6. Vendedores disponibles (para el dropdown del frontend)
            available_sellers = CreditStatusService.get_available_sellers(
                date_from, date_to
            )

            return {
                'kpis': kpis,
                'credits': credits_rows,
                'pagination': {
                    'current_page': page,
                    'total_pages': paginator.num_pages,
                    'total_count': paginator.count,
                    'page_size': page_size,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'next_page': (
                        page_obj.next_page_number() if page_obj.has_next() else None
                    ),
                    'previous_page': (
                        page_obj.previous_page_number()
                        if page_obj.has_previous()
                        else None
                    ),
                },
                'available_sellers': available_sellers,
            }

        except Exception as e:
            logger.error(f"Error in CreditStatusService.get_credit_status_data: {e}")
            return {}

    # ------------------------------------------------------------------ #
    #  QUERYSET CONSTRUCTION                                              #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _build_base_queryset(
        date_from: date,
        date_to: date,
        seller_id: Optional[int] = None,
    ):
        """
        Construye el queryset base optimizado con select_related
        y aplica los filtros de fecha y vendedor.
        """
        qs = Credit.objects.select_related(
            'user',
            'seller',
            'seller__user',
            'registered_by',
            'subcategory',
            'periodicity',
            'currency',
            'payment',
        ).filter(
            created_at__date__range=[date_from, date_to],
        )

        if seller_id is not None:
            qs = qs.filter(seller_id=seller_id)

        return qs

    # ------------------------------------------------------------------ #
    #  KPI AGGREGATION                                                    #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _calculate_kpis(queryset) -> Dict[str, Any]:
        """
        Calcula los KPIs sobre el queryset completo (sin paginar)
        usando un único .aggregate().

        KPIs:
        - ganancias_periodo  → Sum(earnings)
        - total_creditos     → Sum(price)
        - total_cobros       → Sum(total_abonos)
        - clientes_unicos    → Count(user, distinct=True)
        - estado_cuenta      → total_creditos − total_cobros
        - total_pendiente    → Sum(pending_amount)
        - cantidad_creditos  → Count(id)
        """
        try:
            zero = Decimal('0.00')
            agg = queryset.aggregate(
                ganancias_periodo=Coalesce(
                    Sum('earnings'), zero, output_field=DecimalField()
                ),
                total_creditos=Coalesce(
                    Sum('price'), zero, output_field=DecimalField()
                ),
                total_cobros=Coalesce(
                    Sum('total_abonos'), zero, output_field=DecimalField()
                ),
                total_pendiente=Coalesce(
                    Sum('pending_amount'), zero, output_field=DecimalField()
                ),
                clientes_unicos=Count('user', distinct=True),
                cantidad_creditos=Count('id'),
            )

            total_creditos = agg['total_creditos']
            total_cobros = agg['total_cobros']
            estado_cuenta = total_creditos - total_cobros

            return {
                'ganancias_periodo': float(agg['ganancias_periodo']),
                'total_creditos': float(total_creditos),
                'total_cobros': float(total_cobros),
                'total_pendiente': float(agg['total_pendiente']),
                'clientes_unicos': agg['clientes_unicos'],
                'cantidad_creditos': agg['cantidad_creditos'],
                'estado_cuenta': float(estado_cuenta),
            }

        except Exception as e:
            logger.error(f"Error calculating KPIs: {e}")
            return {
                'ganancias_periodo': 0.0,
                'total_creditos': 0.0,
                'total_cobros': 0.0,
                'total_pendiente': 0.0,
                'clientes_unicos': 0,
                'cantidad_creditos': 0,
                'estado_cuenta': 0.0,
            }

    # ------------------------------------------------------------------ #
    #  TABLE ROW SERIALIZATION                                            #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _build_table_rows(page_queryset) -> List[Dict[str, Any]]:
        """
        Serializa los créditos de la página actual en dicts planos
        aptos para JSON.  Aprovecha el select_related previo.
        """
        rows: List[Dict[str, Any]] = []

        for credit in page_queryset:
            percentage_paid = 0.0
            if credit.price and credit.price > 0:
                percentage_paid = float((credit.total_abonos / credit.price) * 100)

            seller_name = None
            if credit.seller and credit.seller.user:
                u = credit.seller.user
                seller_name = f"{u.first_name} {u.last_name}".strip() or u.username

            rows.append({
                'uid': str(credit.uid),
                'state': credit.state,
                'created_at': credit.created_at.isoformat(),
                # Usuario / cliente
                'user_id': credit.user.id,
                'user_full_name': (
                    f"{credit.user.first_name} {credit.user.last_name}".strip()
                    or credit.user.username
                ),
                'user_username': credit.user.username,
                # Vendedor
                'seller_id': credit.seller_id,
                'seller_name': seller_name,
                # Financieros
                'cost': float(credit.cost) if credit.cost else 0.0,
                'price': float(credit.price) if credit.price else 0.0,
                'earnings': float(credit.earnings) if credit.earnings else 0.0,
                'interest': float(credit.interest) if credit.interest else 0.0,
                'total_abonos': float(credit.total_abonos) if credit.total_abonos else 0.0,
                'pending_amount': float(credit.pending_amount) if credit.pending_amount else 0.0,
                'percentage_paid': round(percentage_paid, 2),
                # Fechas
                'first_date_payment': (
                    credit.first_date_payment.isoformat()
                    if credit.first_date_payment else None
                ),
                'second_date_payment': (
                    credit.second_date_payment.isoformat()
                    if credit.second_date_payment else None
                ),
                'credit_days': credit.credit_days or 0,
                # Morosidad
                'morosidad_level': credit.morosidad_level or 'on_time',
                'is_in_default': credit.is_in_default,
                # Categorización
                'subcategory_name': (
                    credit.subcategory.name if credit.subcategory else None
                ),
                'periodicity_name': (
                    credit.periodicity.name if credit.periodicity else None
                ),
                'currency': (
                    credit.currency.currency if credit.currency else 'COP'
                ),
            })

        return rows

    # ------------------------------------------------------------------ #
    #  UTILITIES                                                          #
    # ------------------------------------------------------------------ #

    @staticmethod
    def get_available_sellers(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retorna los vendedores que tienen créditos en el rango de fechas,
        útil para poblar el dropdown de filtro en el frontend.
        """
        try:
            qs = Credit.objects.select_related('seller', 'seller__user')

            if date_from and date_to:
                qs = qs.filter(created_at__date__range=[date_from, date_to])

            sellers_qs = (
                qs.exclude(seller__isnull=True)
                .values(
                    'seller__id',
                    'seller__user__id',
                    'seller__user__first_name',
                    'seller__user__last_name',
                    'seller__user__username',
                )
                .annotate(credits_count=Count('id'))
                .order_by('-credits_count')
            )

            sellers: List[Dict[str, Any]] = []
            for item in sellers_qs:
                first = item['seller__user__first_name'] or ''
                last = item['seller__user__last_name'] or ''
                full_name = f"{first} {last}".strip()
                if not full_name:
                    full_name = item['seller__user__username'] or f"Seller {item['seller__id']}"

                sellers.append({
                    'id': item['seller__id'],
                    'name': full_name,
                    'credits_count': item['credits_count'],
                })

            return sellers

        except Exception as e:
            logger.error(f"Error getting available sellers: {e}")
            return []
