from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import CustomUser, Subscriber, Newsletter


class StudentRegistrationForm(UserCreationForm):
    """
    Форма для регистрации студента.

    Включает поля для имени пользователя, email, пароля, имени, фамилии, телефона, возраста
    и согласие с условиями.
    """
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
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'phone',
            'age'
        )

    def save(self, commit: bool = True) -> CustomUser:
        """
        Сохраняет пользователя с ролью 'student'.

        :param commit: Флаг, указывающий, нужно ли сохранять объект в базе данных.
        :return: Сохранённый объект пользователя.
        """
        user = super().save(commit=False)
        user.role = 'student'  # Устанавливаем роль вручную
        if commit:
            user.save()
        return user


class SubscribeForm(forms.ModelForm):
    """
    Форма подписки на новостную рассылку.

    Включает только поле для email и проверку на уникальность email.
    """
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'})
        }

    def clean_email(self) -> str:
        """
        Проверяет уникальность email для подписки.

        :return: Проверенный и очищенный email.
        :raises ValidationError: Если email уже подписан.
        """
        email = self.cleaned_data['email']
        subscriber = Subscriber.objects.filter(email=email).first()
        if subscriber and subscriber.is_confirmed:
            raise forms.ValidationError("Этот email уже подписан.")
        return email


class NewsForm(forms.ModelForm):
    """
    Форма для создания и отправки новостной рассылки.

    Включает поля для темы и сообщения.
    """
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


class SubscriptionForm(forms.Form):
    email = forms.EmailField()


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=255)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
