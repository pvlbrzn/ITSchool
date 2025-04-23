from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . models import Course, Lesson, Blog, CustomUser


# Настройка отображения в админке для CustomUser
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']

    # Настройка полей в форме создания/редактирования пользователя
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email', 'bio', 'age', 'stack', 'phone')}),
        ('Роли', {'fields': ('role',)}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'password1', 'password2', 'email', 'role', 'first_name', 'last_name', 'bio', 'age', 'stack',
            'phone')}
         ),
    )
    filter_horizontal = ('groups', 'user_permissions')


# Регистрируем кастомного пользователя
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'language', 'skill')
    search_fields = ('title', 'language', 'skill', 'start_date')
    list_filter = ('price', )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'teacher', 'course')
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author')
    search_fields = ('title', 'author')
    list_filter = ('title', 'date', 'author')
