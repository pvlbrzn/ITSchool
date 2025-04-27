from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import CustomUser, Subscriber, Newsletter


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

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'})
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if Subscriber.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже подписан.")
        return email


class NewsForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['subject', 'message']
        labels = {
            'subject': 'Тема',
            'message': 'Сообщение'
        }
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Введите тему письма'}),
            'message': forms.Textarea(attrs={'placeholder': 'Введите текст сообщения'})
        }


