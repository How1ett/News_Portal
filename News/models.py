from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import pgettext_lazy
from django.core.cache import cache


# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rat_post = self.post_set.all().aggregate(Sum('mat_rating'))['mat_rating__sum'] * 3
        rat_comment = self.user.comment_set.all().aggregate(Sum('com_rating'))['com_rating__sum']
        sum_rating = 0
        for i in self.post_set.all().values('id'):
            sum_rating += Comment.objects.filter(post=i['id']).aggregate(Sum('com_rating'))['com_rating__sum']
        self.rating = rat_post + rat_comment + sum_rating
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    subscribe = models.ManyToManyField(User, through='CategorySubscribe', verbose_name=pgettext_lazy('subscriber', 'subscriber'))

    def __str__(self) -> str:
        return f'{self.category}'


class CategorySubscribe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name=pgettext_lazy('category', 'category'))
    subscriber = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=pgettext_lazy('subscriber', 'subscriber'))


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # 0 - новость, 1 - статья.
    type = models.BooleanField()
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=100)
    text = models.TextField()
    mat_rating = models.IntegerField(default=0)

    def like(self):
        self.mat_rating += 1
        self.save()

    def dislike(self):
        self.mat_rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

    def __str__(self):
        return f'{self.title} - {self.text[:128]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.category}{self.post}'




class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    com_rating = models.IntegerField(default=0)

    def like(self):
        self.com_rating += 1
        self.save()

    def dislike(self):
        self.com_rating -= 1
        self.save()

    def __str__(self) -> str:
        return f'{self.text}'
