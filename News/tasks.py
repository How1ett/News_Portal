from NewsPaper import settings
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from News.models import Post, Category


@shared_task
def weekly_email():
    today = timezone.now()
    day_week_ago = today - timezone.timedelta(days=7)
    posts = Post.objects.filter(time_create__gte=day_week_ago)
    categories = set(posts.values_list('category__category', flat=True))
    subscribers = set(Category.objects.filter(category__in=categories).values_list('subscribe__email', flat=True))

    html_content = render_to_string(
        'mail_posts_week.html',
        {
            'link': f'http://127.0.0.1:8000',
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject="Посты за неделю",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
