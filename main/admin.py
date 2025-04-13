from django.contrib import admin

from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'language', 'type')
    search_fields = ('title', 'language', 'type', 'start_date')
    list_filter = ('price', )