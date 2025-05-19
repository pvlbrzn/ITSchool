from rest_framework import viewsets

from main.models import (CustomUser, Course, Lesson, Payment, Blog, Subscriber, Newsletter, FAQ,
                         EnrollmentRequest, Review)
from .permissions import IsManagerOrReadOnly, IsManager
from .serializers import (CustomUserSerializer, CourseSerializer, LessonSerializer, FAQSerializer,
                          PaymentSerializer, BlogSerializer, SubscriberSerializer,
                          NewsletterSerializer, EnrollmentRequestSerializer, ReviewSerializer)


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing CustomUser instances.
    Accessible only by users with manager permissions.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsManager]


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Course instances.
    Managers can edit, others have read-only access.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsManagerOrReadOnly]


class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Lesson instances.
    Managers can edit, others have read-only access.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsManagerOrReadOnly]


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Payment instances.
    Accessible only by users with manager permissions.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsManager]


class BlogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Blog instances.
    Managers can edit, others have read-only access.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsManagerOrReadOnly]


class SubscriberViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Subscriber instances.
    Accessible only by users with manager permissions.
    """
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [IsManager]


class NewsletterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Newsletter instances.
    Accessible only by users with manager permissions.
    """
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [IsManager]


class FAQViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing FAQ instances.
    Managers can edit, others have read-only access.
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsManagerOrReadOnly]


class EnrollmentRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing EnrollmentRequest instances.
    Managers can edit, others have read-only access.
    """
    queryset = EnrollmentRequest.objects.all()
    serializer_class = EnrollmentRequestSerializer
    permission_classes = [IsManagerOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Review instances.
    Managers can edit, others have read-only access.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsManagerOrReadOnly]
