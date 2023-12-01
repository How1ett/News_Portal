from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'text', 'author', 'mat_rating') # оставляем только имя и цену товара
    list_filter = ('author', 'mat_rating', 'time_create') # добавляем примитивные фильтры в нашу админку
    search_fields = ('mat_rating', 'author__user__username', 'time_create', 'title')  # тут всё очень похоже на фильтры из запросов в базу


class CommentsAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('text', 'post', 'user', 'time_create', 'com_rating') # оставляем только имя и цену товара
    list_filter = ('user', 'com_rating', 'time_create') # добавляем примитивные фильтры в нашу админку
    search_fields = ('com_rating', 'user__username', 'time_create', 'text')  # тут всё очень похоже на фильтры из запросов в базу


class AuthorAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('user', 'rating') # оставляем только имя и цену товара
    list_filter = ('user', 'rating') # добавляем примитивные фильтры в нашу админку
    search_fields = ('rating', 'user__username')  # тут всё очень похоже на фильтры из запросов в базу


class PostCategoryAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('post', 'category') # оставляем только имя и цену товара
    list_filter = ('category',) # добавляем примитивные фильтры в нашу админку
    search_fields = ('post__title', 'category__category')  # тут всё очень похоже на фильтры из запросов в базу


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(Author, AuthorAdmin)