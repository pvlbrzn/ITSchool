from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mass_mail
from django.http import HttpRequest, HttpResponse

from main.models import (CustomUser, Course, Blog, Lesson, EnrollmentRequest, FAQ, Newsletter, Subscriber)
from .forms import (CourseForm, ManagerUserCreateForm, ManagerUserEditForm, BlogForm,
                    QuestionsForm, NewsForm, NewsletterSendForm)


def is_manager(user: CustomUser) -> bool:
    """Проверяет, является ли пользователь менеджером или суперпользователем."""
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name='managers').exists()
)


@user_passes_test(is_manager)
def manager(request: HttpRequest) -> HttpResponse:
    """Страница аккаунта менеджера."""
    return render(
        request,
        'manager_panel/manager-account.html',
        {'user_role': request.user.get_role_display()}
    )


@user_passes_test(is_manager)
def course_list(request: HttpRequest) -> HttpResponse:
    """Отображает список курсов с возможностью фильтрации."""
    search_query: str = request.GET.get('search', '')
    language_filter: str = request.GET.get('language', '')
    start_date_filter: str = request.GET.get('start_date', '')
    end_date_filter: str = request.GET.get('end_date', '')

    courses = Course.objects.all()

    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if language_filter:
        courses = courses.filter(language=language_filter)

    if start_date_filter:
        try:
            start_date = datetime.strptime(start_date_filter, '%Y-%m-%d')
            courses = courses.filter(start_date__gte=start_date)
        except ValueError:
            pass

    if end_date_filter:
        try:
            end_date = datetime.strptime(end_date_filter, '%Y-%m-%d')
            courses = courses.filter(end_date__lte=end_date)
        except ValueError:
            pass

    return render(
        request,
        'manager_panel/course/manager_course_list.html',
        {
            'courses': courses,
            'languages': Course.LANGUAGE_CHOICES,
            'search_query': search_query,
            'language_filter': language_filter,
            'start_date_filter': start_date_filter,
            'end_date_filter': end_date_filter,
        }
    )


@user_passes_test(is_manager)
def course_create(request: HttpRequest) -> HttpResponse:
    """Создание нового курса."""
    form = CourseForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('manager')
    return render(request, 'manager_panel/course/manager_add_course.html', {'form': form})


@user_passes_test(is_manager)
def course_edit(request: HttpRequest, pk: int) -> HttpResponse:
    """Редактирование существующего курса."""
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST or None, request.FILES or None, instance=course)

    selected_students_ids = course.students.values_list('id', flat=True)
    selected_teachers_ids = course.teachers.values_list('id', flat=True)

    if form.is_valid():
        form.save()
        return redirect('manager')

    return render(
        request,
        'manager_panel/course/manager_add_course.html',
        {
            'form': form,
            'selected_students_ids': selected_students_ids,
            'selected_teachers_ids': selected_teachers_ids,
        }
    )


@user_passes_test(is_manager)
def course_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Удаление курса."""
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('manager')
    return render(request, 'manager_panel/course/manager_del_course.html',
                  {'course': course})


@user_passes_test(is_manager)
def users_list(request: HttpRequest) -> HttpResponse:
    """Список пользователей с возможностью фильтрации по имени, роли и возрасту."""
    search_query = request.GET.get('search', '')
    age_filter = request.GET.get('age', '')
    role_filter = request.GET.get('role', '')
    newsletters = Newsletter.objects.all()

    users = CustomUser.objects.filter(is_superuser=False).exclude(role='manager')

    if search_query:
        users = users.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(username__icontains=search_query)
        )

    if age_filter:
        try:
            users = users.filter(age=int(age_filter))
        except ValueError:
            pass

    if role_filter in ['student', 'teacher']:
        users = users.filter(role=role_filter)

    return render(request, 'manager_panel/user/manager_users_list.html', {
        'users': users,
        'search_query': search_query,
        'age_filter': age_filter,
        'role_filter': role_filter,
        'newsletters': newsletters
    })


@user_passes_test(is_manager)
def user_create(request: HttpRequest) -> HttpResponse:
    """Создание нового пользователя менеджером."""
    form = ManagerUserCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password('default123')
        user.save()
        messages.success(request, f"Пользователь {user.username} успешно создан.")
        return redirect('manager_users_list')
    return render(request, 'manager_panel/user/manager_add_user.html', {'form': form})


@user_passes_test(is_manager)
def user_edit(request: HttpRequest, pk: int) -> HttpResponse:
    """Редактирование существующего пользователя, кроме менеджеров и суперпользователей."""
    user = get_object_or_404(CustomUser, pk=pk)

    if user.role == 'manager' or user.is_superuser:
        messages.error(request, "Нельзя редактировать администратора или менеджера.")
        return redirect('manager_users_list')

    form = ManagerUserEditForm(request.POST or None, request.FILES or None, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, f"Пользователь {user.username} успешно обновлён.")
        return redirect('manager_users_list')

    return render(request, 'manager_panel/user/manager_add_user.html', {'form': form})


@user_passes_test(is_manager)
def user_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Удаление пользователя."""
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Пользователь успешно удалён.")
        return redirect('manager_users_list')
    return render(request, 'manager_panel/user/manager_del_user.html', {'user': user})


@user_passes_test(is_manager)
def users_bulk_action(request: HttpRequest) -> HttpResponse:
    """Групповое действие над пользователями: удаление, блокировка, повышение в преподаватели."""
    if request.method == 'POST':
        user_ids = request.POST.getlist('selected_users')
        action = request.POST.get('action')

        if not user_ids or not action:
            messages.warning(request, "Выберите пользователей и действие для выполнения.")
            return redirect('manager_users_list')

        users = CustomUser.objects.filter(id__in=user_ids).exclude(role__in=['manager', 'superuser'])

        if action == 'delete':
            users.delete()
            messages.success(request, f"Удалено пользователей: {len(user_ids)}")
        elif action == 'promote':
            users.update(role='teacher')
            messages.success(request, f"Повышено до преподавателей: {len(user_ids)}")
        elif action == 'block':
            users.update(is_active=False)
            messages.success(request, f"Заблокировано пользователей: {len(user_ids)}")

        elif action == 'newsletter':
            newsletter_id = request.POST.get('newsletter_id')
            newsletter = get_object_or_404(Newsletter, id=newsletter_id)

            messages_list = []
            for user in users:
                if user.email:
                    messages_list.append((
                        newsletter.subject,
                        newsletter.message,
                        'blr.artyom.gonchar@gmail.com',
                        [user.email]
                    ))

            if messages_list:
                send_mass_mail(messages_list, fail_silently=False)
                messages.success(request, f'Рассылка отправлена {len(messages_list)} пользователям.')
            else:
                messages.warning(request, 'Ни у одного из выбранных пользователей нет email.')

            return redirect('manager_users_list')

        else:
            messages.error(request, "Неизвестное действие.")

    return redirect('manager_users_list')


@user_passes_test(is_manager)
def blog_list(request: HttpRequest) -> HttpResponse:
    """Список всех блогов."""
    blogs = Blog.objects.all()
    return render(request, 'manager_panel/blog/manager_blog_list.html',
                  {'blogs': blogs})


@user_passes_test(is_manager)
def blog_create(request: HttpRequest) -> HttpResponse:
    """Создание нового блога."""
    form = BlogForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('manager_blog_list')
    return render(request, 'manager_panel/blog/manager_add_blog.html',
                  {'form': form})


@user_passes_test(is_manager)
def blog_edit(request: HttpRequest, pk: int) -> HttpResponse:
    """Редактирование существующего блога."""
    blog = get_object_or_404(Blog, pk=pk)
    form = BlogForm(request.POST or None, request.FILES or None, instance=blog)
    if form.is_valid():
        form.save()
        return redirect('manager_blog_list')
    return render(request, 'manager_panel/blog/manager_add_blog.html',
                  {'form': form})


@user_passes_test(is_manager)
def blog_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Удаление блога."""
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('manager_blog_list')
    return render(request, 'manager_panel/blog/manager_del_blog.html',
                  {'blog': blog})


@user_passes_test(is_manager)
def lesson_list(request: HttpRequest, course_id: int) -> HttpResponse:
    """Список уроков по заданному курсу."""
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    return render(request, 'manager_panel/lesson/manager_lesson_list.html', {
        'course': course,
        'lessons': lessons,
    })


@user_passes_test(is_manager)
def lesson_create(request: HttpRequest, course_id: int) -> HttpResponse:
    """Создание нового урока в рамках курса."""
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        teacher_id = request.POST.get('teacher')

        teacher = CustomUser.objects.filter(id=teacher_id, role='teacher').first() if teacher_id else None

        Lesson.objects.create(course=course, title=title, content=content, teacher=teacher)
        return redirect('manager_lesson_list', course_id=course.id)

    teachers = CustomUser.objects.filter(role='teacher')
    return render(request, 'manager_panel/lesson/manager_add_lesson.html', {
        'course': course,
        'teachers': teachers,
    })


@user_passes_test(is_manager)
def lesson_edit(request: HttpRequest, pk: int) -> HttpResponse:
    """Редактирование урока."""
    lesson = get_object_or_404(Lesson, pk=pk)

    if request.method == 'POST':
        lesson.title = request.POST.get('title')
        lesson.content = request.POST.get('content')
        teacher_id = request.POST.get('teacher')
        lesson.teacher = CustomUser.objects.filter(id=teacher_id, role='teacher').first() if teacher_id else None
        lesson.save()
        return redirect('manager_lesson_list', course_id=lesson.course.id)

    teachers = CustomUser.objects.filter(role='teacher')
    return render(request, 'manager_panel/lesson/manager_edit_lesson.html', {
        'lesson': lesson,
        'teachers': teachers,
    })


@user_passes_test(is_manager)
def lesson_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Удаление урока."""
    lesson = get_object_or_404(Lesson, pk=pk)
    course_id = lesson.course.id
    if request.method == 'POST':
        lesson.delete()
        return redirect('manager_lesson_list', course_id=course_id)
    return render(request, 'manager_panel/lesson/manager_del_lesson.html',
                  {'lesson': lesson})


@user_passes_test(is_manager)
def manager_lesson_bulk_action(request: HttpRequest, course_id: int) -> HttpResponse:
    """Групповые действия над уроками курса."""
    if request.method == 'POST':
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('selected_lessons')

        if not selected_ids:
            messages.error(request, "Выберите хотя бы один урок для действия.")
            return redirect('manager_lesson_list', course_id=course_id)

        lessons = Lesson.objects.filter(id__in=selected_ids, course_id=course_id)

        if action == 'delete':
            count = lessons.count()
            lessons.delete()
            messages.success(request, f"Успешно удалено {count} урок(ов).")

    return redirect('manager_lesson_list', course_id=course_id)


@user_passes_test(is_manager)
def enrollment_request_list_view(request: HttpRequest) -> HttpResponse:
    """Список всех заявок на запись в курсы."""
    requests = EnrollmentRequest.objects.all().order_by('-created_at')
    return render(request, 'manager_panel/enrollment_request_list.html',
                  {'requests': requests})


@user_passes_test(is_manager)
def enrollment_request_approve_view(request: HttpRequest, request_id: int) -> HttpResponse:
    """Одобрение заявки на курс."""
    enroll_request = get_object_or_404(EnrollmentRequest, id=request_id)

    if enroll_request.status != 'pending':
        messages.warning(request, 'Эта заявка уже была обработана.')
    else:
        enroll_request.status = 'approved'
        enroll_request.save()
        messages.success(request, 'Заявка одобрена, студент добавлен на курс.')

    return redirect('manager_enrollment_requests')


@user_passes_test(is_manager)
def enrollment_request_reject_view(request: HttpRequest, request_id: int) -> HttpResponse:
    """Отклонение заявки на курс."""
    enroll_request = get_object_or_404(EnrollmentRequest, id=request_id)

    if enroll_request.status != 'pending':
        messages.warning(request, 'Эта заявка уже была обработана.')
    else:
        enroll_request.status = 'rejected'
        enroll_request.save()
        messages.info(request, 'Заявка отклонена.')

    return redirect('manager_enrollment_requests')


@user_passes_test(is_manager)
def questions_list(request: HttpRequest) -> HttpResponse:
    """Список часто задаваемых вопросов (FAQ)."""
    faqs = FAQ.objects.all()
    return render(request, 'manager_panel/question/manager_questions_list.html',
                  {'faqs': faqs})


@user_passes_test(is_manager)
def question_create(request: HttpRequest) -> HttpResponse:
    """Создание нового вопроса FAQ."""
    form = QuestionsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('manager_questions_list')
    return render(request, 'manager_panel/question/manager_add_question.html',
                  {'form': form})


@user_passes_test(is_manager)
def question_edit(request: HttpRequest, pk: int) -> HttpResponse:
    """Редактирование существующего вопроса FAQ."""
    question = get_object_or_404(FAQ, pk=pk)
    form = QuestionsForm(request.POST or None, request.FILES or None, instance=question)
    if form.is_valid():
        form.save()
        return redirect('manager_questions_list')
    return render(request, 'manager_panel/question/manager_add_question.html',
                  {'form': form})


@user_passes_test(is_manager)
def question_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Удаление вопроса FAQ."""
    question = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('manager_questions_list')
    return render(request, 'manager_panel/question/manager_del_question.html',
                  {'question': question})




@user_passes_test(is_manager)
def news_list(request):
    news = Newsletter.objects.all()
    return render(request, 'manager_panel/manager_news_list.html', {'news': news})


@user_passes_test(is_manager)
def news_create(request):
    form = NewsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('manager_news_list')
    return render(request, 'manager_panel/manager_add_news.html', {'form': form})


@user_passes_test(is_manager)
def news_edit(request, pk):
    news = get_object_or_404(Newsletter, pk=pk)
    form = NewsForm(request.POST or None, request.FILES or None, instance=news)
    if form.is_valid():
        form.save()
        return redirect('manager_news_list')
    return render(request, 'manager_panel/manager_add_news.html', {'form': form})


@user_passes_test(is_manager)
def news_delete(request, pk):
    news = get_object_or_404(Newsletter, pk=pk)
    if request.method == 'POST':
        news.delete()
        return redirect('manager_news_list')
    return render(request, 'manager_panel/manager_del_news.html', {'news': news})


@user_passes_test(is_manager)
def send_newsletter(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    subscribers = Subscriber.objects.filter(is_confirmed=True)

    if not subscribers:
        messages.warning(request, "Нет подтверждённых подписчиков для рассылки.")
        return redirect('manager_news_list')

    messages_list = []
    for sub in subscribers:
        messages_list.append((
            newsletter.subject,
            newsletter.message,
            'blr.artyom.gonchar@gmail.com',
            [sub.email],
        ))

    send_mass_mail(messages_list, fail_silently=False)
    messages.success(request, "Рассылка успешно отправлена подтверждённым подписчикам.")
    return redirect('manager_news_list')


@user_passes_test(is_manager)
def send_newsletter_custom(request):
    if request.method == 'POST':
        form = NewsletterSendForm(request.POST)
        if form.is_valid():
            users = form.cleaned_data['users']
            newsletter = form.cleaned_data['newsletter']

            messages_list = []
            for user in users:
                messages_list.append((
                    newsletter.title,
                    newsletter.content,
                    'your_email@example.com',  # От кого
                    [user.email],
                ))

            send_mass_mail(messages_list, fail_silently=False)
            messages.success(request, "Новость успешно отправлена выбранным пользователям.")
            return redirect('manager_users_list')  # или куда нужно
    else:
        form = NewsletterSendForm()

    return render(request, 'manager_panel/send_newsletter_custom.html', {'form': form})
