from rest_framework import viewsets

from main.models import (CustomUser, Course, Lesson, Payment, Blog, Subscriber, Newsletter, FAQ,
                         EnrollmentRequest, Review)
from .serializers import (CustomUserSerializer, CourseSerializer, LessonSerializer, FAQSerializer,
                          PaymentSerializer, BlogSerializer, SubscriberSerializer,
                          NewsletterSerializer, EnrollmentRequestSerializer, ReviewSerializer)
from .permissions import IsManagerOrReadOnly


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsManagerOrReadOnly]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsManagerOrReadOnly]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsManagerOrReadOnly]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsManagerOrReadOnly]


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsManagerOrReadOnly]


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [IsManagerOrReadOnly]


class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [IsManagerOrReadOnly]


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsManagerOrReadOnly]


class EnrollmentRequestViewSet(viewsets.ModelViewSet):
    queryset = EnrollmentRequest.objects.all()
    serializer_class = EnrollmentRequestSerializer
    permission_classes = [IsManagerOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsManagerOrReadOnly]
