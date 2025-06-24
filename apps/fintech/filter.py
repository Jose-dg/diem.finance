from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Credit

class CreditFilter(filters.FilterSet):
    # Campos del usuario (AbstractUser)
    first_name = filters.CharFilter(field_name="user__first_name", lookup_expr="icontains")
    last_name = filters.CharFilter(field_name="user__last_name",  lookup_expr="icontains")

    # PhoneNumber: el FK en User es phone_1, sin related_name
    phone_number = filters.CharFilter(field_name="user__phone_1__phone_number", lookup_expr="icontains")

    # Label: user.label tiene related_name default 'label'
    label = filters.CharFilter(field_name="user__label__name", lookup_expr="icontains")

    # Periodicity: FK a Periodicity
    periodicity_days = filters.NumberFilter(field_name="periodicity__days", lookup_expr="exact")
    periodicity_id = filters.UUIDFilter(  field_name="periodicity__id", lookup_expr="exact")

    # Estado del crédito
    is_in_default = filters.BooleanFilter(field_name="is_in_default")
    morosidad_level  = filters.CharFilter(  field_name="morosidad_level", lookup_expr="exact")
    state = filters.CharFilter(  field_name="state", lookup_expr="exact")

    # Búsqueda combinada (opcional)
    search = filters.CharFilter(method="filter_search", label="Search")

    class Meta:
        model  = Credit
        fields = [
            "first_name", "last_name", "phone_number",
            "label", "periodicity_days", "periodicity_id",
            "is_in_default", "morosidad_level", "state", "search",
        ]

    def filter_search(self, queryset, name, value):
        """
        Permite búsqueda de texto libre sobre varios campos a la vez.
        """
        return queryset.filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value)  |
            Q(user__label__name__icontains=value)|
            Q(description__icontains=value)
        )
