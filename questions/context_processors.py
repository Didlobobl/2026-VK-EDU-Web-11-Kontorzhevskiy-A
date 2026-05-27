from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.contrib.auth.models import User
from .models import Tag

def sidebar_data(request):
    tags = cache.get('popular_tags_cache')
    if tags is None:
        three_months = timezone.now() - timedelta(days=90)
        qs_tags = Tag.objects.filter(questions__created_at__gte=three_months)\
                    .annotate(q_count=Count('questions')).order_by('-q_count')[:10]
        tags = list(qs_tags.values('name', 'id'))
        cache.set('popular_tags_cache', tags, 3600)

    members = cache.get('best_members_cache')
    if members is None:
        last_week = timezone.now() - timedelta(days=7)
        qs_users = User.objects.filter(question__created_at__gte=last_week)\
                    .annotate(activity=Count('question')).order_by('-activity')[:10]
        members = list(qs_users.values('username', 'id'))
        cache.set('best_members_cache', members, 3600)

    return {'popular_tags': tags, 'best_members': members}