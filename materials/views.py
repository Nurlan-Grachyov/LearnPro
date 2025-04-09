import logging
from datetime import datetime

import pytz
from django.utils import timezone
from rest_framework import generics, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from yaml import serialize

from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPaginator
from materials.permissions import Moderators, Owner
from materials.serializers import (CourseSerializer, LessonSerializer,
                                   SubscriptionSerializer)
from materials.tasks import send_email_about_update_materials

logging.basicConfig(level=logging.DEBUG)


class CourseViewSet(viewsets.ModelViewSet):
    """
    Контроллер курса с логикой создания, предоставления прав доступа в зависимости от метода и возврата списка курсов.
    """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialsPaginator

    def perform_create(self, serializer):
        """
        Метод создание курса.
        """

        serializer.save(owner=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        print(kwargs)
        course_id = kwargs.get("pk")
        print(course_id)
        course = Course.objects.get(id=course_id)
        print(course)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            subs = Subscription.objects.filter(course=course.id)
            print(subs)
            users_ids = [sub.user.id for sub in subs]
            if users_ids:
                send_email_about_update_materials(users_ids)
            return Response({"message": "Курс успешно обновлен"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    pagination_class = MaterialsPaginator

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

    def partial_update(self, request, *args, **kwargs):
        lesson_id = kwargs.get("pk")
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"message": "Такого урока не существует"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LessonSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            subs = Subscription.objects.filter(course=lesson.course.id)
            users_ids = [sub.user.id for sub in subs]
            if users_ids:
                send_email_about_update_materials(users_ids)
            return Response({"message": "Урок успешно обновлен"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    вьюха, в которой осуществлена логика создания подписки и удаления подписки на курс
    """

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Создание новой подписки.
        """

        course_id = request.data.get("course")
        logging.debug(course_id)
        course_item = get_object_or_404(Course, pk=course_id)
        logging.debug(course_item)

        subscription_exists = Subscription.objects.filter(
            user=request.user, course=course_item
        ).exists()

        if subscription_exists:
            return Response({"message": "Вы уже подписаны на этот курс."})

        Subscription.objects.create(user=request.user, course=course_item)

        return Response({"message": "Подписка успешно создана."})

    def destroy(self, request, *args, **kwargs):
        """
        Удаление существующей подписки.
        """

        subs_id = kwargs.get("pk")

        subscription = Subscription.objects.filter(id=subs_id)

        if not subscription.exists():
            return Response({"message": "У вас нет активной подписки на этот курс."})

        subscription.delete()

        return Response({"message": "Подписка успешно удалена."})
