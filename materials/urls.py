from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import LearningConfig
from materials.views import CourseViewSet, LessonListCreateApiView, LessonRetrieveUpdateDestroy

app_name = LearningConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='courses')

urlpatterns = [
path('list_create_lesson/', LessonListCreateApiView.as_view(), name='list_create_lesson'),
path('retrieve_update_destroy/<int:pk>/', LessonRetrieveUpdateDestroy.as_view(), name='retrieve_update_destroy'),
] + router.urls