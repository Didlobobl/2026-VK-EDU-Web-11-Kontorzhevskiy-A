from django.contrib import admin
from .models import Question, Answer, Tag, QuestionLike, AnswerLike

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1 

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at') 
    list_filter = ('created_at', 'tags') 
    search_fields = ('title', 'text') 
    inlines = [AnswerInline] 

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'author', 'is_correct', 'created_at')
    list_filter = ('is_correct',)

# Остальные модели регистрируем просто
admin.site.register(Tag)
admin.site.register(QuestionLike)
admin.site.register(AnswerLike)