from django.db.models import Q, Sum, Count
from rest_framework import status

from apps.fintech.models import User, Credit


class ClientService:
    """Service class for client-related business logic"""
    
    @staticmethod
    def normalize_document_number(document_number):
        """
        Normaliza el número de documento removiendo guiones, espacios y puntos
        """
        if not document_number:
            return ""
        # Remover guiones, espacios, puntos y otros caracteres especiales
        return ''.join(filter(str.isalnum, str(document_number)))
    
    @staticmethod
    def search_clients_by_criteria(document_number=None, first_name=None, last_name=None):
        """
        Busca clientes por criterios específicos con optimización de queries
        """
        try:
            # Construir filtros para buscar usuarios
            user_filters = Q()
            
            # Filtro por documento - normalizado automáticamente
            if document_number:
                normalized_document = ClientService.normalize_document_number(document_number)
                user_filters &= Q(document__document_number=normalized_document)
            
            # Filtros por nombre
            if first_name and last_name:
                user_filters &= Q(first_name__icontains=first_name) & Q(last_name__icontains=last_name)
            elif first_name:
                user_filters &= Q(first_name__icontains=first_name)
            elif last_name:
                user_filters &= Q(last_name__icontains=last_name)
            
            # Buscar usuarios que coincidan con los criterios con optimización
            users = User.objects.filter(user_filters).select_related(
                'document__document_type'
            ).prefetch_related(
                'credits__subcategory__category',
                'credits__currency',
                'credits__periodicity',
                'credits__installments',
                'credits__payments__payment_method',
                'credits__payments__currency',
                'credits__payments__transaction'
            )
            
            return users
            
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_client_credits_summary(user_ids):
        """
        Obtiene resumen de créditos para una lista de usuarios
        """
        try:
            # Consulta optimizada para créditos con agregaciones
            credits_data = Credit.objects.filter(
                user_id__in=user_ids
            ).select_related(
                'user__document__document_type',
                'subcategory__category',
                'currency',
                'periodicity'
            ).prefetch_related(
                'installments',
                'payments__payment_method',
                'payments__currency',
                'payments__transaction'
            ).order_by('-created_at')
            
            # Calcular totales usando agregaciones de base de datos
            totals = credits_data.aggregate(
                total_credits=Count('id'),
                total_pending=Sum('pending_amount'),
                total_paid=Sum('total_abonos')
            )
            
            # Calcular estadísticas por cliente usando agregaciones
            client_stats = credits_data.values('user_id').annotate(
                credits_count=Count('id'),
                total_pending=Sum('pending_amount'),
                total_paid=Sum('total_abonos')
            )
            
            # Crear diccionario para acceso rápido a estadísticas por cliente
            client_stats_dict = {
                stat['user_id']: {
                    'credits_count': stat['credits_count'],
                    'total_pending': float(stat['total_pending'] or 0),
                    'total_paid': float(stat['total_paid'] or 0)
                }
                for stat in client_stats
            }
            
            return credits_data, totals, client_stats_dict
            
        except Exception as e:
            return None, None, None, str(e)
    
    @staticmethod
    def format_client_credits_response(users, credits_data, totals, client_stats_dict):
        """
        Formatea la respuesta de créditos de clientes
        """
        try:
            if not users.exists():
                return {
                    'message': 'No se encontraron clientes con los criterios proporcionados',
                    'credits': [],
                    'total_credits': 0,
                    'total_pending': 0,
                    'total_paid': 0
                }
            
            # Información de los clientes encontrados
            clients_info = []
            for user in users:
                user_stats = client_stats_dict.get(user.id, {
                    'credits_count': 0,
                    'total_pending': 0,
                    'total_paid': 0
                })
                
                clients_info.append({
                    'user_id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'document_type': user.document.document_type.description if user.document else None,
                    'document_number': user.document.document_number if user.document else None,
                    'credits_count': user_stats['credits_count'],
                    'total_pending': user_stats['total_pending'],
                    'total_paid': user_stats['total_paid']
                })
            
            # Serializar créditos
            from apps.fintech.serializers import CreditSerializer
            credits_serializer = CreditSerializer(credits_data, many=True)
            
            return {
                'message': f'Se encontraron {len(clients_info)} cliente(s)',
                'clients': clients_info,
                'credits': credits_serializer.data,
                'total_credits': totals['total_credits'] or 0,
                'total_pending': float(totals['total_pending'] or 0),
                'total_paid': float(totals['total_paid'] or 0)
            }
            
        except Exception as e:
            return None, str(e) 