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
    skill = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Тип')
    teachers = models.ManyToManyField(Teacher, related_name='courses',
                                      verbose_name='Преподаватели')
    students = models.ManyToManyField(Student, related_name='courses',
                                      verbose_name='Студенты')


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


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Тема занятия')
    content = models.TextField(verbose_name='Содержание')
    teacher = models.ForeignKey(Teacher, related_name='lessons', on_delete=models.SET_NULL,
                                null=True, verbose_name='Преподаватель')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='lessons', verbose_name='Курс')

    def __str__(self):
        return f'{self.title} ({self.course.title})'

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        ordering = ['title']


class Payment(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Сумма оплаты')
    payment_date = models.DateTimeField(default=timezone.now, verbose_name='Дата оплаты')
    is_successful = models.BooleanField(default=True, verbose_name='Оплата прошла успешно?')
    payment_method = models.CharField(max_length=50, blank=True, null=True,
                                      verbose_name='Метод оплаты')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                related_name='payments', verbose_name='Студент')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='payments', verbose_name='Курс')

    def __str__(self):
        return f'{self.student} → {self.course} ({self.amount}р.)'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
        ordering = ['-payment_date']


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    date = models.DateField(default=timezone.now, verbose_name='Дата публикации')
    author = models.CharField(max_length=20, verbose_name='Автор')
    image = models.ImageField(upload_to='', verbose_name='Изображение')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ['title']
