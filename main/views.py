import asyncio
import random
from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

from . models import Course, Blog, CustomUser, EnrollmentRequest, Payment, FAQ, Review, Subscriber
from . forms import StudentRegistrationForm, SubscribeForm, ContactForm
from .utils import send_confirmation_email, send_welcome_email
from support_bot.utils import send_enrollment_update


def index(request) -> render:
    """
    Главная страница сайта, которая отображает случайные курсы, учителей и блоги.

    :param request: HTTP запрос
    :return: HTML ответ с отрендеренной главной страницей
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
    Страница курсов, на которой отображаются все доступные курсы.

    :param request: HTTP запрос
    :return: HTML ответ с отрендеренными курсами
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
    Страница деталей курса, отображает информацию о выбранном курсе и похожие курсы.

    :param request: HTTP запрос
    :param course_id: ID курса, для которого отображается информация
    :return: HTML ответ с отрендеренной страницей курса
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


def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(CustomUser, id=teacher_id, role='teacher')

    related_courses = Course.objects.filter(teachers=teacher).order_by('?')[:3]

    return render(request, 'main/teachers-details.html', {
        'teacher': teacher,
        'related_courses': related_courses
    })


def teachers_list(request) -> render:
    """
    Страница списка учителей.

    :param request: HTTP запрос
    :return: HTML ответ с отрендеренным списком учителей
    """
    teachers = CustomUser.objects.filter(role='teacher')
    return render(request, 'main/teachers.html', {'teachers': teachers})


def about(request) -> render:
    """
    Страница 'О нас', которая отображает все отзывы.

    :param request: HTTP запрос
    :return: HTML ответ с отрендеренной страницей с отзывами
    """
    reviews = Review.objects.all()
    return render(request, 'main/about-us.html', {'reviews': reviews})


def faq(request) -> render:
    """
    Страница часто задаваемых вопросов (FAQ).

    :param request: HTTP запрос
    :return: HTML ответ с отрендеренными вопросами и ответами
    """
    faqs = FAQ.objects.all()
    return render(request, 'main/faq.html', {'faqs': faqs})


def contact(request) -> render:
    """
    Страница с контактной информацией.

    :param request: HTTP запрос
    :return: HTML ответ с отрендеренной страницей контактов
    """
    return render(request, 'main/contact.html')


def blog_list(request) -> render:
    """
    Страница блога с постами.

    :param request: HTTP запрос
    :return: HTML ответ с отрендеренными блогами с пагинацией
    """
    blogs = Blog.objects.all().order_by('-date')
    paginator = Paginator(blogs, 5)  # по 5 постов на страницу

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/blog.html', {'blogs': page_obj})


def blog_details(request, blog_id: int) -> render:
    """
    Страница деталей блога.

    :param request: HTTP запрос
    :param blog_id: ID блога, для которого отображается информация
    :return: HTML ответ с отрендеренной страницей блога
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
    Перенаправление пользователя после входа в систему в зависимости от его роли.

    :param request: HTTP запрос
    :return: Перенаправление на страницу в зависимости от роли пользователя
    """
    if request.user.is_superuser:
        return redirect('/admin/')
    elif request.user.groups.filter(name='managers').exists():
        return redirect('/manager/')
    return redirect('profile')


def register(request) -> render:
    """
    Страница регистрации нового пользователя.

    :param request: HTTP запрос
    :return: HTML ответ с отрендеренной страницей регистрации
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
    Страница личного кабинета пользователя.

    :param request: HTTP запрос
    :return: HTML ответ с отрендеренной страницей личного кабинета
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
    Страница списка уроков для выбранного курса.

    :param request: HTTP запрос
    :param course_id: ID курса для отображения уроков
    :return: HTML ответ с отрендеренными уроками
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
    Отправка заявки на курс для пользователя.

    :param request: HTTP запрос
    :param course_id: ID курса, на который подается заявка
    :return: Перенаправление на страницу курса или сообщение об ошибке
    """
    course = get_object_or_404(Course, id=course_id)

    # Проверяем, не подавал ли уже заявку
    if EnrollmentRequest.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, 'Вы уже оставили заявку на этот курс.')
        return redirect('course-detail', course_id=course.id)  # куда тебе удобно

    enrollment = EnrollmentRequest.objects.create(user=request.user, course=course)
    messages.success(request, 'Заявка успешно отправлена! Проверьте статус в личном кабинете.')

    asyncio.run(send_enrollment_update(enrollment, request))

    return redirect('course-detail', course_id=course.id)


@login_required
def payment_start(request, request_id: int) -> redirect:
    """
    Начало процесса оплаты для выбранной заявки.

    :param request: HTTP запрос
    :param request_id: ID заявки на курс
    :return: Перенаправление в зависимости от статуса оплаты
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
            is_successful=True,  # В реальной ситуации это зависит от статуса транзакции
            payment_method="Manual"
        )
    except Exception as e:
        messages.error(request, 'Ошибка при создании записи об оплате. Попробуйте позже.')
        return redirect('profile')  # В случае ошибки возвращаем на профиль

    # Добавляем студента в курс
    enroll_request.course.students.add(request.user)

    # Обновляем статус заявки и удаляем её
    enroll_request.status = 'approved'
    enroll_request.save()

    # Удаляем заявку из личного кабинета (если нужно)
    enroll_request.delete()  # Удаляем заявку, так как она больше не нужна

    # Сообщаем пользователю об успешной оплате
    messages.success(request, 'Оплата прошла успешно! Вы зачислены на курс.')

    # Направляем на личный кабинет
    return redirect('profile')  # Редирект на личный кабинет пользователя


def subscribe(request) -> render:
    """
    Страница подписки на рассылку новостей.

    :param request: HTTP запрос
    :return: HTML ответ с формой подписки
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

    # if path == 'about/':
    return render(request, 'main/subscribe.html', {'form': form})
   # else:
       # return render(request, 'main/base.html', {'form': form})


def confirm_subscription(request, token):
    subscriber = get_object_or_404(Subscriber, confirmation_token=token)
    if not subscriber.is_confirmed:
        subscriber.is_confirmed = True
        subscriber.save()
        send_welcome_email(subscriber.email)
        return HttpResponse('Спасибо! Подписка подтверждена.')
    else:
        return HttpResponse('Вы уже подтвердили подписку ранее.')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"От: {name} <{email}>\n\n{message}"

        send_mail(
            subject=subject,
            message=full_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['blr.artyom.gonchar@gmail.com'],
            fail_silently=False,
        )
        return render(request, 'main/contact_success.html')

    return render(request, 'main/contact.html')


def custom_404(request, exception) -> render:
    """
    Страница ошибки 404 (не найдено).

    :param request: HTTP запрос
    :param exception: исключение, вызвавшее ошибку
    :return: HTML ответ с ошибкой 404
    """
    return render(request, 'main/404.html', status=404)


# Удалить при настройке Debug = False
def test_404(request) -> render:
    """
    Тестовая страница для ошибки 404.

    :param request: HTTP запрос
    :return: HTML ответ с ошибкой 404
    """
    return render(request, 'main/404.html', status=404)
