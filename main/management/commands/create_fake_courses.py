from django.core.management.base import BaseCommand
from main.models import Course
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Генерирует тестовых преподавателей в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10)

    def handle(self, *args, **options):
        languages = ['Python', 'C#', 'GO', 'Java', 'JavaScript']
        skills = ['frontend', 'backend', 'devops', 'ML', 'Security', 'test']
        fake_ru = Faker('ru_RU')
        fake = Faker()
        count = options['count']

        for _ in range(count):
            lang = random.choice(languages)
            skil = random.choice(skills)
            Course.objects.create(
                title=f'{skil} {lang}',
                description=fake_ru.sentences(2),
                duration=fake.random_int(min=4, max=10),
                start_date=fake.date_between(start_date='today', end_date='+6m'),
                end_date=fake.date_between(start_date='+8m', end_date='+14m'),
                price=fake.random_int(min=1600, max=3600),
                language=lang,
                skill=skil
            )

        self.stdout.write(
            self.style.SUCCESS(f'Успешно создано {count} курсов')
        )
