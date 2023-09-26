from django.urls import path
from .views import *


urlpatterns = [
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/search/', NewsSearch.as_view(), name='news_search'),
    path('news/create/', NewsCreate.as_view(), name='news_post'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

    path('articles/', ArticlesList.as_view(), name='articles_list'),
    path('articles/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_post'),
    path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),

    path('posts/', PostsList.as_view(), name='post_list'),
    path('posts/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('posts/create/', PostCreate.as_view(), name='create_post'),
    path('posts/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]