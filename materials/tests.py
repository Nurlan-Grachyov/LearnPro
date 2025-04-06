from django.contrib.auth.models import Group
from django.db import connections
from rest_framework import status
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)

from materials.models import Course, Lesson, Subscription
from materials.views import LessonListCreateApiView
from users.models import CustomUser


class MaterialsTest(APITestCase):
    def setUp(self):
        # создание тестовых данных

        self.course = Course.objects.create(
            name="test_course", description="test_course"
        )
        self.lesson_data = {
            "name": "test_lesson",
            "description": "test_lesson",
            "course": 21,
        }
        self.lesson = Lesson.objects.create(
            name="test_lesson", description="test_lesson", course=self.course.id
        )
        self.lesson_update = Lesson.objects.filter(name="test_lesson").update(
            name="test_lesson_update", description="test_lesson_update", course=self.course.id
        )
        self.factory = APIRequestFactory()
        moderators_group, created = Group.objects.get_or_create(name="Moderators")
        self.user = CustomUser.objects.create_user(email="test_user_sussecc@mail")
        self.user.set_password("12345678")
        self.user.save()
        self.user.groups.add(moderators_group)

        self.normal_user = CustomUser.objects.create(email="normal@mail.ru")
        self.subscription = Subscription.objects.create(
            user=self.normal_user, course=self.course.id
        )

    def tearDown(self):
        super().tearDown()
        connections.close_all()

    def test_create_lesson_with_root(self):
        # тестирование создания юзером-модератором

        request = self.factory.post("/list_create_lesson/", json=self.lesson_data)

        force_authenticate(request, user=self.user)
        response = LessonListCreateApiView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "name": "test_lesson",
                "description": "test_lesson",
                "course": self.course.id,
                "owner": None,
            },
        )

        self.assertTrue(Lesson.objects.all().exists())

    def test_create_lesson_without_root(self):
        # тестирование создания юзером без прав

        self.user_without_root = CustomUser.objects.create_user(
            email="test_user_without_root@mail"
        )
        self.user_without_root.set_password("12345")

        request = self.factory.post("/list_create_lesson/", json=self.lesson_data)

        force_authenticate(request, user=self.user)
        response = LessonListCreateApiView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_lesson(self):
        # тестирование получения конкретного объекта

        response = self.client.get(
            f"/retrieve_update_destroy/{self.lesson.id}/", json=self.lesson_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.id,
                "name": "test_lesson",
                "description": "test_lesson",
                "course": self.course.id,
                "owner": None,
            },
        )
        self.assertTrue(Lesson.objects.all().exists())

    def test_update_lesson(self):
        # тестирование обновления объекта

        response = self.client.put(
            f"/retrieve_update_destroy/{self.lesson.id}/", json=self.lesson_update
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.id,
                "name": "test_lesson_update",
                "description": "test_lesson_update",
                "course": self.course.id,
                "owner": None,
            },
        )
        self.assertTrue(Lesson.objects.all().exists())

    def test_delete_lesson(self):
        # тестирование удаления объекта

        response = self.client.delete(
            f"/retrieve_update_destroy/{self.lesson.id}/", json=self.lesson_data
        )
        self.lesson_update.delete()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Lesson.objects.all().exists(), False)

    def test_create_subscription(self):
        # тестирование создания подписки

        response = self.client.post("/subscription/", json=self.subscription)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                "id": self.subscription.id,
                "user": self.normal_user.id,
                "course": self.course.id,
            },
        )
        self.assertTrue(Subscription.objects.all().exists())

    def test_delete_subscription(self):
        # тестирование удаления подписки

        response = self.client.delete(
            f"/subscription/{self.subscription.id}/", json=self.subscription
        )
        self.subscription.delete()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Subscription.objects.all().exists(), False)
