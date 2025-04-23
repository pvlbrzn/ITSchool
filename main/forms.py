from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'age')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'  # Устанавливаем роль вручную
        if commit:
            user.save()
        return user

