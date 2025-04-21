from django.core.management.base import BaseCommand
from main.models import Teacher
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Генерирует тестовых преподавателей в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10)

    def handle(self, *args, **options):
        languages = ['Python', 'C#', 'GO', 'Java', 'JavaScript']

        fake_ru = Faker('ru_RU')
        fake = Faker()
        count = options['count']

        for _ in range(count):
            Teacher.objects.create(
                age=fake.random_int(min=23, max=45),
                first_name=fake_ru.first_name(),
                last_name=fake_ru.last_name(),
                bio=fake_ru.paragraph(nb_sentences=3),
                email=fake.email(),
                stack=random.choice(languages)
            )

        self.stdout.write(
            self.style.SUCCESS(f'Успешно создано {count} ')
        )
