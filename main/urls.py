from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.courses, name='courses'),
    path('teachers/', views.teachers_list, name='teachers_list'),
    path('courses/<int:pk>/', views.course_detail, name='course-detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog_list, name='blog'),
    path('blog/<int:blog_id>/', views.blog_details, name='blog_details'),
    path('parse/', views.update_blog, name='run_parse'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
