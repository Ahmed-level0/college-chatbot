from rest_framework.serializers import ModelSerializer
from .models import Lecture, Exam

class LectureSerializer(ModelSerializer):
    class Meta:
        model = Lecture
        fields = "__all__"


class ExamSerializer(ModelSerializer):
    class Meta:
        model = Exam
        fields = "__all__"

