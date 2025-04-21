from django.core.management.base import BaseCommand
from faker import Faker
from main.models import Lesson, Course
import random


class Command(BaseCommand):
    help = 'Создать фейковые уроки для курсов'

    def handle(self, *args, **options):
        fake = Faker()
        fake_ru = Faker('ru_RU')

        courses = Course.objects.all()

        if not courses.exists():
            self.stdout.write(self.style.ERROR('Нет доступных курсов. Сначала создайте курсы.'))
            return

        for course in courses:
            start_date = course.start_date
            end_date = course.end_date

            for i in range(random.randint(5, 10)):
                lesson_date = fake.date_between_dates(
                    date_start=start_date,
                    date_end=end_date
                )

                Lesson.objects.create(
                    course=course,
                    title=f'Занятие {i + 1}',
                    content=fake_ru.paragraph(nb_sentences=3),
                    # date=lesson_date,
                    # start_time=fake.time_object(),
                    # duration=random.randint(60, 180),
                )

        self.stdout.write(self.style.SUCCESS(f'Успешно созданы занятия для {courses.count()} уроков'))
