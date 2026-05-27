from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum

class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('-created_at')

    def hot_questions(self):
         return self.get_with_related().annotate(count_likes=Count('likes', distinct=True)).order_by('-count_likes')
    
    def by_tag(self, tag_name):
        return self.get_with_related().filter(tags__name=tag_name)
    
    def get_with_related(self):
        qs = self.select_related('author__profile').prefetch_related('tags')
        qs = qs.annotate(answers_count=Count('answers', distinct=True))
        return qs
    
class Tag(models.Model):
    name = models.SlugField(max_length=50, unique=True, verbose_name="Имя тега")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    text = models.TextField(max_length=5000, verbose_name="Текст вопроса")
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    tags = models.ManyToManyField('questions.Tag', related_name='questions', verbose_name="Теги")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    objects = QuestionManager()

    def __str__(self):
        return self.title
    
    def get_rating(self):
        result = self.likes.aggregate(total=Sum('value'))['total']
        return result if result is not None else 0

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    text = models.TextField(max_length=10000, verbose_name="Текст ответа")
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, related_name='answers', verbose_name="Вопрос")
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Ответ от {self.author.username} к {self.question.title}"
    
    def get_rating(self):
        result = self.likes.aggregate(total=Sum('value'))['total']
        return result if result is not None else 0

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class QuestionLike(models.Model):
    VALUE_CHOICES = [(1, 'Like'), (-1, 'Dislike')]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')
    value = models.SmallIntegerField(default=1, verbose_name="Голос")

    class Meta:
        unique_together = ('user', 'question') 

class AnswerLike(models.Model):
    VALUE_CHOICES = [(1, 'Like'), (-1, 'Dislike')]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')
    value = models.SmallIntegerField(default=1, verbose_name="Голос")
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