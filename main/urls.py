from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.courses, name='courses'),
    path('courses/<int:pk>/', views.course_detail, name='course-detail'),
    path('teachers/', views.teachers_list, name='teachers_list'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog_list, name='blog'),
    path('blog/<int:blog_id>/', views.blog_details, name='blog_details'),
    path('parse/', views.update_blog, name='run_parse'),
    path('login/', auth_views.LoginView.as_view(
        template_name='main/login.html'), name='login'),
    path('after-login/', views.after_login_redirect, name='after_login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('manager/', views.manager, name='manager'),
    path('profile/', views.personal_account, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
