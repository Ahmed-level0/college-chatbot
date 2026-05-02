from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Lecture, Exam

# Create your views here.
class LectureAPIView(APIView):

    def get(self, request):
        year = request.query_params.get("year")
        day = request.query_params.get("day")
        course = request.query_params.get("course")

        lectures = Lecture.objects.all()

        if year:
            lectures = lectures.filter(year__iexact=year)

        if day:
            lectures = lectures.filter(day_of_week__iexact=day)

        if course:
            lectures = lectures.filter(course_name__icontains=course)

        lectures = lectures.order_by("day_of_week", "start_time")

        data = [
            {
                "year": lecture.year,
                "day_of_week": lecture.day_of_week,
                "course_name": lecture.course_name,
                "lecturer": lecture.lecturer,
                "start_time": lecture.start_time.strftime("%H:%M"),
                "end_time": lecture.end_time.strftime("%H:%M"),
            }
            for lecture in lectures
        ]

        return Response(data)
    
class ExamAPIView(APIView):

    def get(self, request):
        year = request.query_params.get("year")
        course = request.query_params.get("course")

        exams = Exam.objects.all()

        if year:
            exams = exams.filter(year__iexact=year)

        if course:
            exams = exams.filter(course_name__icontains=course)

        exams = exams.order_by("date", "start_time")

        data = [
            {
                "year": exam.year,
                "course_name": exam.course_name,
                "date": exam.date.strftime("%Y-%m-%d"),
                "start_time": exam.start_time.strftime("%H:%M"),
                "end_time": exam.end_time.strftime("%H:%M"),
            }
            for exam in exams
        ]

        return Response(data)