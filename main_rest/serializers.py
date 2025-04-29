import random
from rest_framework import serializers

from main.models import (CustomUser, Course, Lesson, Payment, Blog, Subscriber, Newsletter, FAQ,
                         EnrollmentRequest, Review)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class EnrollmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentRequest
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'image', 'bio']  # подбери поля под себя


class CourseSerializer(serializers.ModelSerializer):
    random_rating = serializers.SerializerMethodField()
    random_stars = serializers.SerializerMethodField()
    random_likes = serializers.SerializerMethodField()
    random_peoples = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'random_rating', 'random_stars', 'random_likes', 'random_peoples']

    def get_random_rating(self, obj):
        return round(random.uniform(3.7, 5.0), 1)

    def get_random_stars(self, obj):
        return random.randint(50, 150)

    def get_random_likes(self, obj):
        return random.randint(1500, 3000)

    def get_random_peoples(self, obj):
        return random.randint(300, 500)


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'annotation', 'image', 'date']