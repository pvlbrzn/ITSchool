from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Subscriber, Newsletter


class StudentRegistrationForm(UserCreationForm):
    """
    Form for student registration.

    Includes fields for username, email, password, first name, last name,
    phone number, age, and a required agreement checkbox.
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
        Saves the user with the role set to 'student'.

        :param commit: Whether to save the object to the database.
        :return: The saved CustomUser instance.
        """
        user = super().save(commit=False)
        user.role = 'student'  # Устанавливаем роль вручную
        if commit:
            user.save()
        return user


class SubscribeForm(forms.ModelForm):
    """
    Form for subscribing to the newsletter.

    Includes a unique email field.
    """
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'})
        }

    def clean_email(self) -> str:
        """
        Ensures the email is not already confirmed for subscription.

        :raises ValidationError: If the email is already subscribed.
        :return: Validated email.
        """
        email = self.cleaned_data['email']
        subscriber = Subscriber.objects.filter(email=email).first()
        if subscriber and subscriber.is_confirmed:
            raise forms.ValidationError("Этот email уже подписан.")
        return email


class NewsForm(forms.ModelForm):
    """
    Form for creating and sending a newsletter.

    Includes fields for subject and message content.
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
    """
    Basic subscription form with a single email field.
    """
    email = forms.EmailField()


class ContactForm(forms.Form):
    """
    Contact form for sending a message.

    Includes name, subject, email, and message body.
    """
    name = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=255)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
