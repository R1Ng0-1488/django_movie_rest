from django_filters import rest_framework as filters
from .models import Movies


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        print("this is ip if ",ip)
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class MoviesFilter(filters.FilterSet):
    genres = CharFilterInFilter(field_name='genre__name', lookup_expr='in')
    year = filters.RangeFilter()

    class Meta:
        model = Movies
        fields = ['genres', 'year']
