from django.contrib.auth.models import User
from questions.models import Tag
from django.db.models import Count

def sidebar_data(request):
    # Топ 20 популярных тегов (по количеству вопросов)
    popular_tags = Tag.objects.annotate(
        questions_count=Count('questions')
    ).order_by('-questions_count')[:20]

    best_members = User.objects.annotate(
        q_count=Count('question')
    ).order_by('-q_count')[:10]

    return {
        'popular_tags': popular_tags,
        'best_members': best_members,
    }