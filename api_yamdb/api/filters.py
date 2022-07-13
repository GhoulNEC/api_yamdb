from django_filters import rest_framework

from reviews.models import Titles


class TitlesFilter(rest_framework.FilterSet):
    category = rest_framework.CharFilter(field_name='category__slug')
    genre = rest_framework.CharFilter(field_name='genre__slug')
    name = rest_framework.CharFilter(field_name='name',
                                     lookup_expr='icontains')
    year = rest_framework.NumberFilter(field_name='year')

    class Meta:
        model = Titles
        fields = ('genre', 'category', 'name', 'year')