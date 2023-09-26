from django_filters import FilterSet, ModelChoiceFilter, DateFilter, CharFilter
from django.forms import DateInput
from .models import Post, User


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    author = ModelChoiceFilter(
        field_name='author_id__user',
        queryset=User.objects.filter(),
        label="Автор",
        empty_label="Все авторы",
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'title': ['icontains'],
            # количество товаров должно быть больше или равно
            'time_create': ['date'],
            'mat_rating': [
                'lt',  # цена должна быть меньше или равна указанной
                'gt',  # цена должна быть больше или равна указанной
            ],
        }


class NewsFilter(FilterSet):
    date = DateFilter(
        field_name='time_create',
        label='Дата (позже)',
        lookup_expr='gt',
        widget=DateInput(
            attrs={
                'type': 'date',
            }
        ),
    )
    title = CharFilter(
        field_name='title',
        label='Заголовок',
        lookup_expr='icontains',
    )
    author = CharFilter(
        field_name='author__user__username',
        label='Автор',
        lookup_expr='icontains',
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'author',
        ]
