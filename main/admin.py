from django.contrib import admin

from . models import Course, Teacher, Student, Lesson, Blog


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'language', 'skill')
    search_fields = ('title', 'language', 'skill', 'start_date')
    list_filter = ('price', )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'bio', 'email')
    search_fields = ('first_name', 'last_name', 'bio', 'email')
    list_filter = ('stack',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email')
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    list_filter = ('last_name',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'teacher', 'course')
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date', 'author')
    search_fields = ('title', 'date', 'author')
    list_filter = ('title', 'date', 'author')
