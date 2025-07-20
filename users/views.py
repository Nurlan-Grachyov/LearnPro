import logging

from django.contrib.auth.models import update_last_login
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase

from materials.permissions import Moderators
from users.services import create_price, create_session
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


class MyTokenObtainPairView(TokenObtainPairView, TokenViewBase):
    """
    Переопределение класса TokenObtainPairView с предоставлением доступа всем
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = self.get_user(request.data)
            update_last_login(None, user)
        return response

    def get_user(self, validated_data):
        return CustomUser.objects.get(email=validated_data["email"])


class PaymentsViewSet(viewsets.ModelViewSet):
    """
    Контроллер платежей с фильтрацией и сортировкой
    """

    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("pay_date",)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        price = create_price(int(payment.payment_amount))

        session_id, payment_link = create_session(price)
        payment.link = payment_link
        payment.session_id = session_id
        payment.save()
