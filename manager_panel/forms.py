from django.contrib.auth.forms import UserCreationForm
from django import forms

from main.models import CustomUser, Course, Blog, FAQ, Newsletter


class CourseForm(forms.ModelForm):
    """
    Форма для создания и редактирования курсов.

    Атрибуты:
        students (ModelMultipleChoiceField): Множественный выбор студентов для курса.
        teachers (ModelMultipleChoiceField): Множественный выбор преподавателей для курса.
    """

    class Meta:
        model = Course
        fields = '__all__'

    students: forms.ModelMultipleChoiceField = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role='student'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox student-checkboxes'}),
        required=False
    )

    teachers: forms.ModelMultipleChoiceField = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role='teacher'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox teacher-checkboxes'}),
        required=False
    )


class ManagerUserCreateForm(UserCreationForm):
    """
    Форма для создания нового пользователя.

    Атрибуты:
        username (str): Имя пользователя.
        email (str): Электронная почта пользователя.
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        age (int): Возраст пользователя.
        phone (str): Телефон пользователя.
        bio (str): Биография пользователя.
        stack (str): Технологический стек пользователя.
        image (Image): Изображение пользователя.
        role (str): Роль пользователя (студент, преподаватель).
    """

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'age', 'phone',
                  'bio', 'stack', 'image', 'role')

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы с установкой доступных вариантов для поля 'role'.

        Если пользователь создается, доступны только роли 'студент' и 'преподаватель'.
        Если редактируется, можно изменить роль только если это не менеджер.
        """
        super().__init__(*args, **kwargs)

        # Если это создание нового пользователя
        if not self.instance.pk:
            self.fields['role'].choices = [
                ('student', 'Студент'),
                ('teacher', 'Преподаватель')
            ]
        else:
            # Для редактирования, если роль пользователя не "менеджер", исключаем роль "менеджер"
            if self.instance.role != 'manager':
                self.fields['role'].choices = [
                    ('student', 'Студент'),
                    ('teacher', 'Преподаватель')
                ]
            else:
                # Для "менеджера" роль "менеджер" доступна только для суперпользователя
                if not self.instance.is_superuser:
                    self.fields['role'].choices = [
                        ('student', 'Студент'),
                        ('teacher', 'Преподаватель')
                    ]

    def save(self, commit=True) -> CustomUser:
        """
        Сохранение нового пользователя с установкой пароля, если он был изменен.

        :param commit: Если True, сохраняет пользователя в базе данных.
        :return: Сохраненный объект пользователя.
        """
        user = super().save(commit=False)

        # Если пароль был изменен, устанавливаем новый
        if 'password1' in self.cleaned_data and self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class ManagerUserEditForm(forms.ModelForm):
    """
    Форма для редактирования существующего пользователя.

    Атрибуты:
        username (str): Имя пользователя.
        email (str): Электронная почта пользователя.
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        age (int): Возраст пользователя.
        phone (str): Телефон пользователя.
        bio (str): Биография пользователя.
        stack (str): Технологический стек пользователя.
        image (Image): Изображение пользователя.
        role (str): Роль пользователя (студент, преподаватель).
    """

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'age', 'phone',
                  'bio', 'stack', 'image', 'role')

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы с установкой доступных вариантов для поля 'role'.
        При редактировании: если роль пользователя - "менеджер", она не может быть изменена.
        """
        super().__init__(*args, **kwargs)

        # Убираем поля пароля при редактировании
        if self.instance.pk:
            self.fields.pop('password1', None)
            self.fields.pop('password2', None)

        # Если это редактирование существующего пользователя
        if self.instance and self.instance.pk:
            # Если роль пользователя - "менеджер", то роль нельзя изменить
            if self.instance.role == 'manager' and not self.instance.is_superuser:
                self.fields['role'].disabled = True  # Блокируем поле роли
            else:
                # Если это не менеджер, то можно изменять роль между студентом и преподавателем
                self.fields['role'].choices = [
                    ('student', 'Студент'),
                    ('teacher', 'Преподаватель')
                ]

    def save(self, commit=True) -> CustomUser:
        """
        Сохранение изменений пользователя с установкой пароля, если он был изменен.

        :param commit: Если True, сохраняет пользователя в базе данных.
        :return: Сохраненный объект пользователя.
        """
        user = super().save(commit=False)

        # Если пароль был изменен, устанавливаем новый
        if 'password1' in self.cleaned_data and self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class BlogForm(forms.ModelForm):
    """
    Форма для создания и редактирования блогов.

    Атрибуты:
        title (str): Заголовок блога.
        content (str): Контент блога.
        image (Image): Изображение блога.
    """

    class Meta:
        model = Blog
        fields = '__all__'


class QuestionsForm(forms.ModelForm):
    """
    Форма для создания и редактирования часто задаваемых вопросов (FAQ).

    Атрибуты:
        question (str): Вопрос.
        answer (str): Ответ на вопрос.
    """

    class Meta:
        model = FAQ
        fields = '__all__'


class NewsForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = '__all__'


class NewsletterSendForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Выберите пользователей"
    )
    newsletter = forms.ModelChoiceField(
        queryset=Newsletter.objects.all(),
        label="Выберите новость"
    )
