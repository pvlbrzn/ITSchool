from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.courses, name='courses'),
    path('courses/<int:course_id>/', views.course_detail, name='course-detail'),
    path('teachers/', views.teachers_list, name='teachers_list'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog_list, name='blog'),
    path('blog/<int:blog_id>/', views.blog_details, name='blog_details'),
    path('login/', views.custom_login_view, name='login'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('after-login/', views.after_login_redirect, name='after_login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('manager/', include('manager_panel.urls')),
    path('profile/', views.personal_account, name='profile'),
    path('profile/<int:course_id>/lessons/', views.lesson_list, name='personal_lesson_list'),
    path('courses/<int:course_id>/enroll/', views.enroll_request_view, name='enroll_request'),
    path('payment/<int:request_id>/', views.payment_start, name='payment_start'),
    path('subscribe/', views.subscribe, name='subscribe'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
