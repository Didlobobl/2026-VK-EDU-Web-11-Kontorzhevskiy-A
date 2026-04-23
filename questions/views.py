from django.shortcuts import render
from core.utils import paginate

def generate_questions(count=50):
    return [
        {
            'id': i,
            'title': f'Заголовок вопроса №{i}',
            'text': f'Текст вопроса №{i}. Здесь должно быть подробное описание проблемы... ' * 2,
            'tags': ['python', 'django', 'web'],
            'answers_count': i % 5,
            'rating': i * 2,
            'author': f'user{i % 10 + 1}',
            'created_at': '2025-04-08 14:00',
        } for i in range(1, count + 1)
    ]

def generate_answers(question_id, count=30):
    return [
        {
            'id': i,
            'text': f'Текст ответа №{i} на вопрос {question_id}. Очень полезный и правильный совет! ' * 2,
            'author': f'answer_user{i % 5 + 1}',
            'rating': i * 3,
            'is_correct': i == 1,
            'created_at': '2025-04-08 15:00',
        } for i in range(1, count + 1)
    ]

def index(request):
    all_questions = generate_questions(100)
    page_obj = paginate(all_questions, request, per_page=10)
    return render(request, 'questions/index.html', {
        'questions': page_obj.object_list,
        'page_obj': page_obj,
    })

def hot(request):
    all_questions = generate_questions(100)
    hot_questions = sorted(all_questions, key=lambda x: x['rating'], reverse=True)
    page_obj = paginate(hot_questions, request, per_page=10)
    return render(request, 'questions/index.html', {
        'questions': page_obj.object_list,
        'page_obj': page_obj,
    })

def tag(request, tag_name):
    all_questions = generate_questions(100)
    tag_questions = [q for q in all_questions if tag_name in q['tags']]
    page_obj = paginate(tag_questions, request, per_page=10)
    return render(request, 'questions/tag.html', {
        'questions': page_obj.object_list,
        'page_obj': page_obj,
        'tag_name': tag_name,
    })

def question(request, question_id):
    all_questions = generate_questions(100)
    item = next((q for q in all_questions if q['id'] == question_id), None)
    if not item:
        item = all_questions[0]  # заглушка

    all_answers = generate_answers(question_id, count=30)
    answer_page = paginate(all_answers, request, per_page=10)

    return render(request, 'questions/question.html', {
        'question': item,
        'answers': answer_page.object_list,
        'answer_page_obj': answer_page,
    })

def ask(request):
    return render(request, 'questions/ask.html')