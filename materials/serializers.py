from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validator_materials_description


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор курса с логикой получения уроков и их количества
    """

    count_lessons = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()
    description = serializers.CharField(validators=[validator_materials_description])

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
    """
    Сериализатор урока
    """

    description = serializers.CharField(validators=[validator_materials_description])

    class Meta:
        model = Lesson
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор подписки
    """

    class Meta:
        model = Subscription
        fields = "__all__"
