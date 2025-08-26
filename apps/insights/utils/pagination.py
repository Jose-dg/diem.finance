"""
Paginación personalizada para el dashboard de insights
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    """Paginación personalizada con información adicional"""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200
    page_query_param = 'page'
    
    def get_paginated_response(self, data):
        """Retorna respuesta paginada con información adicional"""
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page_info': {
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'page_size': self.page.paginator.per_page,
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous(),
            },
            'results': data
        })
    
    def get_page_size(self, request):
        """Obtiene el tamaño de página desde los parámetros de consulta"""
        page_size = request.query_params.get(self.page_size_query_param)
        if page_size:
            try:
                page_size = int(page_size)
                if page_size > 0 and page_size <= self.max_page_size:
                    return page_size
            except (ValueError, TypeError):
                pass
        return self.page_size
