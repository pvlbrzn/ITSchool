from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, CourseViewSet, LessonViewSet, PaymentViewSet,
                    BlogViewSet, SubscriberViewSet, NewsletterViewSet, FAQViewSet,
                    EnrollmentRequestViewSet, ReviewViewSet)


router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'lessons', LessonViewSet, basename='lessons')
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'blogs', BlogViewSet, basename='blogs')
router.register(r'subscribers', SubscriberViewSet, basename='subscribers')
router.register(r'newsletters', NewsletterViewSet, basename='newsletters')
router.register(r'faqs', FAQViewSet, basename='faqs')
router.register(r'enrollment-requests', EnrollmentRequestViewSet, basename='enrollment-requests')
router.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]
