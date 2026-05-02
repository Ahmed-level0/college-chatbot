from django.contrib import admin
from .models import Lecture, Exam
# Register your models here.

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("course_name", "year", "date", "start_time", "end_time")
    list_filter = ("year", "course_name")
    search_fields = ("course_name",)

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ("course_name", "year", "day_of_week", "lecturer", "start_time", "end_time")
    list_filter = ("year", "day_of_week", "course_name")
    search_fields = ("course_name", "lecturer")