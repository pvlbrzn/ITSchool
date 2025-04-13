from django.db import models
from django.utils import timezone


class Teacher(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', blank=True, null=True)
    bio = models.TextField(verbose_name='Биография', blank=True, null=True)
    email = models.EmailField(verbose_name='Эл. почта', unique=True)
    age = models.PositiveIntegerField(verbose_name='Возраст', help_text='в годах')
    stack = models.CharField(max_length=200, blank=True,
                             help_text="Языки через запятую (python, js)")

    def __str__(self):
        return f"{self.last_name} {self.first_name}".strip()

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        ordering = ['last_name', 'first_name']


class Student(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', blank=True, null=True)
    email = models.EmailField(verbose_name='Эл. почта', unique=True)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}".strip()

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['last_name', 'first_name']


class Course(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('js', 'JavaScript'),
        ('csharp', 'C#'),
        ('go', 'Go'),
    ]

    TYPE_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('test', 'Test'),
        ('devops', 'Devops'),
        ('security', 'Security'),
        ('ml', 'ML'),
    ]

    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    duration = models.FloatField(help_text='Продолжительность курса в месяцах.',
                                 verbose_name='Длительность')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Стоимость')
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, verbose_name='Язык')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Тип')
    teachers = models.ManyToManyField(Teacher, related_name='courses',
                                      verbose_name='Преподаватели')
    students = models.ManyToManyField(Student, related_name='courses',
                                      verbose_name='Студенты')
    # lessons = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='courses',
    #                            verbose_name='Занятия')

    def is_active(self) -> bool:
        """
        The method shows whether the course is active.
        """
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['title', 'price']
