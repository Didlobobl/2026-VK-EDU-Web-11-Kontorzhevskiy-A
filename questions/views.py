from django.db.models import Sum 
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Question, Tag, Answer, QuestionLike, AnswerLike
from questions.utils import paginate
from .forms import AskForm, AnswerForm

def index(request):
    questions_list = Question.objects.new_questions().select_related('author__profile').prefetch_related('tags')
    page_obj = paginate(questions_list, request, 20)
    return render(request, 'questions/index.html', {'questions': page_obj})

def hot(request):
    questions = Question.objects.hot_questions()
    page_obj = paginate(questions, request, 20)
    return render(request, 'questions/index.html', {'questions': page_obj})

def tag(request, tag_name):
    tag_obj = get_object_or_404(Tag, name=tag_name)
    
    questions_list = Question.objects.by_tag(tag_name)
    page_obj = paginate(questions_list, request, 20)
    return render(request, 'questions/tag.html', {
        'tag': tag_obj, 
        'questions': page_obj
    })
def question(request, question_id):
    item = get_object_or_404(Question.objects.select_related('author'), pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = item
            answer.save()
            return redirect(f"{reverse('questions:question', args=[item.id])}#answer-{answer.id}")
    else:
        form = AnswerForm()

    answers_list = item.answers.select_related('author__profile').order_by('-created_at')
    page_obj = paginate(answers_list, request, 30)
    return render(request, 'questions/question.html', {
        'question': item, 
        'answers': page_obj,
        'form': form  
    })

def ask(request):
    return render(request, 'questions/ask.html')

def answer(request, question_id):
    from django.shortcuts import redirect
    return redirect('questions:question', question_id=question_id)

def page_not_found(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

@login_required(login_url='core:login')
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save(user=request.user)
            return redirect('questions:question', question_id=question.id)
    else:
        form = AskForm()
    return render(request, 'questions/ask.html', {'form': form})

@login_required(login_url='core:login')
def answer(request, question_id):
    question_obj = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            ans = form.save(commit=False)
            ans.author = request.user
            ans.question = question_obj
            ans.save()
            
            return redirect(f"/question/{question_id}/#answer-{ans.id}")
            
    return redirect('questions:question', question_id=question_id)

@login_required
@require_POST
def vote(request):
    obj_id = request.POST.get('id')
    obj_type = request.POST.get('type') 
    action = request.POST.get('action') 
    
    new_value = 1 if action == 'like' else -1
    
    if obj_type == 'question':
        model = Question
        like_model = QuestionLike
        lookup_field = 'question'
    else:
        model = Answer
        like_model = AnswerLike
        lookup_field = 'answer'

    obj = get_object_or_404(model, pk=obj_id)
    
    like, created = like_model.objects.get_or_create(
        user=request.user,
        **{lookup_field: obj},
        defaults={'value': new_value}
    )
    is_active = True
    if not created:
        if like.value == new_value:
            like.delete()
            is_active = False
        else:
            like.value = new_value
            like.save()

    current_rating = like_model.objects.filter(**{lookup_field: obj}).aggregate(Sum('value'))['value__sum'] or 0
    obj.rating = current_rating
    obj.save()

    return JsonResponse({
        'status': 'ok',
        'new_rating': obj.rating, 
        'is_active': is_active
    })


@require_POST
@login_required
def mark_correct(request):
    answer_id = request.POST.get('answer_id')
    
    answer = get_object_or_404(Answer, pk=answer_id)
    question = answer.question

    if request.user != question.author:
        return JsonResponse({'message': 'Только автор вопроса может выбрать правильный ответ.'}, status=403)

    question.answers.all().update(is_correct=False)
    
    answer.is_correct = True
    answer.save()

    return JsonResponse({'status': 'ok'})