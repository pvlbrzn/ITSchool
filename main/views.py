from django.shortcuts import render, get_object_or_404
from . models import Course, Teacher


def index(request):
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    return render(request, 'main/index.html', {'courses': courses, 'teachers': teachers})


def courses(request):
    courses = Course.objects.all()
    return render(request, 'main/courses.html', {'courses': courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/detail.html', {'course': course})


def teachers_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'main/teachers.html', {'teachers': teachers})
