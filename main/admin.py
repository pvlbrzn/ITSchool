from django.contrib import admin

from .models import Course, Teacher, Student


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'language', 'type')
    search_fields = ('title', 'language', 'type', 'start_date')
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
