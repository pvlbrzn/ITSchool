from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.courses, name='courses'),
    path('teachers/', views.teachers_list, name='teachers_list'),
    path('courses/<int:pk>/', views.course_detail, name='course-detail'),
]
