from rest_framework import viewsets

from users.models import CustomUser
from users.serializers import CustomUserSerializer


class CustomUserViewSets(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
