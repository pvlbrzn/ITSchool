import random

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test

from . models import Course, Blog, CustomUser
from . services import parse_blog
from . forms import StudentRegistrationForm


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
    return render(request, 'courses/detail.html', {'course': course})


def teachers_list(request):
    teachers = CustomUser.objects.filter(role='teacher')
    return render(request, 'main/teachers.html', {'teachers': teachers})


def about(request):
    return render(request, 'main/about-us.html')


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
    elif user.is_teacher():
        courses = user.courses_as_teacher.all()
    else:
        courses = Course.objects.all()

    return render(request, 'main/personal-account.html', {
        'courses': courses,
        'user_role': user.get_role_display()
    })


def is_manager(user):
    return CustomUser.is_superuser or CustomUser.groups.filter(name='managers').exists()


@user_passes_test(is_manager)
def manager(request):
    return render(request, 'main/manager-account.html')

