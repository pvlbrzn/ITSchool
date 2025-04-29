from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from main.models import (CustomUser, Course, Lesson, Payment, Blog, Subscriber, Newsletter, FAQ,
                         EnrollmentRequest, Review)
from .serializers import (CustomUserSerializer, CourseSerializer, LessonSerializer, FAQSerializer,
                          PaymentSerializer, BlogSerializer, SubscriberSerializer,
                          NewsletterSerializer, EnrollmentRequestSerializer, ReviewSerializer,
                          TeacherSerializer)
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


class IndexViewSet(viewsets.ViewSet):
    """
    ViewSet для данных главной страницы (index).
    """

    @action(detail=False, methods=['get'], url_path='home')
    def index(self, request):
        teachers = CustomUser.objects.filter(role='teacher')[:8]
        courses_hot = Course.objects.order_by('title')[:8]
        courses = Course.objects.all()[:9]
        blogs = Blog.objects.order_by('-title')[:4]

        # Здесь добавляем случайные поля через сериализатор
        return Response({
            'teachers': TeacherSerializer(teachers, many=True).data,
            'courses_hot': CourseSerializer(courses_hot, many=True).data,
            'courses': CourseSerializer(courses, many=True).data,
            'blogs': BlogSerializer(blogs, many=True).data,
        })
