import random
from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpRequest
from django.core.mail import send_mail
from django.conf import settings

from .models import Course, Blog, CustomUser, EnrollmentRequest, Payment, FAQ, Review, Subscriber
from .forms import StudentRegistrationForm, SubscribeForm
from .utils import send_confirmation_email, send_welcome_email
from support_bot.utils import notify_about_enrollment


def index(request) -> render:
    """
    The site's home page, which displays random courses, teachers, and blogs.

    :param request: HTTP request
    :return: HTML response with the rendered home page
    """
    teachers = CustomUser.objects.filter(role='teacher')[:8]
    courses_hot = Course.objects.order_by('title')[:8]
    courses = Course.objects.all()[:9]
    blogs = Blog.objects.order_by('-title')[:4]

    for course in courses:
        course.random_rating = round(random.uniform(3.7, 5.0), 1)
        course.random_stars = random.randint(50, 150)
        course.random_likes = random.randint(1500, 3000)
        course.random_peoples = random.randint(300, 500)

    return render(
        request,
        'main/index.html',
        {
            'teachers': teachers,
            'courses_hot': courses_hot,
            'courses': courses,
            'blogs': blogs
        }
    )


def courses(request) -> render:
    """
    A courses page that displays all available courses.

    :param request: HTTP request
    :return: HTML response with rendered courses
    """
    courses = Course.objects.all()

    for course in courses:
        course.random_rating = round(random.uniform(3.7, 5.0), 1)
        course.random_stars = random.randint(50, 150)
        course.random_likes = random.randint(1500, 3000)
        course.random_peoples = random.randint(300, 500)

    return render(request, 'main/courses.html', {'courses': courses})


def course_detail(request, course_id: int) -> render:
    """
    Course details page, displays information about the selected course and similar courses.

    :param request: HTTP request
    :param course_id: ID of the course for which information is displayed
    :return: HTML response with the rendered course page
    """
    course = get_object_or_404(Course, id=course_id)

    # Ищем похожие курсы (по языку или навыку), исключая текущий
    related_courses = Course.objects.filter(
        Q(language=course.language) | Q(skill=course.skill)
    ).exclude(id=course.id).order_by('?')[:3]  # случайные 3 похожих курса

    return render(request, 'main/course-details.html', {
        'course': course,
        'related_courses': related_courses
    })


def teacher_detail(request, teacher_id: int) -> render:
    """
    Displays the details of a specific teacher along with a few random related courses.

    :param request: The incoming HTTP request.
    :param teacher_id: ID of the teacher to display.
    :return: Rendered HTML page with teacher details and related courses.
    """
    teacher = get_object_or_404(CustomUser, id=teacher_id, role='teacher')

    related_courses = Course.objects.filter(teachers=teacher).order_by('?')[:3]

    return render(request, 'main/teachers-details.html', {
        'teacher': teacher,
        'related_courses': related_courses
    })


def teachers_list(request) -> render:
    """
    Teacher list page.

    :param request: HTTP request
    :return: HTML response with rendered teacher list
    """
    teachers = CustomUser.objects.filter(role='teacher')
    return render(request, 'main/teachers.html', {'teachers': teachers})


def about(request) -> render:
    """
    About Us page that displays all reviews.

    :param request: HTTP request
    :return: HTML response with rendered review page
    """
    reviews = Review.objects.all()
    return render(request, 'main/about-us.html', {'reviews': reviews})


def faq(request) -> render:
    """
    Frequently asked questions (FAQ) page.

    :param request: HTTP request
    :return: HTML response with rendered questions and answers
    """
    faqs = FAQ.objects.all()
    return render(request, 'main/faq.html', {'faqs': faqs})


def contact(request) -> render:
    """
    Contact information page.

    :param request: HTTP request
    :return: HTML response with rendered contact page
    """
    return render(request, 'main/contact.html')


def blog_list(request) -> render:
    """
    Blog page with posts.

    :param request: HTTP request
    :return: HTML response with rendered blogs with pagination
    """
    blogs = Blog.objects.all().order_by('-date')
    paginator = Paginator(blogs, 5)  # по 5 постов на страницу

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/blog.html', {'blogs': page_obj})


def blog_details(request, blog_id: int) -> render:
    """
    Blog details page.

    :param request: HTTP request
    :param blog_id: ID of the blog to display information for
    :return: HTML response with the rendered blog page
    """
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'main/blog-details.html', {'blog': blog})


def custom_login_view(request) -> render:
    """
    Страница для входа пользователя в систему.

    :param request: HTTP запрос
    :return: HTML ответ с отрендеренной страницей входа
    """
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Если пользователь не выбрал "Запомнить меня"
            if not request.POST.get('remember'):
                request.session.set_expiry(0)
            else:
                # Если выбрано "Запомнить меня", сессия длится 3 дня
                request.session.set_expiry(timedelta(days=3))

            return redirect('after_login')

    return render(request, 'main/login.html', {'form': form})


@login_required
def after_login_redirect(request) -> redirect:
    """
    Redirect the user after logging in, depending on their role.

    :param request: HTTP request
    :return: Redirect to a page, depending on the user's role
    """
    if request.user.is_superuser:
        return redirect('/admin/')
    elif request.user.groups.filter(name='managers').exists():
        return redirect('/manager/')
    return redirect('profile')


def register(request) -> render:
    """
    New user registration page.

    :param request: HTTP request
    :return: HTML response with rendered registration page
    """
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Или на любую страницу после регистрации
    else:
        form = StudentRegistrationForm()

    return render(request, 'main/registration.html', {'form': form})


@login_required
def personal_account(request) -> render:
    """
    User's personal account page.

    :param request: HTTP request
    :return: HTML response with rendered personal account page
    """
    user = request.user

    if user.is_student():
        courses = user.courses_as_student.all()
        enrollment_requests = EnrollmentRequest.objects.filter(user=user).select_related('course')
    elif user.is_teacher():
        courses = user.courses_as_teacher.all()
        enrollment_requests = None
    else:
        courses = Course.objects.all()
        enrollment_requests = None

    return render(
        request,
        'main/personal-account.html',
        {
            'courses': courses,
            'user_role': user.get_role_display(),
            'enrollment_requests': enrollment_requests
        }
    )


@login_required
def lesson_list(request, course_id: int) -> render:
    """
    Lesson list page for the selected course.

    :param request: HTTP request
    :param course_id: Course ID to display lessons
    :return: HTML response with rendered lessons
    """
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()

    return render(
        request,
        'main/personal-account-lessons.html',
        {'course': course, 'lessons': lessons}
    )


@login_required
def enroll_request_view(request, course_id: int) -> redirect:
    """
    Submit a course request for the user.

    :param request: HTTP request
    :param course_id: ID of the course being applied for
    :return: Redirect to the course page or an error message
    """
    course = get_object_or_404(Course, id=course_id)

    # Проверяем, не подавал ли уже заявку
    if EnrollmentRequest.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, 'Вы уже оставили заявку на этот курс.')
        return redirect('course-detail', course_id=course.id)  # куда тебе удобно

    enrollment = EnrollmentRequest.objects.create(user=request.user, course=course)
    messages.success(request, 'Заявка успешно отправлена! Проверьте статус в личном кабинете.')

    notify_about_enrollment(request, enrollment)

    return redirect('course-detail', course_id=course.id)


@login_required
def payment_start(request, request_id: int) -> redirect:
    """
    Start the payment process for the selected application.

    :param request: HTTP request
    :param request_id: Course application ID
    :return: Redirect depending on the payment status
    """
    enroll_request = get_object_or_404(EnrollmentRequest, id=request_id, user=request.user)

    # Проверяем, что заявка одобрена
    if enroll_request.status != 'approved':
        messages.error(request, 'Вы не можете оплатить этот курс, так как заявка не была одобрена.')
        return redirect('student_enrollment_requests')  # Направляем на страницу с заявками

    # Создаем запись о платеже
    try:
        Payment.objects.create(
            amount=enroll_request.course.price,
            student=request.user,
            course=enroll_request.course,
            is_successful=True,
            payment_method="Manual"
        )
    except Exception as e:
        messages.error(request, 'Ошибка при создании записи об оплате. Попробуйте позже.')
        return redirect('profile')  # В случае ошибки возвращаем на профиль

    # Добавляем студента в курс
    enroll_request.course.students.add(request.user)

    enroll_request.status = 'approved'
    enroll_request.save()
    enroll_request.delete()
    messages.success(request, 'Оплата прошла успешно! Вы зачислены на курс.')
    return redirect('profile')


def subscribe(request) -> render:
    """
    Newsletter subscription page.

    :param request: HTTP request
    :return: HTML response with subscription form
    """
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber, created = Subscriber.objects.get_or_create(email=email)

            if subscriber.is_confirmed:
                messages.info(request, 'Вы уже подписаны.')
            else:
                send_confirmation_email(subscriber, request)
                messages.success(request, 'Проверьте вашу почту для подтверждения подписки.')

            return redirect('subscribe')
        else:
            print("Форма НЕ прошла валидацию!")
            messages.error(request, 'Ошибка! Проверьте правильность email.')
    else:
        form = SubscribeForm()

    return render(request, 'main/subscribe.html', {'form': form})


def confirm_subscription(request: HttpRequest, token: str) -> HttpResponse:
    """
    Confirms a user's email subscription using a token.

    :param request: The incoming HTTP request.
    :param token: Unique confirmation token.
    :return: HTTP response indicating confirmation result.
    """
    subscriber = get_object_or_404(Subscriber, confirmation_token=token)

    if not subscriber.is_confirmed:
        subscriber.is_confirmed = True
        subscriber.save()
        send_welcome_email(subscriber.email)
        return HttpResponse('Thank you! Your subscription has been confirmed.')
    return HttpResponse('You have already confirmed your subscription.')


def contact(request: HttpRequest) -> HttpResponse:
    """
    Handles contact form submissions by sending an email to the admin.

    :param request: The incoming HTTP request.
    :return: Rendered success page or contact form.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"From: {name} <{email}>\n\n{message}"

        send_mail(
            subject=subject,
            message=full_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['blr.artyom.gonchar@gmail.com'],
            fail_silently=False,
        )
        return render(request, 'main/contact_success.html')

    return render(request, 'main/contact.html')


def custom_404(request: HttpRequest, exception: Exception) -> HttpResponse:
    """
    Custom 404 error page view.

    :param request: The HTTP request.
    :param exception: The exception that triggered the 404.
    :return: Rendered 404 HTML page.
    """
    return render(request, 'main/404.html', status=404)


def test_404(request: HttpRequest) -> HttpResponse:
    """
    Test view for simulating a 404 error. For development use only.

    :param request: The HTTP request.
    :return: Rendered 404 HTML page.
    """
    return render(request, 'main/404.html', status=404)
