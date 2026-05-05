from django.urls import path
from questions import views

app_name = 'questions'  

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot_questions'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('question/<int:question_id>/answer/', views.answer, name='answer'),
    path('vote/', views.vote, name='vote'),
    path('answer/<int:answer_id>/correct/', views.mark_correct, name='mark_correct'),
]