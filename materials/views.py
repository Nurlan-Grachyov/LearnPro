import logging

from rest_framework import generics, viewsets

from materials.models import Course, Lesson
from materials.permissions import Moderators, Owner
from materials.serializers import (CourseSerializer, LessonSerializer)

logging.basicConfig(level=logging.DEBUG)


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [Owner | Moderators]

    def get_queryset(self):
        if self.action == "list":
            logging.debug('go')
            if not self.request.user.groups.filter(name='Moderators').exists() or not self.request.user.is_superuser:
                return Course.objects.filter(owner=self.request.user)
            return Course.objects.all()
        else:
            permission_classes = [Owner | Moderators]
            return permission_classes


class LessonListCreateApiView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [Owner | Moderators]


class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [Owner | Moderators]
