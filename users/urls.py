from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from materials.services import test_session
from users.apps import UsersConfig
from users.views import (CustomUserViewSets, PaymentsViewSet,
                         RegisterCreateAPIView)

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"user", CustomUserViewSets, basename="users")
router.register(r"payments", PaymentsViewSet, basename="payments")

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterCreateAPIView.as_view(), name="register"),
    path("test_session/<str:session_id>/", test_session, name="test_session"),
] + router.urls
