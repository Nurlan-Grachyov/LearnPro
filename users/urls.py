from rest_framework.routers import DefaultRouter

from materials.apps import LearningConfig
from users.views import CustomUserViewSets

app_name = LearningConfig.name

router = DefaultRouter()
router.register(r'user', CustomUserViewSets, basename='users')
urlpatterns = [

              ] + router.urls
