from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, CourseViewSet, LessonViewSet, PaymentViewSet,
                    BlogViewSet, SubscriberViewSet, NewsletterViewSet, FAQViewSet,
                    EnrollmentRequestViewSet, ReviewViewSet, IndexViewSet)


router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'subscribers', SubscriberViewSet)
router.register(r'newsletters', NewsletterViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'enrollment-requests', EnrollmentRequestViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'index', IndexViewSet, basename='index')

urlpatterns = [
    path('', include(router.urls)),
]
