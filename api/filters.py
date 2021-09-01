from django_filters import rest_framework as dfilters

from .models import Title


class TitleFilter(dfilters.FilterSet):
    genre = dfilters.CharFilter(field_name='genre__slug',)
    category = dfilters.CharFilter(field_name='category__slug',)
    name = dfilters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year',)
