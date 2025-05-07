from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Course, Lesson, Blog, CustomUser, EnrollmentRequest, Payment, FAQ,
    Subscriber, Newsletter, Review
)
from .tasks import send_newsletter_to_all


class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for CustomUser model.
    Customizes the list display, filters, search fields, and fieldsets.
    """
    model = CustomUser
    list_display = [
        'username', 'email', 'role', 'first_name', 'last_name',
        'is_staff', 'is_active'
    ]
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Information', {
            'fields': (
                'first_name', 'last_name', 'email', 'bio',
                'age', 'stack', 'phone'
            )
        }),
        ('Roles', {'fields': ('role',)}),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'email',
                'role', 'first_name', 'last_name', 'bio',
                'age', 'stack', 'phone'
            )
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin configuration for Course model.
    """
    list_display = ('title', 'description', 'language', 'skill')
    search_fields = ('title', 'language', 'skill', 'start_date')
    list_filter = ('price',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Admin configuration for Lesson model.
    """
    list_display = ('title', 'content', 'teacher', 'course')
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """
    Admin configuration for Blog model.
    """
    list_display = ('title', 'date', 'author')
    search_fields = ('title', 'author')
    list_filter = ('title', 'date', 'author')


@admin.register(EnrollmentRequest)
class EnrollmentRequestAdmin(admin.ModelAdmin):
    """
    Admin configuration for EnrollmentRequest model.
    """
    list_display = ('user', 'course', 'status', 'created_at')
    search_fields = ('user__username', 'course__title', 'status')
    list_filter = ('status', 'created_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Payment model.
    """
    list_display = ('student', 'course', 'payment_date', 'is_successful')
    search_fields = ('student__username', 'payment_date')
    list_filter = ('payment_date', 'is_successful')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """
    Admin configuration for FAQ model.
    """
    list_display = ('question', 'answer')
    search_fields = ('question',)
    list_filter = ('question',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for Review model.
    """
    list_display = ('comment', 'author', 'date', 'image')
    search_fields = ('author__username',)
    list_filter = ('date',)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """
    Admin configuration for Subscriber model.
    """
    list_display = ('email',)
    search_fields = ('email',)
    list_filter = ('email',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """
    Admin configuration for Newsletter model.
    Adds a custom action to send newsletters.
    """
    list_display = ('subject', 'created_at')
    actions = ['send_newsletter']

    @admin.action(description="📬 Send selected newsletters")
    def send_newsletter(self, request, queryset):
        """
        Sends selected newsletters using the asynchronous task.
        """
        for newsletter in queryset:
            send_newsletter_to_all.delay(newsletter.subject, newsletter.message)
        self.message_user(request, "Newsletter dispatch initiated!")
