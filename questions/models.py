from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('-created_at')

    def hot_questions(self):
        # Считаем количество лайков и сортируем
        return self.annotate(likes_count=Count('likes')).order_by('-likes_count')
    
    def by_tag(self, tag_name):
        return self.filter(tags__name=tag_name)
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Имя тега")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст вопроса")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    tags = models.ManyToManyField(Tag, related_name='questions', verbose_name="Теги")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    # Подключаем наш менеджер
    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    text = models.TextField(verbose_name="Текст ответа")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name="Вопрос")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Ответ от {self.author.username} к {self.question.title}"

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'question') 

class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'answer')

class QuestionManager(models.Manager):
    def get_with_related(self):
        return self.select_related('author').prefetch_related('tags')

    def new_questions(self):
        return self.get_with_related().order_by('-created_at')

    def hot_questions(self):
        return self.get_with_related().annotate(count_likes=Count('likes')).order_by('-count_likes')

    def by_tag(self, tag_name):
        return self.get_with_related().filter(tags__name=tag_name)