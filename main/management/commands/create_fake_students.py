from django.core.management.base import BaseCommand
from main.models import Student
from faker import Faker


class Command(BaseCommand):
    help = 'Генерирует тестовых преподавателей в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10)

    def handle(self, *args, **options):
        fake_ru = Faker('ru_RU')
        fake = Faker()
        count = options['count']

        for _ in range(count):
            Student.objects.create(
                first_name=fake_ru.first_name(),
                last_name=fake_ru.last_name(),
                email=fake.email(),
                phone=fake.phone_number()
            )

        self.stdout.write(
            self.style.SUCCESS(f'Успешно создано {count} ')
        )
