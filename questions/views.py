from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Question, Tag, Answer
from questions.utils import paginate
from .forms import AskForm, AnswerForm

def index(request):
    questions_list = Question.objects.new_questions()
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
    answers_list = item.answers.select_related('author').all() 
    page_obj = paginate(answers_list, request, 5)
    return render(request, 'questions/question.html', {'question': item, 'answers': page_obj})

def ask(request):
    return render(request, 'questions/ask.html')

def answer(request, question_id):
    from django.shortcuts import redirect
    return redirect('questions:question', question_id=question_id)

def page_not_found(request, exception):
    return render(request, '404.html', status=404)

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