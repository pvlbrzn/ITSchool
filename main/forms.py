from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import CustomUser


class StudentRegistrationForm(UserCreationForm):
    agree = forms.BooleanField(
        required=True,
        label='Я согласен с Условиями и предложениями',
        error_messages={'required': 'Вы должны согласиться с условиями.'},
        widget=forms.CheckboxInput(attrs={
            'class': 'm-check-input',
            'id': 'm-agree',
        })
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'age')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'  # Устанавливаем роль вручную
        if commit:
            user.save()
        return user
