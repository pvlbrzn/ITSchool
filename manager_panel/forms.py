from django.contrib.auth.forms import UserCreationForm
from django import forms

from main.models import CustomUser, Course, Blog, FAQ, Newsletter


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class ManagerUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'age', 'phone',
                  'bio', 'stack', 'image', 'role')  # Включаем 'role' для создания

    def __init__(self, *args, **kwargs):
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

    def save(self, commit=True):
        user = super().save(commit=False)

        # Если пароль был изменен, устанавливаем новый
        if 'password1' in self.cleaned_data and self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class ManagerUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'age', 'phone',
                  'bio', 'stack', 'image', 'role')  # Добавляем 'role' для редактирования

    def __init__(self, *args, **kwargs):
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

    def save(self, commit=True):
        user = super().save(commit=False)

        # Если пароль был изменен, устанавливаем новый
        if 'password1' in self.cleaned_data and self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'


class QuestionsForm(forms.ModelForm):
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
