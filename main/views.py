import random

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from . models import Course, Blog, CustomUser, EnrollmentRequest, Payment, FAQ
from . services import parse_blog
from . forms import StudentRegistrationForm, SubscribeForm
from .utils import send_welcome_email


def index(request):
    teachers = CustomUser.objects.filter(role='teacher')[:8]
    courses_hot = Course.objects.order_by('title')[:8]
    blogs = Blog.objects.order_by('-title')[:8]

    skill = request.GET.get('skill', 'all')
    if skill == 'all':
        courses = Course.objects.all()[:9]
    else:
        courses = Course.objects.filter(skill=skill)[:9]

    for course in courses:
        course.random_rating = round(random.uniform(3.7, 5.0), 1)
        course.random_stars = random.randint(50, 150)
        course.random_likes = random.randint(1500, 3000)
        course.random_peoples = random.randint(300, 500)

    return render(request, 'main/index.html',
                  {'teachers': teachers,
                   'courses_hot': courses_hot,
                   'courses': courses,
                   'blogs': blogs,
                   'current_skill': skill})


def courses(request):
    courses = Course.objects.all()
    return render(request, 'main/courses.html', {'courses': courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Ищем похожие курсы (по языку или навыку), исключая текущий
    related_courses = Course.objects.filter(
        Q(language=course.language) | Q(skill=course.skill)
    ).exclude(id=course.id).order_by('?')[:3]  # случайные 3 похожих курса

    return render(request, 'main/course-details.html', {
        'course': course,
        'related_courses': related_courses
    })


def teachers_list(request):
    teachers = CustomUser.objects.filter(role='teacher')
    return render(request, 'main/teachers.html', {'teachers': teachers})


def about(request):
    return render(request, 'main/about-us.html')


def faq(request):
    faqs = FAQ.objects.all()
    return render(request, 'main/faq.html', {'faqs': faqs})


def contact(request):
    return render(request, 'main/contact.html')


def blog_list(request):
    blogs = Blog.objects.all().order_by('-date')
    paginator = Paginator(blogs, 5)  # по 5 постов на страницу

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/blog.html', {'blogs': page_obj})


def blog_details(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'main/blog-details.html', {'blog': blog})


def update_blog(request):
    if request.method == 'POST':
        try:
            parse_blog()  # Запускаем парсинг
            messages.success(request, "Посты успешно обновлены!")  # Успешное сообщение
        except Exception as e:
            messages.error(request, f"Ошибка при обновлении постов: {e}")  # Сообщение об ошибке

    return redirect('index')


@login_required
def after_login_redirect(request):
    if request.user.is_staff:
        return redirect('/admin/')
    return redirect('/')


def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Или на любую страницу после регистрации
    else:
        form = StudentRegistrationForm()
    return render(request, 'main/registration.html', {'form': form})


@login_required
def personal_account(request):
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

    return render(request, 'main/personal-account.html', {
        'courses': courses,
        'user_role': user.get_role_display(),
        'enrollment_requests': enrollment_requests,
    })


@login_required()
def lesson_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()

    return render(request, 'main/personal-account-lessons.html', {
        'course': course,
        'lessons': lessons,
    })


@login_required
def enroll_request_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Проверяем, не подавал ли уже заявку
    if EnrollmentRequest.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, 'Вы уже оставили заявку на этот курс.')
        return redirect('course-detail', course_id=course.id)  # куда тебе удобно

    EnrollmentRequest.objects.create(user=request.user, course=course)
    messages.success(request, 'Заявка успешно отправлена! Проверьте статус в личном кабинете.')
    return redirect('course-detail', course_id=course.id)


@login_required
def payment_start(request, request_id):
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

def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            print(f"Письмо отправляется на: {subscriber.email}")
            send_welcome_email(subscriber.email)
            messages.success(request, 'Вы успешно подписались!')
            return redirect('subscribe')
        else:
            print("Форма НЕ прошла валидацию!")
            messages.error(request, 'Ошибка! Проверьте правильность email.')
    else:
        form = SubscribeForm()
    return render(request, 'main/base.html', {'form': form})
