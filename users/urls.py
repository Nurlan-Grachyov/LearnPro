from rest_framework.routers import DefaultRouter

from materials.apps import LearningConfig
from materials.views import PaymentsViewSet
from users.views import CustomUserViewSets

app_name = LearningConfig.name

router = DefaultRouter()
router.register(r"user", CustomUserViewSets, basename="users")
router.register(r"payments", PaymentsViewSet, basename="payments")
urlpatterns = [] + router.urls
