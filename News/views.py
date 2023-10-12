from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Category, CategorySubscribe, User
from .filters import PostFilter, NewsFilter
from .forms import PostForm, NewsForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from NewsPaper import settings
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.utils import timezone


# from django.shortcuts import render
# from django.http import HttpResponse, HttpResponseRedirect

class PostsList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    # Переопределяем функцию получения списка постов
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        user = post.author
        time = timezone.now()
        posts_24_hours = time - timezone.timedelta(days=1)
        posts_count = Post.objects.filter(author=user, time_create__gte=posts_24_hours).count()
        if posts_count >= 3:
            return HttpResponseBadRequest(f'{post.author}, Вы создали больше трёх постов за сутки, лимит превышен.')
        else:
            post.save()

            post_category_pk = self.request.POST['category']
            sub_text = self.request.POST.get('text')
            sub_title = self.request.POST.get('title')
            post_category = Category.objects.get(pk=post_category_pk)
            subscribers = post_category.subscribe.all()

            for subscriber in subscribers:
                html_content = render_to_string(
                    'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': post, 'title': sub_title}
                )
                msg = EmailMultiAlternatives(
                    subject=sub_title,
                    body=f'{sub_text[:50]}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            return super().form_valid(form)
            # return redirect('/posts/')



class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('News.change_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class NewsList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    # Переопределяем функцию получения списка постов
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = Post.objects.filter(type=0)
        # queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post',)
    form_class = NewsForm
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = False
        user = post.author
        time = timezone.now()
        posts_24_hours = time - timezone.timedelta(days=1)
        posts_count = Post.objects.filter(author=user, time_create__gte=posts_24_hours).count()
        if posts_count >= 3:
            return HttpResponseBadRequest(f'{post.author}, Вы создали больше трёх постов за сутки, лимит превышен.')
        else:
            post.save()

            post_category_pk = self.request.POST['category']
            sub_text = self.request.POST.get('text')
            sub_title = self.request.POST.get('title')
            post_category = Category.objects.get(pk=post_category_pk)
            subscribers = post_category.subscribe.all()


            for subscriber in subscribers:
                html_content = render_to_string(
                    'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': post, 'title': sub_title}
                )
                msg = EmailMultiAlternatives(
                    subject=sub_title,
                    body=f'{sub_text[:50]}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            return super().form_valid(form)
            # return redirect('/news/')



class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('News.change_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    ordering = ['-time_create']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ArticlesList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    # Переопределяем функцию получения списка постов
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = Post.objects.filter(type=1)
        # queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class ArticlesCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post',)
    form_class = NewsForm
    template_name = 'articles_edit.html'


    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 1
        user = post.author
        time = timezone.now()
        posts_24_hours = time - timezone.timedelta(days=1)
        posts_count = Post.objects.filter(author=user, time_create__gte=posts_24_hours).count()
        if posts_count >= 3:
            return HttpResponseBadRequest(f'{post.author}, Вы создали больше трёх постов за сутки, лимит превышен.')
        else:
            post.save()

            post_category_pk = self.request.POST['category']
            sub_text = self.request.POST.get('text')
            sub_title = self.request.POST.get('title')
            post_category = Category.objects.get(pk=post_category_pk)
            subscribers = post_category.subscribe.all()

            for subscriber in subscribers:
                html_content = render_to_string(
                    'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': post, 'title': sub_title}
                )
                msg = EmailMultiAlternatives(
                    subject=sub_title,
                    body=f'{sub_text[:50]}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            return super().form_valid(form)
            # return redirect('/articles/')


class ArticlesUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'articles_edit.html'


class ArticlesDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('News.change_post',)
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('articles_list')


class CategoryPost(DetailView):
    model = Category
    template_name = 'post_category.html'
    context_object_name = 'postcategory'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(category=kwargs['object'])
        context['is_not_categorys'] = not CategorySubscribe.objects.filter(category=self.kwargs['pk'], subscriber=self.request.user.id).exists()

        return context


# Добавление категории:
class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'


# Список категорий:
class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'category'


class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# @login_required
# def subscribe_me(request):
#     user = request.user
#     category = Category.objects.get(id=pk)
#     category.subscribers.add(user)
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def subscribe_to_category(request, pk):
    user = request.user
    if not CategorySubscribe.objects.filter(category=pk, subscriber=user.id).exists():
        CategorySubscribe.objects.create(category=Category.objects.get(pk=pk), subscriber=User.objects.get(pk=user.id))


    # current_user = request.user
    # CategorySubscribe.objects.create(category=Category.objects.get(pk=pk),
    #                                  subscriber=User.objects.get(pk=current_user.id))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
