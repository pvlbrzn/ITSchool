from datetime import timedelta
from io import BytesIO
from typing import List

from PIL import Image
import random
from faker import Faker

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from main.models import CustomUser, Course, Lesson

fake = Faker('ru_RU')

languages = ['python', 'csharp', 'go', 'java', 'js']
skills = ['frontend', 'backend', 'devops', 'ml', 'security', 'test']


def get_image_file() -> ContentFile:
    """
    Generates a random PNG image and returns it as a Django ContentFile.
    Used for populating image fields in models.
    """
    img = Image.new('RGB', (800, 536),
                    color=(random.randint(100, 255),
                           random.randint(100, 255),
                           random.randint(100, 255)))
    bio = BytesIO()
    img.save(bio, format='PNG')
    bio.seek(0)
    return ContentFile(bio.read(), name=f"{fake.word()}.png")


class Command(BaseCommand):
    help = 'Генерация тестовых данных'

    def handle(self, *args, **kwargs) -> None:
        """
        Entry point for the management command.
        Creates test users, courses, and lessons with dummy data.
        """
        self.stdout.write("Начало генерации данных...")

        teachers = self.generate_users(count=10, role='teacher')
        self.stdout.write(f"Создано {len(teachers)} преподавателей")

        students = self.generate_users(count=20, role='student')
        self.stdout.write(f"Создано {len(students)} студентов")

        courses = self.generate_courses(teachers, students, count=10)
        self.stdout.write(f"Создано {len(courses)} курсов")

        lessons = self.generate_lessons(courses)
        self.stdout.write(f"Создано {len(lessons)} занятий")

        self.stdout.write(self.style.SUCCESS("Генерация завершена!"))

    def generate_users(self, count: int, role: str) -> List[CustomUser]:
        """
        Creates a list of users with the specified role.

        :param count: Number of users to create.
        :param role: 'student' or 'teacher'.
        :return: List of created CustomUser instances.
        """
        users = []
        for _ in range(count):
            email = fake.unique.email()
            user = CustomUser.objects.create_user(
                username=email.split('@')[0],
                email=email,
                password='test1234',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                age=random.randint(18, 65),
                role=role,
                phone=fake.phone_number() if role == 'student' else None,
                stack=', '.join(random.sample(languages, random.randint(1, 3))) if role == 'teacher' else None
            )
            # Добавим фото
            user.image.save(f'{user.username}_photo.png', get_image_file(), save=True)
            users.append(user)
        return users

    def generate_courses(self, teachers: List[CustomUser], students: List[CustomUser], count: int) -> List[Course]:
        """
        Creates a list of courses, randomly assigning teachers and students.

        :param teachers: List of available teacher users.
        :param students: List of available student users.
        :param count: Number of courses to create.
        :return: List of created Course instances.
        """
        courses = []
        for _ in range(count):
            language = random.choice(languages)
            skill = random.choice(skills)
            start_date = fake.date_between(start_date='today', end_date='+30d')
            end_date = start_date + timedelta(days=random.randint(60, 180))

            course = Course.objects.create(
                title=f"{skill.capitalize()} на {language.upper()}",
                description="\n".join(fake.paragraphs(nb=3)),
                duration=round(random.uniform(2.0, 6.0), 1),
                start_date=start_date,
                end_date=end_date,
                price=random.randint(1000, 7000),
                language=language,
                skill=skill
            )
            course.teachers.set(random.sample(teachers, k=min(len(teachers), 3)))
            course.students.set(random.sample(students, k=min(len(students), 20)))

            # Добавим картинку
            course.image.save(f'{course.title[:10]}_img.png', get_image_file(), save=True)

            courses.append(course)
        return courses

    def generate_lessons(self, courses: List[Course]) -> List[Lesson]:
        """
        Creates a set of lessons for each course.

        :param courses: List of Course instances.
        :return: List of created Lesson instances.
        """
        lessons = []
        for course in courses:
            for i in range(random.randint(8, 12)):
                lesson = Lesson.objects.create(
                    title=f"Занятие {i + 1}: {course.title}",
                    content="\n".join(fake.paragraphs(nb=2)),
                    teacher=random.choice(course.teachers.all()),
                    course=course
                )
                lessons.append(lesson)
        return lessons
