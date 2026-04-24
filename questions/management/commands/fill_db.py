import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from questions.models import Question, Answer, Tag, QuestionLike, AnswerLike
from core.models import Profile
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент заполнения')

    def handle(self, *args, **options):
        ratio = options['ratio']
        
        self.stdout.write('Генерация тегов...')
        tags = [Tag(name=fake.unique.word() + str(i)) for i in range(ratio)]
        Tag.objects.bulk_create(tags)
        tags = list(Tag.objects.all())

        self.stdout.write('Генерация пользователей...')
        users_to_create = []
        for i in range(ratio):
            users_to_create.append(User(
                username=f'{fake.unique.user_name()}_{random.randint(1, 100000)}',
                email=fake.unique.email(),
                password='password123'
            ))
        
        new_users = User.objects.bulk_create(users_to_create)

        profiles = [Profile(user=u) for u in new_users]
        Profile.objects.bulk_create(profiles, ignore_conflicts=True)
        
        users = list(User.objects.all())

        self.stdout.write('Генерация вопросов...')
        questions = []
        for i in range(ratio * 10):
            questions.append(Question(
                title=fake.sentence()[:50],
                text=fake.text(max_nb_chars=200),
                author=random.choice(users),
            ))
        Question.objects.bulk_create(questions)
        questions = list(Question.objects.all())

        self.stdout.write('Привязка тегов...')
        QuestionTagRel = Question.tags.through
        relations = []
        for q in questions:
            chosen_tags = random.sample(tags, random.randint(1, 3))
            for t in chosen_tags:
                relations.append(QuestionTagRel(question_id=q.id, tag_id=t.id))
        QuestionTagRel.objects.bulk_create(relations, ignore_conflicts=True)

        self.stdout.write('Генерация ответов...')
        answers = []
        for _ in range(ratio * 100):
            answers.append(Answer(
                text=fake.text(max_nb_chars=100),
                question=random.choice(questions),
                author=random.choice(users),
                is_correct=random.choice([True, False, False, False])
            ))
            if len(answers) >= 10000:
                Answer.objects.bulk_create(answers)
                answers = []
        Answer.objects.bulk_create(answers)

        self.stdout.write('Генерация лайков...')
        likes = []
        for _ in range(ratio * 200):
            likes.append(QuestionLike(
                user=random.choice(users),
                question=random.choice(questions)
            ))
            if len(likes) >= 10000:
                QuestionLike.objects.bulk_create(likes, ignore_conflicts=True)
                likes = []
        QuestionLike.objects.bulk_create(likes, ignore_conflicts=True)

        
        self.stdout.write('Генерация лайков к ответам...')

        answer_ids = list(Answer.objects.values_list('id', flat=True)[:100000])
        
        answer_likes = []
        for _ in range(ratio * 100): # Распределяем лайки
            answer_likes.append(AnswerLike(
                user=random.choice(users),
                answer_id=random.choice(answer_ids)
            ))
            if len(answer_likes) >= 10000:
                AnswerLike.objects.bulk_create(answer_likes, ignore_conflicts=True)
                answer_likes = []
        AnswerLike.objects.bulk_create(answer_likes, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'База успешно заполнена (ratio={ratio})'))