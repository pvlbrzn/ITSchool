from faker import Faker
from django.core.management.base import BaseCommand
from main.models import Teacher, Student, Course, Lesson
import random
from datetime import timedelta

fake = Faker('ru_RU')

languages = ['Python', 'C#', 'GO', 'Java', 'JavaScript']
skills = ['frontend', 'backend', 'devops', 'ML', 'Security', 'test']


class Command(BaseCommand):
    help = 'Генерация тестовых данных для всех моделей'

    def handle(self, *args, **options):
        self.stdout.write("Начало генерации данных...")

        teachers = self.generate_teachers(15)
        self.stdout.write(f"Создано {len(teachers)} преподавателей")

        students = self.generate_students(50)
        self.stdout.write(f"Создано {len(students)} студентов")

        courses = self.generate_courses(teachers, students, 10)
        self.stdout.write(f"Создано {len(courses)} курсов")

        lessons = self.generate_lessons(courses, teachers)
        self.stdout.write(f"Создано {len(lessons)} занятий")

        self.stdout.write(
            self.style.SUCCESS("Генерация данных успешно завершена!")
        )

    def generate_teachers(self, count):
        teachers = []
        for _ in range(count):
            teacher = Teacher.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                patronymic=fake.middle_name(),
                bio=fake.paragraph(nb_sentences=3),
                email=fake.unique.email(),
                age=random.randint(25, 65),
                stack=", ".join(random.sample(['python', 'java', 'js', 'csharp', 'go'], k=random.randint(1, 3)))
            )
            teachers.append(teacher)
        return teachers

    def generate_students(self, count):
        students = []
        for _ in range(count):
            student = Student.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                patronymic=fake.middle_name() if random.choice([True, False]) else None,
                email=fake.unique.email(),
                phone=fake.phone_number()
            )
            students.append(student)
        return students

    def generate_courses(self, teachers, students, count):
        courses = []
        language_choices = [lang[0] for lang in Course.LANGUAGE_CHOICES]
        skill_choices = [skill[0] for skill in Course.SKILL_CHOICES]

        for _ in range(count):
            lang = random.choice(language_choices)
            skill = random.choice(skill_choices)

            start_date = fake.date_between(start_date='today', end_date='+6m')
            end_date = start_date + timedelta(days=random.randint(60, 180))

            course = Course.objects.create(
                title=f"{skill} {lang}",
                description="\n".join(fake.paragraphs(nb=3)),
                duration=round(random.uniform(2.0, 6.0), 1),
                start_date=start_date,
                end_date=end_date,
                price=random.randint(1500, 5000),
                language=lang,
                skill=skill
            )

            course.teachers.set(random.sample(list(teachers), k=min(3, len(teachers))))
            course.students.set(random.sample(list(students), k=min(20, len(students))))

            courses.append(course)

        return courses

    def generate_lessons(self, courses, teachers):
        lessons = []
        for course in courses:
            for i in range(random.randint(8, 12)):
                lesson_date = fake.date_between_dates(
                    date_start=course.start_date,
                    date_end=course.end_date
                )

                lesson = Lesson.objects.create(
                    title=f"Занятие {i + 1}: {course.title}",
                    content="\n".join(fake.paragraphs(nb=2)),
                    teacher=random.choice(course.teachers.all()),
                    course=course
                )
                lessons.append(lesson)
        return lessons
