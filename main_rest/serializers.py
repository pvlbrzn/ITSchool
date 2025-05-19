from rest_framework import serializers

from main.models import (CustomUser, Course, Lesson, Payment, Blog, Subscriber, Newsletter, FAQ,
                         EnrollmentRequest, Review)


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    Serializes all fields.
    """
    class Meta:
        model = CustomUser
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.
    Serializes all fields.
    """
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lesson model.
    Serializes all fields.
    """
    class Meta:
        model = Lesson
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.
    Serializes all fields.
    """
    class Meta:
        model = Payment
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for the Blog model.
    Serializes all fields.
    """
    class Meta:
        model = Blog
        fields = '__all__'


class SubscriberSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subscriber model.
    Serializes all fields.
    """
    class Meta:
        model = Subscriber
        fields = '__all__'


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Serializer for the Newsletter model.
    Serializes all fields.
    """
    class Meta:
        model = Newsletter
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    """
    Serializer for the FAQ model.
    Serializes all fields.
    """
    class Meta:
        model = FAQ
        fields = '__all__'


class EnrollmentRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for the EnrollmentRequest model.
    Serializes all fields.
    """
    class Meta:
        model = EnrollmentRequest
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    Serializes all fields.
    """
    class Meta:
        model = Review
        fields = '__all__'
