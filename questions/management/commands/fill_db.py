import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from questions.models import Question, Answer, Tag, QuestionLike, AnswerLike
from core.models import Profile
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными'
    Tag.objects.get_or_create(name='python')
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент заполнения')

    def handle(self, *args, **options):
        ratio = options['ratio']
        
        self.stdout.write('Генерация тегов...')
        tags = [Tag(name=f"{fake.word()}_{i}_{random.randint(1,1000)}") for i in range(ratio)]
        Tag.objects.bulk_create(tags, ignore_conflicts=True)
        tags = list(Tag.objects.all())

        self.stdout.write('Генерация пользователей...')
        users_to_create = []
        for i in range(ratio):
            users_to_create.append(User(
                username=f'{fake.unique.user_name()}_{i}',
                email=fake.unique.email(),
                password='password123'
            ))
        new_users = User.objects.bulk_create(users_to_create)
        
        profiles = [Profile(user=u) for u in new_users]
        Profile.objects.bulk_create(profiles, ignore_conflicts=True)
        users = list(User.objects.all())

        self.stdout.write('Генерация вопросов...')
        questions_to_create = []
        for i in range(ratio * 10):
            questions_to_create.append(Question(
                title=fake.sentence()[:50],
                text=fake.text(max_nb_chars=500),
                author=random.choice(users),
                rating=0 
            ))
            
        Question.objects.bulk_create(questions_to_create, batch_size=5000)
        questions = list(Question.objects.all())

        self.stdout.write('Привязка тегов к вопросам...')
        QuestionTagRel = Question.tags.through
        relations = []
        for q in questions:
            chosen_tags = random.sample(tags, random.randint(1, 3))
            for t in chosen_tags:
                relations.append(QuestionTagRel(question_id=q.id, tag_id=t.id))
            if len(relations) >= 10000:
                QuestionTagRel.objects.bulk_create(relations, ignore_conflicts=True)
                relations = []
        QuestionTagRel.objects.bulk_create(relations, ignore_conflicts=True)

        self.stdout.write('Генерация ответов...')
        answers_to_create = []
        for i in range(ratio * 100):
            answers_to_create.append(Answer(
                text=fake.text(max_nb_chars=200),
                question=random.choice(questions),
                author=random.choice(users),
                rating=0
            ))
            if len(answers_to_create) >= 10000:
                Answer.objects.bulk_create(answers_to_create)
                answers_to_create = []
        Answer.objects.bulk_create(answers_to_create)
        answer_ids = list(Answer.objects.values_list('id', flat=True))

        self.stdout.write('Генерация лайков к вопросам...')
        q_likes = []
        q_rating_map = {q.id: 0 for q in questions} 
        
        for _ in range(ratio * 200):
            q_id = random.choice(list(q_rating_map.keys()))
            val = random.choice([1, 1, 1, -1]) 
            q_likes.append(QuestionLike(user=random.choice(users), question_id=q_id, value=val))
            q_rating_map[q_id] += val
            
            if len(q_likes) >= 10000:
                QuestionLike.objects.bulk_create(q_likes, ignore_conflicts=True)
                q_likes = []
        QuestionLike.objects.bulk_create(q_likes, ignore_conflicts=True)

        self.stdout.write('Обновление рейтинга вопросов...')
        for q in questions:
            q.rating = q_rating_map.get(q.id, 0)
        Question.objects.bulk_update(questions, ['rating'], batch_size=5000)

        
        self.stdout.write('Генерация лайков к ответам...')
        a_likes = []
        sampled_answer_ids = random.sample(answer_ids, min(len(answer_ids), ratio * 50))
        a_rating_map = {a_id: 0 for a_id in sampled_answer_ids}

        for _ in range(ratio * 200):
            a_id = random.choice(sampled_answer_ids)
            val = random.choice([1, 1, -1])
            a_likes.append(AnswerLike(user=random.choice(users), answer_id=a_id, value=val))
            a_rating_map[a_id] += val
            
            if len(a_likes) >= 10000:
                AnswerLike.objects.bulk_create(a_likes, ignore_conflicts=True)
                a_likes = []
        AnswerLike.objects.bulk_create(a_likes, ignore_conflicts=True)

        self.stdout.write('Обновление  рейтинга ответов...')
        answers_to_update = []
        for a_id, r_val in a_rating_map.items():
            answers_to_update.append(Answer(id=a_id, rating=r_val))
            if len(answers_to_update) >= 5000:
                Answer.objects.bulk_update(answers_to_update, ['rating'])
                answers_to_update = []
        Answer.objects.bulk_update(answers_to_update, ['rating'])

        self.stdout.write(self.style.SUCCESS(f'База успешно заполнена (ratio={ratio})'))