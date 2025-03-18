import logging

from rest_framework import generics, viewsets

from materials.models import Course, Lesson
from materials.permissions import Moderators, Owner
from materials.serializers import (CourseSerializer, LessonSerializer)

logging.basicConfig(level=logging.DEBUG)

class CourseViewSet(viewsets.ModelViewSet):
    logging.debug("course")
    serializer_class = CourseSerializer
    logging.debug("course1")
    queryset = Course.objects.all()
    logging.debug("course2")
    permission_classes = [Owner | Moderators]


class LessonListCreateApiView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [Owner | Moderators]


class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [Owner | Moderators]


