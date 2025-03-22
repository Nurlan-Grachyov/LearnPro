import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenViewBase

from materials.permissions import Moderators
from users.models import CustomUser, Payments
from users.permissions import SelfUser
from users.serializers import (CustomUserSerializer, PaymentsSerializer,
                               RegisterSerializer)

logging.basicConfig(level=logging.DEBUG)


class CustomUserViewSets(viewsets.ModelViewSet):
    """
    класс пользователя с проверкой прав доступа в зависимости от метода
    """

    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        """
        Метод проверки прав доступа в зависимости от метода
        """

        if self.request.method in ("GET",):
            permission_class = [IsAuthenticated]
        elif self.request.method in ("PUT", "PATCH"):
            permission_class = [SelfUser]
        elif self.request.method == "DELETE":
            permission_class = [SelfUser | Moderators]
        else:
            permission_class = [IsAuthenticated]
        return [permission() for permission in permission_class]


class RegisterCreateAPIView(generics.CreateAPIView):
    """
    Класс регистрации пользователя
    """

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


class TokenObtainPairView(TokenViewBase):
    """
    Переопределение класса TokenObtainPairView с предоставлением доступа всем
    """

    permission_classes = [AllowAny]


class PaymentsViewSet(viewsets.ModelViewSet):
    """
    Контроллер платежей с фильтрацией и сортировкой
    """

    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("pay_date",)
