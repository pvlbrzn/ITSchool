from django.contrib.auth.forms import UserCreationForm
from django import forms

from main.models import CustomUser, Course, Blog, FAQ, Newsletter


class CourseForm(forms.ModelForm):
    """
    Form for creating and editing courses.

    Attributes:
        students (ModelMultipleChoiceField): Multiple selection of students for the course.
        teachers (ModelMultipleChoiceField): Multiple selection of teachers for the course.
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
    Form for creating a new user.

    Attributes:
        username (str): User's username.
        email (str): User's email address.
        first_name (str): User's first name.
        last_name (str): User's last name.
        age (int): User's age.
        phone (str): User's phone number.
        bio (str): User's biography.
        stack (str): User's technology stack.
        image (Image): User's profile image.
        role (str): User's role (student, teacher).
    """

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'age', 'phone',
            'bio', 'stack', 'image', 'role'
        )

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and set available role choices.

        For creation, only 'student' and 'teacher' roles are available.
        For editing, 'manager' role is excluded unless it's a superuser.
        """
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields['role'].choices = [
                ('student', 'Студент'),
                ('teacher', 'Преподаватель')
            ]
        else:
            if self.instance.role != 'manager':
                self.fields['role'].choices = [
                    ('student', 'Студент'),
                    ('teacher', 'Преподаватель')
                ]
            elif not self.instance.is_superuser:
                self.fields['role'].choices = [
                    ('student', 'Студент'),
                    ('teacher', 'Преподаватель')
                ]

    def save(self, commit=True) -> CustomUser:
        """
        Save the new user and set password if provided.

        Args:
            commit (bool): Whether to save the instance to the database.

        Returns:
            CustomUser: The saved user instance.
        """
        user = super().save(commit=False)
        if 'password1' in self.cleaned_data and self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class ManagerUserEditForm(forms.ModelForm):
    """
    Form for editing an existing user.

    Attributes:
        username (str): User's username.
        email (str): User's email address.
        first_name (str): User's first name.
        last_name (str): User's last name.
        age (int): User's age.
        phone (str): User's phone number.
        bio (str): User's biography.
        stack (str): User's technology stack.
        image (Image): User's profile image.
        role (str): User's role (student, teacher).
    """

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'age', 'phone',
            'bio', 'stack', 'image', 'role'
        )

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and restrict role changes if necessary.

        If the user is a manager and not a superuser, the role field is disabled.
        """
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields.pop('password1', None)
            self.fields.pop('password2', None)

        if self.instance and self.instance.pk:
            if self.instance.role == 'manager' and not self.instance.is_superuser:
                self.fields['role'].disabled = True
            else:
                self.fields['role'].choices = [
                    ('student', 'Студент'),
                    ('teacher', 'Преподаватель')
                ]

    def save(self, commit=True) -> CustomUser:
        """
        Save the updated user and set password if changed.

        Args:
            commit (bool): Whether to save the instance to the database.

        Returns:
            CustomUser: The updated user instance.
        """
        user = super().save(commit=False)
        if 'password1' in self.cleaned_data and self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class BlogForm(forms.ModelForm):
    """
    Form for creating and editing blog posts.

    Attributes:
        title (str): Blog title.
        content (str): Blog content.
        image (Image): Blog image.
    """

    class Meta:
        model = Blog
        fields = '__all__'


class QuestionsForm(forms.ModelForm):
    """
    Form for creating and editing FAQ entries.

    Attributes:
        question (str): The frequently asked question.
        answer (str): The answer to the question.
    """

    class Meta:
        model = FAQ
        fields = '__all__'


class NewsForm(forms.ModelForm):
    """
    Form for creating and editing newsletters.
    """

    class Meta:
        model = Newsletter
        fields = '__all__'


class NewsletterSendForm(forms.Form):
    """
    Form for sending a selected newsletter to specific users.

    Attributes:
        users (QuerySet[CustomUser]): Selected users to receive the newsletter.
        newsletter (Newsletter): The newsletter to be sent.
    """

    users = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Выберите пользователей"
    )
    newsletter = forms.ModelChoiceField(
        queryset=Newsletter.objects.all(),
        label="Выберите новость"
    )
