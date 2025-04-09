from django.contrib.auth.models import Group
from django.db import connections
from rest_framework import status
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)

from materials.models import Course, Lesson, Subscription
from materials.views import (LessonListCreateApiView,
                             LessonRetrieveUpdateDestroyApiView,
                             SubscriptionViewSet)
from users.models import CustomUser


class MaterialsTest(APITestCase):
    def setUp(self):
        # создание тестовых данных
        self.owner_lesson = CustomUser.objects.create(email="owner_lesson@mail")
        self.owner_lesson.set_password("12345678")
        self.owner_lesson.save()

        self.course = Course.objects.create(
            name="test_course", description="test_course"
        )
        self.lesson_data = {
            "name": "test_lesson",
            "description": "test_lesson",
            "course": self.course.id,
        }

        self.lesson = Lesson.objects.create(
            name="test_lesson",
            description="test_lesson",
            course=self.course,
            owner=self.owner_lesson,
        )
        Lesson.objects.filter(name="test_lesson").update(
            name="test_lesson_update",
            description="test_lesson_update",
            course=self.course,
        )
        self.lesson_update = Lesson.objects.get(name="test_lesson_update")
        self.update_data = {
            "name": "test_lesson_update",
            "description": "test_lesson_update",
            "course": self.course.id,
        }

        self.factory = APIRequestFactory()
        moderators_group, created = Group.objects.get_or_create(name="Moderators")
        self.user = CustomUser.objects.create(email="test_user_sussecc@mail")
        self.user.set_password("12345678")
        self.user.groups.add(moderators_group)
        self.user.save()

        self.admin = CustomUser.objects.create(email="admin@mail.ru")
        self.admin.set_password("12345678")
        self.admin.is_staff = True
        self.admin.is_active = True
        self.admin.is_superuser = True
        self.admin.save()

        self.normal_user = CustomUser.objects.create(email="normal@mail.ru")
        self.normal_user.set_password("12345678")
        self.normal_user.save()
        self.subscription = Subscription.objects.create(
            user=self.normal_user, course=self.course
        )
        self.subscription_data = {
            "user": self.owner_lesson.id,
            "course": self.course.id,
        }

        self.user_without_root = CustomUser.objects.create(
            email="test_user_without_root@mail"
        )
        self.user_without_root.set_password("12345")
        self.user_without_root.save()

    def test_create_lesson_with_root(self):
        # тестирование создания юзером-модератором

        request = self.factory.post(
            "/materials/list_create_lesson/", data=self.lesson_data
        )

        force_authenticate(request, user=self.admin)
        response = LessonListCreateApiView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.data,
            {
                "id": 2,
                "description": "test_lesson",
                "name": "test_lesson",
                "preview": None,
                "video_url": None,
                "course": 1,
                "owner": 3,
            },
        )

        self.assertTrue(Lesson.objects.filter(name="test_lesson").exists())

    def test_create_lesson_without_root(self):
        # тестирование создания юзером без прав

        request = self.factory.post(
            "/materials/list_create_lesson/", data=self.lesson_data
        )

        force_authenticate(request, user=self.user_without_root)
        response = LessonListCreateApiView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_lesson(self):
        # тестирование получения конкретного объекта
        request = self.factory.get(
            f"/materials/retrieve_update_destroy/{self.lesson.id}/", json=self.lesson
        )
        force_authenticate(request, user=self.owner_lesson)
        response = LessonRetrieveUpdateDestroyApiView.as_view()(
            request, pk=self.lesson.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(Lesson.objects.all().exists())

    def test_update_lesson(self):
        # тестирование обновления объекта
        request = self.factory.put(
            f"/retrieve_update_destroy/{self.lesson.id}/", data=self.update_data
        )
        force_authenticate(request, user=self.owner_lesson)
        response = LessonRetrieveUpdateDestroyApiView.as_view()(
            request, pk=self.lesson.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(Lesson.objects.all().exists())

    def test_delete_lesson(self):
        # тестирование удаления объекта

        request = self.factory.delete(
            f"/materials/retrieve_update_destroy/{self.lesson.id}/",
            json=self.lesson_data,
        )

        force_authenticate(request, user=self.owner_lesson)
        response = LessonRetrieveUpdateDestroyApiView.as_view()(
            request, pk=self.lesson.id
        )

        self.lesson_update.delete()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.all().exists())

    def test_create_subscription(self):
        # тестирование создания подписки
        request = self.factory.post(
            "/materials/subscription/", data=self.subscription_data
        )
        force_authenticate(request, user=self.owner_lesson)
        response = SubscriptionViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"message": "Подписка успешно создана."},
        )
        self.assertTrue(Subscription.objects.all().exists())

    def test_delete_subscription(self):
        # тестирование удаления подписки

        request = self.factory.delete(
            f"/materials/subscription/{self.subscription.id}/", json=self.subscription
        )
        force_authenticate(request, user=self.normal_user)
        response = SubscriptionViewSet.as_view({"delete": "destroy"})(
            request, pk=self.subscription.id
        )
        self.subscription.delete()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.all().exists())
