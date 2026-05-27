import requests
from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Tag, Question

@shared_task(name='questions.tasks.update_sidebar_cache')
def update_sidebar_cache():
    three_months = timezone.now() - timedelta(days=90)
    tags = Tag.objects.filter(questions__created_at__gte=three_months)\
              .annotate(q_count=Count('questions')).order_by('-q_count')[:10]
    cache.set('popular_tags_cache', list(tags.values('name', 'id')), 3600)

    last_week = timezone.now() - timedelta(days=7)
    users = User.objects.filter(question__created_at__gte=last_week)\
                .annotate(activity=Count('question')).order_by('-activity')[:10]
    cache.set('best_members_cache', list(users.values('username', 'id')), 3600)

@shared_task(name='questions.tasks.send_new_answer_email')
def send_new_answer_email(question_title, author_email, question_url):
    send_mail(
        f"Новый ответ: {question_title}",
        f"На ваш вопрос ответили! Посмотреть: {question_url}",
        settings.DEFAULT_FROM_EMAIL,
        [author_email]
    )

@shared_task(name='questions.tasks.notify_centrifugo')
def notify_centrifugo(question_id, data):
    channel = f"public:question_{question_id}" 
    command = {"method": "publish", "params": {"channel": channel, "data": data}}
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'apikey {settings.CENTRIFUGO_API_KEY}'
    }
    requests.post("http://centrifugo:8000/api", json=command, headers=headers)