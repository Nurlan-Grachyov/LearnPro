from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenViewBase

from users.models import CustomUser
from users.serializers import CustomUserSerializer, RegisterSerializer


class CustomUserViewSets(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class RegisterCreateAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


class TokenObtainPairView(TokenViewBase):
    permission_classes = [AllowAny]
