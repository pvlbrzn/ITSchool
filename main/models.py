import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.

    Adds support for roles (student, teacher, manager), biography, age,
    tech stack, phone number, and user image.
    """
    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('manager', 'Менеджер'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name='Роль'
    )
    bio = models.TextField(blank=True, null=True, verbose_name='Биография')
    age = models.PositiveIntegerField(blank=True, null=True, verbose_name='Возраст')
    stack = models.CharField(max_length=200, blank=True, null=True, verbose_name='Стек технологий')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')
    image = models.ImageField(upload_to='', blank=True, null=True, verbose_name='Изображение')

    def is_student(self) -> bool:
        """Check if the user has the 'student' role."""
        return self.role == 'student'

    def is_teacher(self) -> bool:
        """Check if the user has the 'teacher' role."""
        return self.role == 'teacher'

    def is_manager(self) -> bool:
        """Check if the user has the 'manager' role."""
        return self.role == 'manager'

    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"


class Course(models.Model):
    """
    Represents a course in the system with related teachers and students.
    """
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('js', 'JavaScript'),
        ('csharp', 'C#'),
        ('go', 'Go'),
    ]

    SKILL_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('test', 'Test'),
        ('devops', 'Devops'),
        ('security', 'Security'),
        ('ml', 'ML'),
    ]

    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    duration = models.FloatField(help_text='Продолжительность курса в месяцах.', verbose_name='Длительность')
    start_date = models.DateField(verbose_name='Дата начала', db_index=True)
    end_date = models.DateField(verbose_name='Дата окончания', db_index=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Стоимость')
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, verbose_name='Язык')
    skill = models.CharField(max_length=20, choices=SKILL_CHOICES, verbose_name='Тип')
    image = models.ImageField(upload_to='', blank=True, null=True, verbose_name='Изображение')
    teachers = models.ManyToManyField(
        'CustomUser',
        limit_choices_to={'role': 'teacher'},
        related_name='courses_as_teacher',
        verbose_name='Преподаватели'
    )
    students = models.ManyToManyField(
        'CustomUser',
        limit_choices_to={'role': 'student'},
        related_name='courses_as_student',
        verbose_name='Студенты'
    )

    def is_active(self) -> bool:
        """Check if the course is currently active based on dates."""
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['title', 'price']


class Lesson(models.Model):
    """
    Represents a lesson within a course.
    """
    title = models.CharField(max_length=150, verbose_name='Тема занятия')
    content = models.TextField(verbose_name='Содержание')
    teacher = models.ForeignKey(
        'CustomUser',
        limit_choices_to={'role': 'teacher'},
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lessons',
        verbose_name='Преподаватель'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )

    def __str__(self) -> str:
        return f'{self.title} ({self.course.title})'

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        ordering = ['title']


class Payment(models.Model):
    """
    Represents a payment made by a student for a course.
    """
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Сумма оплаты')
    payment_date = models.DateTimeField(default=timezone.now, verbose_name='Дата оплаты')
    is_successful = models.BooleanField(default=True, verbose_name='Оплата прошла успешно?')
    payment_method = models.CharField(max_length=50, blank=True, null=True, verbose_name='Метод оплаты')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    student = models.ForeignKey(
        'CustomUser',
        limit_choices_to={'role': 'student'},
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Студент'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Курс'
    )

    def __str__(self) -> str:
        return f'{self.student} → {self.course} ({self.amount}р.)'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
        ordering = ['-payment_date']


class Blog(models.Model):
    """
    Represents a blog post or article.
    """
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    annotation = models.TextField(verbose_name='Аннотация')
    content = models.TextField(verbose_name='Содержание')
    date = models.DateField(default=timezone.now, verbose_name='Дата публикации')
    author = models.CharField(max_length=20, verbose_name='Автор')
    image = models.ImageField(upload_to='', verbose_name='Изображение')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ['title']


class Subscriber(models.Model):
    """
    Email subscriber model with confirmation status.
    """
    email = models.EmailField(unique=True)
    is_confirmed = models.BooleanField(default=False)
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        ordering = ['email']


class Newsletter(models.Model):
    """
    Represents a newsletter or announcement.
    """
    subject = models.CharField(max_length=255, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='', verbose_name='Изображение', blank=True, null=True)

    def __str__(self) -> str:
        return self.subject

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['subject']


class FAQ(models.Model):
    """
    Represents a frequently asked question.
    """
    question = models.CharField(max_length=255, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')

    def __str__(self) -> str:
        return self.question

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['question']


class EnrollmentRequest(models.Model):
    """
    Represents a user's request to enroll in a course.
    """
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='enrollment_requests',
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollment_requests',
        verbose_name='Курс'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self) -> str:
        return f"{self.user.username} → {self.course.title} ({self.get_status_display()})"

    class Meta:
        verbose_name = 'Заявка на курс'
        verbose_name_plural = 'Заявки на курсы'
        unique_together = ('user', 'course')


class Review(models.Model):
    """
    Represents a course or platform review.
    """
    image = models.ImageField(upload_to='', verbose_name='Изображение', blank=True, null=True)
    comment = models.TextField(verbose_name='Ответ')
    author = models.CharField(max_length=20, verbose_name='Автор')
    date = models.DateField(default=timezone.now, verbose_name='Дата публикации')

    def __str__(self) -> str:
        return self.comment

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['date']
