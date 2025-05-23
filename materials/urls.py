from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonListCreateApiView,
                             LessonRetrieveUpdateDestroyApiView,
                             SubscriptionViewSet)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="courses")
router.register(r"subscription", SubscriptionViewSet, basename="subscription")

urlpatterns = [
    path(
        "list_create_lesson/",
        LessonListCreateApiView.as_view(),
        name="list_create_lesson",
    ),
    path(
        "retrieve_update_destroy/<int:pk>/",
        LessonRetrieveUpdateDestroyApiView.as_view(),
        name="retrieve_update_destroy",
    ),
] + router.urls
