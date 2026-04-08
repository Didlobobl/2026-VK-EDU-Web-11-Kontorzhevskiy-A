from django.shortcuts import render
from core.utils import paginate 

QUESTIONS = [
    {
        'id': i,
        'title': f'Заголовок вопроса №{i}',
        'content': f'Текст вопроса №{i}. Здесь должно быть подробное описание проблемы...',
        'tags': ['python', 'django', 'web'],
        'answers_count': i % 5,
        'likes': i * 2,
    } for i in range(1, 50)  
]

ANSWERS = [
    {
        'id': i,
        'content': f'Текст ответа №{i}. Очень полезный и правильный совет!',
        'is_correct': i == 1, 
    } for i in range(1, 10)
]


def index(request):
    all_questions = [{'id': i, 'title': f'Вопрос {i}', 'text': 'Очень интересный вопрос'} for i in range(1, 101)]
    page_obj = paginate(all_questions, request, per_page=10)
    return render(request, 'questions/index.html', {
        'questions': page_obj.object_list,
        'page_obj': page_obj,
    })

def hot(request):
    hot_questions = sorted(QUESTIONS, key=lambda x: x['likes'], reverse=True)
    return render(request, 'questions/index.html', {'questions': hot_questions})

def tag(request, tag_name):
    tag_questions = [q for q in QUESTIONS if tag_name in q['tags']]
    return render(request, 'questions/tag.html', {
        'tag_name': tag_name,
        'questions': tag_questions
    })

def question(request, question_id):
    item = QUESTIONS[question_id - 1] 
    return render(request, 'questions/question.html', {
        'question': item,
        'answers': ANSWERS
    })

def ask(request):
    return render(request, 'questions/ask.html')