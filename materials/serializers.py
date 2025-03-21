from rest_framework import serializers

from materials.models import Course, Lesson
from users.models import Payments


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    @staticmethod
    def get_lessons(obj):
        lessons = Lesson.objects.filter(course=obj)
        return lessons

    @staticmethod
    def get_count_lessons(obj):
        count_lessons = Lesson.objects.filter(course=obj).count()
        return count_lessons


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"
