import logging

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.permissions import Moderators, Owner
from materials.serializers import CourseSerializer, LessonSerializer

logging.basicConfig(level=logging.DEBUG)


class CourseViewSet(viewsets.ModelViewSet):
    """
    Контроллер курса с логикой создания, предоставления прав доступа в зависимости от метода и возврата списка курсов.
    """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        """
        Метод создание курса.
        """

        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """
        Метод предоставления прав доступа.
        """

        if self.action == "list":
            permission_classes = [IsAuthenticated]
        elif self.action in ("retrieve", "update", "partial_update"):
            permission_classes = [Owner | Moderators]
        elif self.action == "create":
            permission_classes = [Moderators]
        elif self.action == "destroy":
            permission_classes = [Owner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Метод возврата списка продуктов по критериям.
        """

        if (
            self.request.user.groups.filter(name="Moderators").exists()
            or self.request.user.is_superuser
        ):
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)


class LessonListCreateApiView(generics.ListCreateAPIView):
    """
    Контроллер урока для создания урока или возвращения списка уроков с логикой создания, предоставления прав доступа, в зависимости от метода, и возврата списка курсов.
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [Owner | Moderators]

    def perform_create(self, serializer):
        """
        Метод создание курса.
        """

        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """
        Метод предоставления прав доступа.
        """

        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        elif self.request.method == "POST":
            permission_classes = [Moderators]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Метод возврата списка продуктов по критериям.
        """
        if (
            self.request.user.groups.filter(name="Moderators").exists()
            or self.request.user.is_superuser
        ):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    Контроллер урока для просмотра, обновления или удаления урока с логикой предоставления прав доступа, в зависимости от метода, и возврата списка курсов.
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        """
        Метод предоставления прав доступа.
        """

        if self.request.method in ("GET", "PUT", "PATCH"):
            permission_classes = [Owner | Moderators]
        elif self.request.method == "DELETE":
            permission_classes = [Owner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Метод возврата списка продуктов по критериям.
        """

        if (
            self.request.user.groups.filter(name="Moderators").exists()
            or self.request.user.is_superuser
        ):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)
