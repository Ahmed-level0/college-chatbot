from django.db import models

# Create your models here.
class Lecture(models.Model):
    year = models.CharField(max_length=20)
    day_of_week = models.CharField(max_length=20)
    course_name = models.CharField(max_length=255)
    lecturer = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.course_name} - {self.day_of_week}"
    
class Exam(models.Model):
    year = models.CharField(max_length=20)
    course_name = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.course_name} Exam"