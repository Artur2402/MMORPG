from django.contrib.auth.models import User
from django.forms import DateInput
from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateTimeFilter
from .models import Post


class PostFilter(FilterSet):
    author = ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all(),
        lookup_expr='exact',
        label='Автор',
        empty_label='all'
    )

    title = CharFilter(
        lookup_expr='icontains',
        label='Объявление содержит',
    )

    date = DateTimeFilter(
        lookup_expr='gt',
        label='Опубликовано с',
        widget=DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'},
        )
    )

    class Meta:
        model = Post
        fields = {
            'category': ['exact'],
        }